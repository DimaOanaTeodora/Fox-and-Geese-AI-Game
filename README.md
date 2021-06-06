# Vulpi si Gaste
[Link cerinta joc](http://www.irinaciocan.ro/inteligenta_artificiala/tema-jocuri.php)

[Link joc online](http://www.onlinesologames.com/fox-and-geese)

##  Meniu cu mai multe butoane
<p align="center">
<img src="https://github.com/DimaOanaTeodora/Homework-2-KR-AI/blob/main/Menu.JPG" width="500" height="600">
</p>

- Selectare default jucator vs calculator : Gaste vs Calculator Min-Max
- Utilizatorul poate alege ce algoritm doreste sa foloseasca (Min-Max sau Alpha-Beta)
- Utilizatorul poate sa aleaga daca joaca de partea vulpii sau a gastelor
- Prin utilizarea meniului utilizatorul nu poate raspunde gresit
- Utilizatorul poate alege din 3 nivele de dificultate
  - Fiecare nivel corespunde unei adancimi a arborelui calculata prin formula ``` 1 + 2 * dificultate```

## Tabla de joc
<p align="center">
<img src="https://github.com/DimaOanaTeodora/Homework-2-KR-AI/blob/main/Joc.JPG" width="500" height="600">
</p>

- Interfata grafica PyGame
```python
    def desenare_tabla_joc(self, ecran):
        for i in range(len(self.noduri)):
            for muchie in self.muchii[i]:
                pozitia1 = self.noduri[i].punct_desenat
                pozitia2 = self.noduri[muchie].punct_desenat

                # desenare linie dintre doua puncte
                pygame.draw.line(ecran, (0, 0, 0), pozitia1, pozitia2, 2)
```
- Afisarea a cui este rândul să mute.
- Indicarea, la finalul jocului, a câstigatorului
- Generarea si afisarea starii initiale de joc: 13 gaste si o vulpe
- Generarea si afisarea starilor intermediare de joc
- Mutare utilizator prin eveniment in interfata grafica (click mouse)
  - clasa utilitara pentru controlul inputului de mouse: MouseInput ( constructor + metoda update(self))
  - Verificata si corectitudinea mutarilor utilizatorului prin apelul functiei:
  ```python
  returneaza_nod_apasat(tabla_de_joc, pygame.mouse.get_pos())
  # daca nodul nu exista returneaza -1
  ```

## Afisare + debugging in consola
<p align="center">
<img src="https://github.com/DimaOanaTeodora/Homework-2-KR-AI/blob/main/Consola.JPG" width="500" height="500">
</p>

- Afisare in consola tabela de joc
```python
    def afisare_consola(self, tabla_de_joc):
        for x in range(8):
            for y in range(8):
                if tabla_de_joc.numar_nod_in_grafic.get((x, y)) != None:

                    # accesez valoarea din dictionarul numar_nod_in_grafic
                    numar_nod = tabla_de_joc.numar_nod_in_grafic[(x, y)]

                    if numar_nod in self.gaste:
                        print("G ", end="")
                    elif numar_nod == self.vulpe:
                        print("V ", end="")
                    else:
                        print("# ", end="")
                else:
                    print("  ", end="")

            print("\n", end="")
```
- Afisarea timpului de gandire, dupa fiecare mutare
  - Pentru timpul de găndire al calculatorului: afișarea la final a timpului minim, maxim, mediu și a medianei.
```python
 def update(self): # din clas Joc
```
- Afișarea estimărilor date si numărului de noduri generate de minimax și alpha-beta ( functiile muta din clase)
- La final se va afișa numărul minim, maxim, mediu și mediana pentru numarul de noduri generat pentru fiecare mutare
- Afisarea timpului final de joc (cat a rulat programul) si a numarului total de mutari



## Cerinte suplimentare
- Titlul ferestrei de joc
```python
pygame.display.set_caption('Dima Oana-Teodora Vulpi si Gaste')
```
- Functia de generare succesorilor
```python
    def genereaza_posibile_capturi(solutii, tabla_de_joc, configuratie_curenta, solutie_actuala):
        """
        Recrusivitate
        """
        if solutie_actuala != []: # adauga la lista noile noduri
            solutii.append(solutie_actuala)

        for alt_nod in range(len(tabla_de_joc.noduri)):
            if verificare_adaugare(solutie_actuala, tabla_de_joc, configuratie_curenta, alt_nod):
                solutie_noua = solutie_actuala.copy()
                solutie_noua.append(alt_nod)

                # apel recrusiv
                Vulpe.genereaza_posibile_capturi(solutii, tabla_de_joc, configuratie_curenta, solutie_noua)
```
- functie de testare a validitatii unei mutari (folosita si pentru a verifica mutarea utilizatorului)
```python
def mutare_valida(tabla_de_joc, configuratie_curenta, nr_nod_curent, nr_alt_nod):
    lista_muchii = tabla_de_joc.muchii[nr_nod_curent]

    if nr_alt_nod in lista_muchii:
        if (nr_alt_nod not in configuratie_curenta.gaste) and (nr_alt_nod != configuratie_curenta.vulpe):
            return True

    return False
```

- Functia de stabilire a castigatorului
```python
 def gaseste_castigator(self, tabla_de_joc):
        # calculez miscarile posibile ale vulpii
        configurari_vulpe = Vulpe.configurari_posibile(tabla_de_joc, self)

        if len(configurari_vulpe) == 0:  # daca vulpea nu mai are miscari, gastele castiga
            return "castiga gastele"

        if len(self.gaste) <= 4:  # daca gastele raman mai putine de 4 atunci vulpea castiga
            return "castiga vulpea"

        return "configuratie nefinala"  # nu am configuratie finala
```

- Doua moduri diferite de estimare a scorului (pentru stari care nu sunt inca finale)
```pyton
def estimare_gaste(tabla_de_joc, configuratie_curenta, dummy): # in favoarea gastelor
def estimare_vulpe(tabla_de_joc, configuratie_anterioara, configuratie_curenta): # in favoarea vulpii
```


(5%) La fiecare mutare utilizatorul sa poata si sa opreasca jocul daca vrea,  
 caz in care se vor afisa toate informațiile cerute pentru finalul jocului ( scorul lui si al calculatorului,numărul minim, maxim, mediu și mediana pentru numarul de noduri generat pentru fiecare mutare, timpul final de joc și a numarului total de mutari atat pentru jucator cat si pentru calculator)  
 Punctajul pentru calcularea efectivă a acestor date e cel de mai sus; aici se punctează strict afișarea lor în cazul cerut.
(5%) Comentarii.  
Explicarea algoritmului de generare a mutarilor, explicarea estimarii scorului si dovedirea faptului ca ordoneaza starile cu adevarat in functie de cat de prielnice ii sunt lui MAX (nu trebuie demonstratie matematica, doar explicat clar). Explicarea pe scurt a fiecarei functii si a parametrilor.

Bonus (10%). Ordonarea succesorilor înainte de expandare (bazat pe estimare) astfel încât alpha-beta să taie cât mai mult din arbore.
Bonus (20%). Opțiuni în meniu (cu butoane adăugate) cu:
Jucator vs jucător
Jucător vs calculator (selectată default)
Calculator (cu prima funcție de estimare) vs calculator (cu a doua funcție de estimare)
