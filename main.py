import math
import sys
import pygame
import pygame_gui
import time
from pygame.locals import *

class MouseInput:
    '''
    pygame nu contine un feature pentru apasarea/eliberarea mouse-ului
    '''

    def __init__(self):
        self.apasat = False
        self.eliberat = False

    def update(self):
        stare_curenta = pygame.mouse.get_pressed()

        self.eliberat = False

        if self.apasat and  stare_curenta[0] == False:
            self.eliberat = True

        self.apasat = stare_curenta[0]


class NodGraf:
    '''
    retine pozitia unui nod graf (x,y)
    calculeaza pozitia unui nod pe ecranul desenat
    '''

    def __init__(self, punct):
        self.punct = punct

        # 70 e distanta dintre noduri
        # x-ul este calculat in functie de coordonata y a punctului deoarece este direct proportionala cu
        # distanta de care am nevoie pentru o afisare corecta
        self.punct_desenat = (MARGINI + punct[1] * 70, 2 * MARGINI + punct[0] * 70)


class TablaDeJoc:
    '''
    Grafica tabelei de joc_pornit
    '''

    def __init__(self):

        '''
        Se creeaza intreaga tabla ca un graf. Avem un dictionar
        care ne spune ce nod se afla la o pozitie din grid, o lista
        de noduri, si o lista de adiacenta pentru a putea parcurge
        graful cu usurinta
        '''

        self.noduri = [] # lista de obiecte de tip NodGraf
        self.numar_nod_in_grafic = {} # dictionar de forma: { (x,y): numar nod din grafic }
        self.muchii = {}  # dictionar de forma: { numarul nod in grafic : lista numar nod in grafic } reprezentand muchiile

        nr = 0
        for i in range(7):
            for j in range(7):
                if (j>=2 and j<=4) or (i>=2 and i<=4):
                    numar_nod = NodGraf((i, j))

                    self.noduri.append(numar_nod)

                    # numerotarea incepe din stanga sus
                    self.numar_nod_in_grafic[numar_nod.punct] = nr  # 0, 1, 2, 3...
                    nr +=1

        for nod_coordonata in self.noduri:
            nr=self.numar_nod_in_grafic[nod_coordonata.punct]
            self.muchii[nr]=[]

        for nod_coordonata in self.noduri:
            nr=self.numar_nod_in_grafic[nod_coordonata.punct]
            (i, j) = nod_coordonata.punct

            c1 = (i-1, j)
            c2 = (i, j-1)
            c3 = (i+1, j)
            c4 = (i, j+1)
            c5 = (i+1, j+1)
            c6 = (i-1, j-1)
            c7 = (i+1, j-1)
            c8 = (i-1, j+1)

            if c1 in self.numar_nod_in_grafic.keys():
                self.muchii[nr].append(self.numar_nod_in_grafic[c1])
            if c2 in self.numar_nod_in_grafic.keys():
                self.muchii[nr].append(self.numar_nod_in_grafic[c2])
            if c3 in self.numar_nod_in_grafic.keys():
                self.muchii[nr].append(self.numar_nod_in_grafic[c3])
            if c4 in self.numar_nod_in_grafic.keys():
                self.muchii[nr].append(self.numar_nod_in_grafic[c4])
            if c5 in self.numar_nod_in_grafic.keys() and ((i,j) != (1,4)) and ((i,j) != (4,1)) :
                self.muchii[nr].append(self.numar_nod_in_grafic[c5])
            if c6 in self.numar_nod_in_grafic.keys() and ((i,j) != (2,5)) and ((i,j) != (5,2)) :
                self.muchii[nr].append(self.numar_nod_in_grafic[c6])
            if c7 in self.numar_nod_in_grafic.keys() and ((i,j) != (1,2)) and ((i,j) != (4,5)):
                self.muchii[nr].append(self.numar_nod_in_grafic[c7])
            if c8 in self.numar_nod_in_grafic.keys() and ((i,j) != (2,1))  and ((i,j) != (5,4)):
                self.muchii[nr].append(self.numar_nod_in_grafic[c8])

    def desenare_tabla_joc(self, ecran):

        '''
        Functia care deseneaza tabla de joc_pornit, luandu-se
        dupa relatiile dintre muchii si pozitiile nodurilor
        '''

        for i in range(len(self.noduri)):
            for muchie in self.muchii[i]:
                pozitia1 = self.noduri[i].punct_desenat
                pozitia2 = self.noduri[muchie].punct_desenat

                # desenare linie dintre doua puncte
                pygame.draw.line(ecran, (0, 0, 0),pozitia1, pozitia2, 4)


class ConfiguratieJoc:
    '''
    Informatie despre o stare a jocului.
    Lista cu nodurile cu gaste.
    Variabila care retine pozitia vulpii.
    '''

    def __init__(self, graf_joc, gaste=None, vulpe=None):
        '''
        Creare configuratie tabla
        '''

        self.graf_joc = graf_joc
        # initializare vulpe si nr gaste

        if gaste == None:
            self.gaste = [] # lista cu numerele nodurilor pe care se afla gastele

            for i in range(2, 7):
                for j in range(7):
                        if (i==4) or ((i==5 or i==6) and (j>=2 and j<=4)) or ((i==2 or i==3) and (j==0 or j==6)):
                            self.gaste.append(graf_joc.numar_nod_in_grafic[(i, j)])
        else:
            self.gaste = gaste.copy()

        if vulpe == None:
            self.vulpe = graf_joc.numar_nod_in_grafic[(2, 3)]
        else:
            self.vulpe = vulpe # numarul nodului pe care se afla vulpea

    def gaseste_castigator(self, graf_joc):

        '''
        Metoda care returneaza castigatorul.
        Daca vulpea nu mai poate face miscari, atunci gastele sunt castigatoare.
        Daca sunt 9 sau mai putini gaste ramase, atunci acestea nu mai au cum sa inconjoare vulpea, deci castiga vulpea.
        Altfel nu am configuratie finala.
        '''

        configurari_vulpe = Vulpe.configurari_posibile(graf_joc, self)
        if len(configurari_vulpe) == 0:
            return 0

        if len(self.gaste) <= 9: #TODO : aici de modificat nr de gaste
            return 1

        return -1

    def afisare_consola(self, graf_joc):

        '''
        Metoda care afiseaza tabla de joc_pornit in consola
        '''

        for x in range(8):
            for y in range(8):
                if graf_joc.numar_nod_in_grafic.get((x, y)) != None:

                    # accesez valoarea din dictionarul numar_nod_in_grafic
                    numar_nod = graf_joc.numar_nod_in_grafic[(x, y)]

                    if numar_nod in self.gaste:
                        print("G ", end="")
                    elif numar_nod == self.vulpe:
                        print("V ", end="")
                    else:
                        print("# ", end="")
                else:
                    print("  ", end="")

            print("\n", end="")

    def incarcare(self, ecran, graf_joc):

        '''
        Cercuri albe la pozitiile gastelor
        Cerc negru la pozitia vulpii
        Daca au castigat gastele le va desena cu verde.
        Daca a castigat jaguarul il va desena cu verde.
        '''

        castigator = self.gaseste_castigator(graf_joc)

        for gasca in self.gaste:

            culoare_gasca = (255, 255, 255) # alb #TODO: de modificat imagine

            if castigator == 0: # au castigat gastele
                culoare_gasca = (0, 255, 0)

            pygame.draw.circle(ecran, culoare_gasca, self.graf_joc.noduri[gasca].punct_desenat, RAZA_CERC)
            pygame.draw.circle(ecran, (0, 0, 0), self.graf_joc.noduri[gasca].punct_desenat, RAZA_CERC, 5)

        culoare_vulpe = (0, 0, 0)

        if castigator == 1: # a castigat vulpea
            culoare_vulpe = (0, 255, 0)

        pygame.draw.circle(ecran, culoare_vulpe, self.graf_joc.noduri[self.vulpe].punct_desenat, RAZA_CERC)

def distanta_Euclid (punct1, punct2) :
    """
    Distanta dintre doua punce de pe ecran.
    Cand verific daca s-a dat click pe o pozitie de pe tabla grafica.
    """
    return math.sqrt((punct1[0] - punct2[0]) ** 2 + (punct1[1] - punct2[1]) ** 2)

def inlocuire_valoare(vector,valoare_de_inlocuit, valoare_noua):
    '''
    Inlocuiesc o valoare veche cu o valoare noua
    O folosesc cand mut o gasca pe tabla.
    '''

    vector_nou = vector.copy()

    for i in range(len(vector_nou)):
        if vector_nou[i] == valoare_de_inlocuit:
            vector_nou[i] = valoare_noua

    return vector_nou


class Jucator:
    '''
    Clasa de baza pe care o mostenesc toate tipurile de jucatori, chit
    ca sunt jucatori umani sau AI-uri.
    '''

    def __init__(self):
        pass

    def muta(self, graf_joc, configuratie_curenta):
        '''
        Din moment ce e un jucator generic, nu va face nicio mutare
        '''
        return configuratie_curenta

    def returneaza_nod_apasat(self, graf_joc, punct):

        '''
        functie care primeste graful tablei de joc_pornit si pozitia la care s-a dat click pe ecran
        si returneaza nodul pe care s-a dat click (daca s-a dat click pe un nod, altfel returneaza
        -1)
        '''

        result = -1
        for ix, node in enumerate(graf_joc.noduri):
            dist = distanta_Euclid(node.punct_desenat, punct)
            if dist <= RAZA_CERC:
                result = ix

        return result

    def mutare_valida(graf_joc, configuratie_curenta, nod_curent, alt_nod):

        '''
        Functie care verifica daca o mutare este valida (valabila si pentru vulpe, si pentru gaste)
        Parte din cerinta 5.
        '''

        if graf_joc.muchii.get(nod_curent) != None:
            if alt_nod in graf_joc.muchii[nod_curent]:
                if (alt_nod not in configuratie_curenta.gaste) and (alt_nod != configuratie_curenta.vulpe):
                    return True

        return False

    def incarcare(self, ecran, graf_joc):
        pass


class Gaste(Jucator):
    '''
    Clasa care mosteneste clasa Jucator, si care va fi mostenita
    de clasele care controleaza gaste.
    '''

    def __init__(self):
        pass

    def configurari_posibile(graf_joc, configuratie_curenta):

        '''
        Genereaza toate mutarile posibile pentru jucatorul care controleaza cainii.
        Parte din cerinta 5.
        '''

        result = []
        for gasca in configuratie_curenta.gaste:
            for alt_nod in graf_joc.muchii[gasca]:
                if Jucator.mutare_valida(graf_joc, configuratie_curenta, gasca, alt_nod):
                    result.append(ConfiguratieJoc(graf_joc, inlocuire_valoare(configuratie_curenta.gaste, gasca, alt_nod),
                                                    configuratie_curenta.vulpe))

        return result

    def estimare(graf_joc, configuratie_anterioara, configuratie_curenta):

        '''
        Una din functiile de estimare. Aceasta functie este in favoarea gastelor.
        Nuumara cate gaste inconjoara vulpea.
        AI-urile pentru gastele se folosesc de aceasta functie de estimare.
        '''

        nr = 0
        for alt_nod in graf_joc.muchii[configuratie_curenta.vulpe]:
            if alt_nod in configuratie_curenta.gaste:
                nr = nr + 1

        return nr


class Vulpe(Jucator):
    '''
    Clasa care mosteneste clasa Jucator, si care va fi mostenita
    de clasele care controleaza vulpea.
    '''

    def __init__(self):
        '''
        avem o lista care tine nodurile selectate pentru a
        captura mai multi gaste (folosita de jucatorul uman)
        '''
        self.noduri_selectate = []

    def gasca_intre_noduri(graf_joc, nod_initial, nod_scop, nod_gasca):

        '''
        functie care verifica daca o gasca care se afla pe nodul nod_gasca se afla
        in linie dreapta intre nodurile nod_initial si nod_scop
        '''

        if nod_initial in graf_joc.muchii[nod_gasca] and nod_scop in graf_joc.muchii[nod_gasca]:
            vec1 = (graf_joc.noduri[nod_gasca].punct[0] - graf_joc.noduri[nod_initial].punct[0],
                    graf_joc.noduri[nod_gasca].punct[1] - graf_joc.noduri[nod_initial].punct[1])
            vec2 = (graf_joc.noduri[nod_scop].punct[0] - graf_joc.noduri[nod_gasca].punct[0],
                    graf_joc.noduri[nod_scop].punct[1] - graf_joc.noduri[nod_gasca].punct[1])
            if vec1 == vec2:
                return True

        return False

    def verificare_adaugare(curent, graf_joc, configuratie_curenta, alt_nod):

        '''
        functie care verifica daca un nod se poate adauga la lista in care
        se pastreaza nodurile prin care va trece vulpea in timp ce captureaza gastele

        '''

        ultimul_nod_plan = configuratie_curenta.vulpe
        if len(curent) != 0:
            ultimul_nod_plan = curent[-1]

        if ultimul_nod_plan == alt_nod:
            return False

        if alt_nod in configuratie_curenta.gaste:
            return False

        if alt_nod in curent:
            return False

        if alt_nod == configuratie_curenta.vulpe:
            return False

        for gasca in configuratie_curenta.gaste:
            if Vulpe.gasca_intre_noduri(graf_joc, ultimul_nod_plan, alt_nod, gasca):
                return True

        return False

    def configuration_after_move(noduri_selectate, graf_joc, configuratie_curenta):

        '''
        Functie care primeste lista cu succesiunea de noduri prin care face captura
        si returneaza o noua configuratie de board in urma executarii acelor capturi
        '''

        gaste_de_capturat = []

        for i in range(len(noduri_selectate)):
            nod_anterior = configuratie_curenta.vulpe
            if i != 0:
                nod_anterior = noduri_selectate[i - 1]
            numar_nod = noduri_selectate[i]

            for gasca in configuratie_curenta.gaste:
                if Vulpe.gasca_intre_noduri(graf_joc, nod_anterior, numar_nod, gasca):
                    gaste_de_capturat.append(gasca)

        configuratie_curenta = ConfiguratieJoc(graf_joc, [gasca for gasca in configuratie_curenta.gaste if
                                                               gasca not in gaste_de_capturat], noduri_selectate[-1])

        return configuratie_curenta

    def genereaza_posibile_capturi(solutii, graf_joc, configuratie_curenta, crt_solution, ultimul_nod):

        '''
        functie recursiva returneaza toate posibilitatile de liste
        de noduri care ar putea face parte dintr-o captura pornita din configuratia curenta
        '''

        if crt_solution != []:
            solutii.append(crt_solution)

        for alt_nod in range(len(graf_joc.noduri)):
            if Vulpe.verificare_adaugare(crt_solution, graf_joc, configuratie_curenta, alt_nod):
                solutie_noua = crt_solution.copy()
                solutie_noua.append(alt_nod)
                Vulpe.genereaza_posibile_capturi(solutii, graf_joc, configuratie_curenta, solutie_noua, alt_nod)

    def configurari_posibile(graf_joc, configuratie_curenta):

        '''
        functie care returneaza toate configuratiile de joc_pornit care pot rezulta prin mutarea jaguarului din
        configuratia curenta.
        Parte din cerinta 5.
        '''

        possible_noduri_selectates = []

        for other in graf_joc.muchii[configuratie_curenta.vulpe]:
            if Jucator.mutare_valida(graf_joc, configuratie_curenta, configuratie_curenta.vulpe, other):
                possible_noduri_selectates.append([other])

        Vulpe.genereaza_posibile_capturi(possible_noduri_selectates, graf_joc, configuratie_curenta, [],
                                            configuratie_curenta.vulpe)

        configuratii_posibile= [Vulpe.configuration_after_move(noduri_selectate, graf_joc, configuratie_curenta)
                                    for noduri_selectate in possible_noduri_selectates]

        return configuratii_posibile

    def estimare(graf_joc, configuratie_anterioara, configuratie_curenta):
        return len(configuratie_anterioara.gaste) - len(configuratie_curenta.gaste)


class Algortimi:
    '''
    clasa care contine algoritmii min_max si alpha-beta
    adaptati pentru jocul nostru
    '''

    def __init__(self):
        '''
        initializam nrer-ul pentru numarul de mutari cu 0
        '''
        self.numari_mutari = 0

    def transformare_in_adancime(dificultate):
        '''
        dificultatea este un numar intre 0 si 2, deci noi va trebui sa il
        transformam intr-o adancime pentru parcurgeri, si facem asta folosind
        formula urmatoare
        '''
        return 1 + (dificultate * 2)

    def min_max(graf_joc, configuratie_initiala, configuratie_curenta, este_maxim, este_vulpe, crt_level, maxim_nivele,
                functie_cost):

        '''
        algoritmul min_max. Pentru estimare se foloseste functia functie_cost trimisa ca argument.
        In functie de tipul de jucator (vulpe sau caini) se genereaza configuratii folosind functii diferite.
        '''

        configuratii_posibile= []
        if este_vulpe:
            configuratii_posibile= Vulpe.configurari_posibile(graf_joc, configuratie_curenta)
        else:
            configuratii_posibile= Gaste.configurari_posibile(graf_joc, configuratie_curenta)

        algoritmi.numari_mutari = algoritmi.numari_mutari + len(configuratii_posibile)

        if crt_level >= maxim_nivele - 1:
            sol = (None, -1)
            for configuratie_noua in configuratii_posibile:
                crt_cost = functie_cost(graf_joc, configuratie_initiala, configuratie_noua)
                if este_maxim:
                    if crt_cost > sol[1]:
                        sol = (configuratie_noua, crt_cost)
                else:
                    if sol[1] == -1 or crt_cost < sol[1]:
                        sol = (configuratie_noua, crt_cost)

            if sol[0] != None:
                return sol
            return (configuratie_curenta, 0)

        result = (None, -1)

        for configuratie_noua in configuratii_posibile:
            returned_val = Algortimi.min_max(graf_joc, configuratie_initiala, configuratie_noua, not este_maxim, not este_vulpe,
                                            crt_level + 1, maxim_nivele, functie_cost)
            if returned_val[0] != None:
                if este_maxim:
                    if result[1] < returned_val[1]:
                        result = (configuratie_noua, returned_val[1])
                else:
                    if result[1] == -1 or result[1] > returned_val[1]:
                        result = (configuratie_noua, returned_val[1])

        if result[0] != None:
            return result

        return (configuratie_curenta, 0)

    def alpha_beta(graf_joc, configuratie_initiala, configuratie_curenta, este_maxim, este_vulpe, crt_level, maxim_nivele,
                  functie_cost, alpha, beta):

        '''
        Algoritmul alpha-beta. Exact ca min_max, doar ca exista si optimizarea cu numerele
        alpha si beta.
        '''

        configuratii_posibile= []
        if este_vulpe:
            configuratii_posibile= Vulpe.configurari_posibile(graf_joc, configuratie_curenta)
        else:
            configuratii_posibile= Gaste.configurari_posibile(graf_joc, configuratie_curenta)

        algoritmi.numari_mutari = algoritmi.numari_mutari + len(configuratii_posibile)

        if crt_level >= maxim_nivele - 1:
            sol = (None, -1)
            for configuratie_noua in configuratii_posibile:
                crt_cost = functie_cost(graf_joc, configuratie_initiala, configuratie_noua)
                if este_maxim:
                    if crt_cost > sol[1]:
                        sol = (configuratie_noua, crt_cost)
                else:
                    if sol[1] == -1 or crt_cost < sol[1]:
                        sol = (configuratie_noua, crt_cost)
            if sol[0] != None:
                return sol
            return (configuratie_curenta, 0)

        if este_maxim:

            sol = (None, -1)
            for configuratie_noua in configuratii_posibile:
                returned_val = Algortimi.alpha_beta(graf_joc, configuratie_initiala, configuratie_noua, not este_maxim,
                                                  not este_vulpe, crt_level + 1, maxim_nivele, functie_cost, alpha, beta)

                if returned_val[0] != None:
                    if returned_val[1] > sol[1]:
                        sol = (configuratie_noua, returned_val[1])

                    alpha = max(alpha, returned_val[1])
                    if alpha >= beta:
                        break

            if sol[0] != None:
                return sol
        else:
            sol = (None, -1)
            for configuratie_noua in configuratii_posibile:
                returned_val = Algortimi.alpha_beta(graf_joc, configuratie_initiala, configuratie_noua, not este_maxim,
                                                  not este_vulpe, crt_level + 1, maxim_nivele, functie_cost, alpha, beta)

                if returned_val[0] != None:
                    if returned_val[1] < sol[1] or sol[1] == -1:
                        sol = (configuratie_noua, returned_val[1])

                    beta = min(beta, returned_val[1])
                    if beta <= alpha:
                        break

            if sol[0] != None:
                return sol

        return (configuratie_curenta, 0)


class MMGaste(Gaste):
    '''
    clasa pentru jucatorul de gaste care foloseste min_max
    '''

    def __init__(self, dificultate):
        '''
        cand se creaza jucatorul trebuie sa ii stim dificultatea
        cu care o sa joace
        '''
        self.dificultate = dificultate

    def muta(self, graf_joc, configuratie_curenta):
        '''
        Face o mutare folosind algoritmul min_max pentru a determina mutarea.
        Se afiseaza pe ecran informatiile cerute.
        '''
        algoritmi.numari_mutari = 0
        result = Algortimi.min_max(graf_joc, configuratie_curenta, configuratie_curenta, True, False, 0,
                                  Algortimi.transformare_in_adancime(self.dificultate), Gaste.estimare)
        print("Estimare: " + str(result[1]))
        print("Noduri Generate: " + str(algoritmi.numari_mutari))
        return (result[0], algoritmi.numari_mutari)


class ABGaste(Gaste):
    '''
    clasa pentru jucatorul de caini care foloseste alpha-beta
    '''

    def __init__(self, dificultate):
        '''
        cand se creaza jucatorul trebuie sa ii stim dificultatea
        cu care o sa joace
        '''
        self.dificultate = dificultate

    def muta(self, graf_joc, configuratie_curenta):
        '''
        Face o mutare folosind algoritmul alpha-beta pentru a determina mutarea.
        Se afiseaza pe ecran informatiile cerute.
        '''
        algoritmi.numari_mutari = 0
        result = Algortimi.alpha_beta(graf_joc, configuratie_curenta, configuratie_curenta, True, False, 0,
                                    Algortimi.transformare_in_adancime(self.dificultate), Gaste.estimare,
                                    -sys.maxsize, sys.maxsize)
        print("Estimare: " + str(result[1]))
        print("Noduri Generate: " + str(algoritmi.numari_mutari))
        return (result[0], algoritmi.numari_mutari)


class OmGaste(Gaste):
    '''
    clasa pentru jucatorul uman care controleaza caini.
    '''

    def __init__(self):
        '''
        vom tine minte ultimul caine selectat, pentru ca
        vom face mutarea folosind acel caine
        '''
        self.gasca_selectata = -1

    def muta(self, graf_joc, configuratie_curenta):

        '''
        functia care face o mutare in functie de ce apasa utlizatorul (este
        posibil sa fie apelata de mai multe ori in update pana sa se faca
        o mutare, deoarece depinde de Jucator, nu de calculator, nu stim cand
        se va decide). Se asteapta selectarea unui caine, dupa care se face mutarea
        aleasa daca este valida (se poate schimba cainele).
        '''

        if mouse_input.eliberat:
            index_nod = self.returneaza_nod_apasat(graf_joc, pygame.mouse.get_pos())

            if index_nod != -1:

                if index_nod in configuratie_curenta.gaste:
                    self.gasca_selectata = index_nod
                elif self.gasca_selectata != -1:
                    if Jucator.mutare_valida(graf_joc, configuratie_curenta, self.gasca_selectata, index_nod):
                        configuratie_curenta = ConfiguratieJoc(graf_joc,
                                                                  inlocuire_valoare(configuratie_curenta.gaste, self.gasca_selectata,
                                                                          index_nod), configuratie_curenta.vulpe)
                        self.gasca_selectata = -1

        return (configuratie_curenta, 0)

    def incarcare(self, ecran, graf_joc):

        '''
        daca este o gasca selectata, aceasta va fi desenata cu verde.
        '''

        if self.gasca_selectata != -1:
            pygame.draw.circle(ecran, (0, 255, 0), graf_joc.noduri[self.gasca_selectata].punct_desenat, RAZA_CERC)
            pygame.draw.circle(ecran, (0, 0, 0), graf_joc.noduri[self.gasca_selectata].punct_desenat, RAZA_CERC, 5)


class MMVulpe(Vulpe):
    '''
    clasa pentru jucatorul vulpe care foloseste min_max
    '''

    def __init__(self, dificultate):
        '''
        cand se creaza jucatorul trebuie sa ii stim dificultatea
        cu care o sa joace
        '''
        super().__init__()
        self.dificultate = dificultate

    def muta(self, graf_joc, configuratie_curenta):
        '''
        Face o mutare folosind algoritmul min_max pentru a determina mutarea.
        Se afiseaza pe ecran informatiile cerute.
        '''
        algoritmi.numari_mutari = 0
        result = Algortimi.min_max(graf_joc, configuratie_curenta, configuratie_curenta, True, True, 0,
                                  Algortimi.transformare_in_adancime(self.dificultate), Vulpe.estimare)
        print("Estimare: " + str(result[1]))
        print("Noduri Generate: " + str(algoritmi.numari_mutari))
        return (result[0], algoritmi.numari_mutari)


class ABVulpe(Vulpe):
    '''
    clasa pentru jucatorul vulpe care foloseste alpha-beta
    '''

    def __init__(self, dificultate):
        '''
        cand se creaza jucatorul trebuie sa ii stim dificultatea
        cu care o sa joace
        '''
        super().__init__()
        self.dificultate = dificultate

    def muta(self, graf_joc, configuratie_curenta):
        '''
        Face o mutare folosind algoritmul alpha-beta pentru a determina mutarea.
        Se afiseaza pe ecran informatiile cerute.
        '''
        algoritmi.numari_mutari = 0
        result = Algortimi.alpha_beta(graf_joc, configuratie_curenta, configuratie_curenta, True, True, 0,
                                    Algortimi.transformare_in_adancime(self.dificultate), Vulpe.estimare,
                                    -sys.maxsize, sys.maxsize)
        print("Estimare: " + str(result[1]))
        print("Noduri Generate: " + str(algoritmi.numari_mutari))
        return (result[0], algoritmi.numari_mutari)


class OmVulpe(Vulpe):
    '''
    clasa pentru jucatorul uman de vulpe
    '''

    def __init__(self):
        '''
        ne intereseaza sa avem o lista de capturi posibile creata
        '''
        super().__init__()

    def muta(self, graf_joc, configuratie_curenta):

        '''
        Metoda prin care jucatorul uman este pentru gaste.
        Trates si capturile multiple
        Se fac toate verificarile
        '''

        if mouse_input.eliberat:
            index_nod = self.returneaza_nod_apasat(graf_joc, pygame.mouse.get_pos())
            if index_nod != -1:
                if len(self.noduri_selectate) == 0:
                    if Vulpe.verificare_adaugare(self.noduri_selectate, graf_joc, configuratie_curenta, index_nod):
                        self.noduri_selectate.append(index_nod)
                        
                    elif Jucator.mutare_valida(graf_joc, configuratie_curenta, configuratie_curenta.vulpe,
                                                index_nod):
                        configuratie_curenta = ConfiguratieJoc(graf_joc, configuratie_curenta.gaste, index_nod)
                else:
                    if Vulpe.verificare_adaugare(self.noduri_selectate, graf_joc, configuratie_curenta, index_nod):
                        self.noduri_selectate.append(index_nod)
                    else:
                        configuratie_curenta = Vulpe.configuration_after_move(self.noduri_selectate, graf_joc,
                                                                                      configuratie_curenta)
                        self.noduri_selectate = []

        return (configuratie_curenta, 0)

    def incarcare(self, ecran, graf_joc):

        '''
        deseneaza nodurile din planul de captura cu verde
        '''

        for node in self.noduri_selectate:
            pygame.draw.circle(ecran, (0, 255, 0), graf_joc.noduri[node].punct_desenat, RAZA_CERC)


class Joc:
    '''
    Functionare joc si meniu -> apel catre diverse
    '''

    def __init__(self, ui_manager):

        '''
        pregateste jocul si meniul
        '''

        self.joc_pornit = 0 # am inceput jocul propriu-zis sau sunt inca in menu

        # cu ce a ales sa joace userul/ userii
        self.alegere_gaste = "om"
        self.alegere_vulpe = "om"
        
        self.gaste_dificultate = 0 
        self.vulpe_dificultate = 0

        self.font_marime_text = pygame.font.SysFont('arial.ttf', 60)
        
        self.meniu(ui_manager)
    
    def meniu(self, ui_manager):

        '''
        Metoda care creaza butoanele din meniu
        '''

        # --------------------- Butoane Gaste -------------- #
        self.text_gasca = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((110, 130), (200, 40)), # (pozitie fata de marginea din stanga), (dimensiune caseta)
            text="GASTE",
            manager=ui_manager)

        self.buton_om_gaste = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((115, 180), (180, 40)),
            text='OM',
            manager=ui_manager)

        self.buton_min_max_gasca = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((115, 230), (180, 40)),
            text='Calculator Min-Max',
            manager=ui_manager)

        self.buton_alpha_beta_gasca = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((115, 280), (180, 40)),
            text='Calculator Alpha-Beta',
            manager=ui_manager)

        self.text_dificultate_gasca = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((140, 330), (130, 40)),
            text="Dificultate",
            manager=ui_manager)

        self.dificultate_gaste_1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((140, 380), (130, 40)),
            text='Usor',
            manager=ui_manager)

        self.dificultate_gaste_2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((140, 430), (130, 40)),
            text='Mediu',
            manager=ui_manager)

        self.dificultate_gaste_3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((140, 480), (130, 40)),
            text='Greu',
            manager=ui_manager)

        # ---------------------Sfarsit Butoane Gaste -------------- #

        # --------------------- Butoane Vulpe -------------- #
        self.text_vulpe = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((310, 130), (200, 40)),
            text="VULPE",
            manager=ui_manager)

        self.buton_om_vulpe = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((315, 180), (180, 40)),
            text='OM',
            manager=ui_manager)

        self.buton_min_max_vulpe = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((315, 230), (180, 40)),
            text='Calculator Min-Max',
            manager=ui_manager)

        self.buton_alpha_beta_vulpe = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((315, 280), (180, 40)),
            text='Calculator Alpha-Beta',
            manager=ui_manager)

        self.vulpe_dificultate_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((340, 330), (130, 40)),
            text="Dificultate",
            manager=ui_manager)

        self.dificultate_vulpe_1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((340, 380), (130, 40)),
            text='Usor',
            manager=ui_manager)

        self.dificultate_vulpe_2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((340, 430), (130, 40)),
            text='Mediu',
            manager=ui_manager)

        self.dificultate_vulpe_3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((340, 480), (130, 40)),
            text='Greu',
            manager=ui_manager)

        self.buton_de_start = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 530), (300, 50)),
            text='JOACA',
            manager=ui_manager)

        # --------------------- Sfarsit Butoane Vulpe -------------- #

        # selectare by default
        self.buton_om_gaste.select()
        self.buton_om_vulpe.select()
        self.dificultate_gaste_1.select()
        self.dificultate_vulpe_1.select()
    
    def apasare_butoane_meniu(self, eveniment):

        '''
        Metoda care verifica toate butoanele daca au fost apasate
        Si actioneaza pe cele selectate
         
        '''

        if eveniment.type == pygame.USEREVENT:
            
            if eveniment.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # ------------ Pentru Gaste ----------------------
                if eveniment.ui_element == self.buton_om_gaste:
                    self.buton_om_gaste.select() # selectez
                    
                    self.buton_min_max_gasca.unselect()
                    self.buton_alpha_beta_gasca.unselect()
                    
                    self.alegere_gaste = "om"

                elif eveniment.ui_element == self.buton_min_max_gasca:
                    self.buton_min_max_gasca.select()

                    self.buton_om_gaste.unselect()
                    self.buton_alpha_beta_gasca.unselect()
                    
                    self.alegere_gaste = "mm"

                elif eveniment.ui_element == self.buton_alpha_beta_gasca:
                    self.buton_alpha_beta_gasca.select()
                    
                    self.buton_om_gaste.unselect()
                    self.buton_min_max_gasca.unselect()
                   
                    self.alegere_gaste = "ab"
                    
                elif eveniment.ui_element == self.dificultate_gaste_1:
                    self.dificultate_gaste_1.select()

                    self.dificultate_gaste_2.unselect()
                    self.dificultate_gaste_3.unselect()
                    
                    self.gaste_dificultate = 0

                elif eveniment.ui_element == self.dificultate_gaste_2:
                    self.dificultate_gaste_2.select()
                    
                    self.dificultate_gaste_1.unselect()
                    self.dificultate_gaste_3.unselect()
                    
                    self.gaste_dificultate = 1

                elif eveniment.ui_element == self.dificultate_gaste_3:
                    self.dificultate_gaste_3.select()
                    
                    self.dificultate_gaste_1.unselect()
                    self.dificultate_gaste_2.unselect()
                  
                    self.gaste_dificultate = 2

                # ------------ Pentru Vulpe ----------------------
                
                elif eveniment.ui_element == self.buton_om_vulpe:
                    self.buton_om_vulpe.select()
                    
                    self.buton_min_max_vulpe.unselect()
                    self.buton_alpha_beta_vulpe.unselect()
                    
                    self.alegere_vulpe = "om"

                elif eveniment.ui_element == self.buton_min_max_vulpe:
                    self.buton_min_max_vulpe.select()
                    
                    self.buton_om_vulpe.unselect()
                    self.buton_alpha_beta_vulpe.unselect()
                    
                    self.alegere_vulpe = "mm"

                elif eveniment.ui_element == self.buton_alpha_beta_vulpe:
                    self.buton_alpha_beta_vulpe.select()
                    
                    self.buton_om_vulpe.unselect()
                    self.buton_min_max_vulpe.unselect()
                    
                    self.alegere_vulpe = "ab"

                elif eveniment.ui_element == self.dificultate_vulpe_1:
                    self.dificultate_vulpe_1.select()
                    
                    self.dificultate_vulpe_2.unselect()
                    self.dificultate_vulpe_3.unselect()
                    
                    self.vulpe_dificultate = 0

                elif eveniment.ui_element == self.dificultate_vulpe_2:
                    self.dificultate_vulpe_2.select()
                    
                    self.dificultate_vulpe_1.unselect()
                    self.dificultate_vulpe_3.unselect()
                    
                    self.vulpe_dificultate = 1

                elif eveniment.ui_element == self.dificultate_vulpe_3:
                    self.dificultate_vulpe_3.select()
                    
                    self.dificultate_vulpe_1.unselect()
                    self.dificultate_vulpe_2.unselect()
                    
                    self.vulpe_dificultate = 2

                # ---------------- Pentru butonul de start ---------------
                elif eveniment.ui_element == self.buton_de_start:

                    self.graf_joc = TablaDeJoc()
                    self.configuratie_curenta = ConfiguratieJoc(self.graf_joc)
                    self.configuratie_curenta.afisare_consola(self.graf_joc)

                    self.joc_pornit = 1

                    if self.alegere_gaste == "om":
                        self.jucator_gasca = OmGaste()
                    elif self.alegere_gaste == "mm":
                        self.jucator_gasca = MMGaste(self.gaste_dificultate)
                    elif self.alegere_gaste == "ab":
                        self.jucator_gasca = ABGaste(self.gaste_dificultate)

                    if self.alegere_vulpe == "om":
                        self.jucator_vulpe = OmVulpe()
                    elif self.alegere_vulpe == "mm":
                        self.jucator_vulpe = MMVulpe(self.vulpe_dificultate)
                    elif self.alegere_vulpe == "ab":
                        self.jucator_vulpe = ABVulpe(self.vulpe_dificultate)

                    self.jucator_curent = self.jucator_vulpe

                    self.gaste_timp_de_gandire = []
                    self.vulpe_timp_de_gandire = []
                    self.gaste_noduri_generate = []
                    self.vulpe_noduri_generate = []

                    self.ultimul_timp_de_gandire = time.time()
                    self.timp_start = time.time()
                    self.timpi_afisare = False
                    self.jocul_este_pornit = True

    def update(self):

        '''
        Se apeleaza la fiecare frame
        Aici este apelata functia care decide ce mutare se va face mai departe.
        La sfarsitul jocului se afiseaza in consola informatiile cerute.
        '''

        if self.joc_pornit == 1: # este in timpul jocului

            current_winner = self.configuratie_curenta.gaseste_castigator(self.graf_joc)
            mouse_input.update()

            if current_winner == -1 and self.jocul_este_pornit:

                configuratie_noua, generated_noduri = self.jucator_curent.muta(self.graf_joc, self.configuratie_curenta)
                
                if configuratie_noua != self.configuratie_curenta:

                    current_time = time.time()
                    diferenta_timp = current_time - self.ultimul_timp_de_gandire

                    self.ultimul_timp_de_gandire = current_time

                    configuratie_noua.afisare_consola(self.graf_joc)

                    print("Timpul de gandire: " + str(diferenta_timp))

                    if self.jucator_gasca == self.jucator_curent:
                        self.jucator_curent = self.jucator_vulpe

                        self.gaste_timp_de_gandire.append(diferenta_timp)
                        self.gaste_noduri_generate.append(generated_noduri)

                    else:
                        self.jucator_curent = self.jucator_gasca

                        self.vulpe_timp_de_gandire.append(diferenta_timp)
                        self.vulpe_noduri_generate.append(generated_noduri)

                    self.configuratie_curenta = configuratie_noua

            elif not self.timpi_afisare:

                    if len(self.vulpe_timp_de_gandire) > 0 and len(self.gaste_timp_de_gandire) > 0:
                        print("----Timpi de gandire pentru gaste-------")
                        print("Minim: " + str(min(self.gaste_timp_de_gandire)))
                        print("Maxim: " + str(max(self.gaste_timp_de_gandire)))
                        print("Medie: " + str(sum(self.gaste_timp_de_gandire) / len(self.gaste_timp_de_gandire)))
                        sorted(self.gaste_timp_de_gandire)
                        print("Mediana: " + str(self.gaste_timp_de_gandire[int(len(self.gaste_timp_de_gandire) / 2)]))

                        print("--------------------------------------------------------------")

                        print("------Timpi de gandire pentru vulpe-----")
                        print("Minim: " + str(min(self.vulpe_timp_de_gandire)))
                        print("Maxim: " + str(max(self.vulpe_timp_de_gandire)))
                        print("Medie: " + str(sum(self.vulpe_timp_de_gandire) / len(self.vulpe_timp_de_gandire)))
                        sorted(self.vulpe_timp_de_gandire)
                        print("Mediana: " + str(self.vulpe_timp_de_gandire[int(len(self.vulpe_timp_de_gandire) / 2)]))

                        print("--------------------------------------------------------------")

                        print("-----Noduri generate gaste-----")
                        print("Minim: " + str(min(self.gaste_noduri_generate)))
                        print("Maxim: " + str(max(self.gaste_noduri_generate)))
                        print("Medie: " + str(sum(self.gaste_noduri_generate) / len(self.gaste_noduri_generate)))
                        sorted(self.gaste_noduri_generate)
                        print("Mediana: " + str(self.gaste_noduri_generate[int(len(self.gaste_noduri_generate) / 2)]))

                        print("--------------------------------------------------------------")

                        print("-----Noduri generate vulpe-----")
                        print("Minim: " + str(min(self.vulpe_noduri_generate)))
                        print("Maxim: " + str(max(self.vulpe_noduri_generate)))
                        print("Medie: " + str(sum(self.vulpe_noduri_generate) / len(self.vulpe_noduri_generate)))
                        sorted(self.vulpe_noduri_generate)
                        print("Mediana: " + str(self.vulpe_noduri_generate[int(len(self.vulpe_noduri_generate) / 2)]))

                        print("--------------------------------------------------------------")

                        print("Timpul jocului: " + str(time.time() - self.timp_start))
                        print("Numar mutari gaste: " + str(len(self.gaste_timp_de_gandire)))
                        print("Numar mutari vulpe: " + str(len(self.vulpe_timp_de_gandire)))

                        self.timpi_afisare = True

                    if mouse_input.eliberat or (not self.jocul_este_pornit):
                        self.joc_pornit = 0

    def incarcare(self, ecran):

        '''
        Metoda care deseneaza pe ecran toate lucrurile cerute 
        '''

        if self.joc_pornit == 1:

            if self.jucator_curent == self.jucator_vulpe:
               mesaj = "Randul vulpii"
            else:
                mesaj = "Randul gastelor"

            castigator = self.configuratie_curenta.gaseste_castigator(self.graf_joc)

            if castigator != -1:
                text_rezultat_joc = "Gastele au castigat !"

                if castigator == 1:
                    text_rezultat_joc = "Vulpea a castigat !"

                afisare_mesaj = self.font_marime_text.render(text_rezultat_joc, False, (10, 123, 0))
                ecran.blit(afisare_mesaj, (170, 600))

            afisare_mesaj = self.font_marime_text.render(mesaj, False, (10, 123, 0))
            ecran.blit(afisare_mesaj, (170, 50))

            self.graf_joc.desenare_tabla_joc(ecran)
            self.configuratie_curenta.incarcare(ecran, self.graf_joc)
            self.jucator_curent.incarcare(ecran, self.graf_joc)


def start():
    pornit = True

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Dima Oana-Teodora Vulpi si Gaste')

    ecran = pygame.display.set_mode([LUNGIME, INALTIME])
    ui_manager = pygame_gui.UIManager((LUNGIME, INALTIME))
    timp = pygame.time.Clock()
    jocul_propriuzis = Joc(ui_manager)

    while pornit:

        t = timp.tick(60) / 1000.0 # tick -> updatare ceas
        ecran.fill((242, 170, 87))  # culoare ecran

        for eveniment in pygame.event.get():

            if eveniment.type == pygame.QUIT: # daca am ales sa inchid din X
                pornit = False

            if jocul_propriuzis.joc_pornit == 0: # nu am apasat butonul de start
                jocul_propriuzis.apasare_butoane_meniu(eveniment)
                ui_manager.process_events(eveniment) # metoda din pygame care proceseaza eventurile de input si da un raspuns

        if jocul_propriuzis.joc_pornit == 0: # nu am apasat butonul de start
            ui_manager.update(t) # metoda din pygame care proceseaza eventurile de input si da un raspuns

        jocul_propriuzis.update()
        jocul_propriuzis.incarcare(ecran)

        if jocul_propriuzis.joc_pornit == 0:
            ui_manager.draw_ui(ecran)

        pygame.display.flip()

    pygame.quit()
# intializari
algoritmi = Algortimi()
mouse_input = MouseInput()

# constante
LUNGIME = 600
INALTIME = 700

MARGINI = 80

RAZA_CERC = 20

# pornire joc_pornit
start()
