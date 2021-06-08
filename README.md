# Vulpi si Gaste ( :fox_face: vs :duck: )
[Link cerinta joc](http://www.irinaciocan.ro/inteligenta_artificiala/tema-jocuri.php)

[Link joc online](http://www.onlinesologames.com/fox-and-geese)

##  Meniu cu mai multe butoane
<p align="center">
<img src="https://github.com/DimaOanaTeodora/Homework-2-KR-AI/blob/main/Menu.JPG" width="500" height="600">
</p>

:chart: Posibilitate de selectare a celor 3 optiuni: Jucator vs Jucator, Jucator vs Calculator, Calculator(estimare gaste) vs Calculator(estimare vulpe)

:chart: Selectare default Jucator vs Calculator : Gaste vs Calculator Min-Max

:chart: Utilizatorul poate alege ce algoritm doreste sa foloseasca (Min-Max sau Alpha-Beta)

:chart: Utilizatorul poate sa aleaga daca joaca de partea vulpii sau a gastelor

:chart: Prin utilizarea meniului utilizatorul nu poate raspunde gresit

:chart: Utilizatorul poate alege din 3 nivele de dificultate

  :chart: Fiecare nivel corespunde unei adancimi a arborelui calculata prin formula ``` 1 + 2 * dificultate``` ( pt niv Usor => adancime = 1, pt niv Mediu => adancime=3, pt niv Greu => adancime =5 )

## Tabla de joc
<p align="center">
<img src="https://github.com/DimaOanaTeodora/Homework-2-KR-AI/blob/main/Joc.JPG" width="500" height="600">
</p>


:chart: Interfata grafica PyGame

```python
    def desenare_tabla_joc(self, ecran):
        for i in range(len(self.noduri)):
            for muchie in self.muchii[i]:
                pozitia1 = self.noduri[i].punct_desenat
                pozitia2 = self.noduri[muchie].punct_desenat

                # desenare linie dintre doua puncte
                pygame.draw.line(ecran, (0, 0, 0), pozitia1, pozitia2, 2)
```

:chart: Afisarea a cui este rândul să mute.


:chart: Indicarea, la finalul jocului, a câstigatorului


:chart: Generarea si afisarea starii initiale de joc: 13 gaste si o vulpe


:chart: Generarea si afisarea starilor intermediare de joc


:chart: Mutare utilizator prin eveniment in interfata grafica (click mouse)

  :chart: clasa utilitara pentru controlul inputului de mouse: MouseInput ( constructor + metoda update(self))

  :chart: Verificata si corectitudinea mutarilor utilizatorului prin apelul functiei:

  ```python
  returneaza_nod_apasat(tabla_de_joc, pygame.mouse.get_pos())
  # daca nodul nu exista returneaza -1
  ```

## Afisare + debugging in consola
<p align="center">
<img src="https://github.com/DimaOanaTeodora/Homework-2-KR-AI/blob/main/Consola.JPG" width="500" height="500">
</p>


:chart: Afisare in consola tabela de joc

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

:chart: Afisarea timpului de gandire, dupa fiecare mutare

  :chart: Pentru timpul de găndire al calculatorului: afișarea la final a timpului minim, maxim, mediu și a medianei.

```python
 def update(self): # din clas Joc
```

:chart: Afișarea estimărilor date si numărului de noduri generate de minimax și alpha-beta ( functiile muta din clase)


:chart: La final se va afișa numărul minim, maxim, mediu și mediana pentru numarul de noduri generat pentru fiecare mutare


:chart: Afisarea timpului final de joc (cat a rulat programul) si a numarului total de mutari


:chart: Utilizatorul poate sa opreasca jocul cand vrea si sa afiseze analiza timpilor si a mutarilor in consola folosind tasta ESCAPE care il va intoarce in meniul principal


## Cerinte suplimentare

:chart: Titlul ferestrei de joc

```python
pygame.display.set_caption('Dima Oana-Teodora Vulpi si Gaste')
```

:chart: Functia de generare succesorilor

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

:chart: Functie de testare a validitatii unei mutari (folosita si pentru a verifica mutarea utilizatorului)

```python
def mutare_valida(tabla_de_joc, configuratie_curenta, nr_nod_curent, nr_alt_nod):
    lista_muchii = tabla_de_joc.muchii[nr_nod_curent]

    if nr_alt_nod in lista_muchii:
        if (nr_alt_nod not in configuratie_curenta.gaste) and (nr_alt_nod != configuratie_curenta.vulpe):
            return True

    return False
```


:chart: Functia de stabilire a castigatorului

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


:chart: Doua moduri diferite de estimare a scorului (pentru stari care nu sunt inca finale)

```pyton
def estimare_gaste(tabla_de_joc, configuratie_curenta, dummy): # in favoarea gastelor
def estimare_vulpe(tabla_de_joc, configuratie_anterioara, configuratie_curenta): # in favoarea vulpii
```

:chart: Comentarii


:chart: Explicarea pe scurt a fiecarei functii si a parametrilor: Python DocStrings


:chart: Ordonarea succesorilor înainte de expandare (bazat pe estimare) astfel încât alpha-beta să taie cât mai mult din arbore.

```python
configuratii_posibile = sorted(configuratii_posibile, key=lambda t: functie_estimare(tabla_de_joc, t, t))
```

:chart: Algoritmului de generare a mutarilor

Fiecare din cele 4 clase care apeleaza algoritmii de Min-Max sau Alpha-Beta, au o metoda prin care returneaza configuratiile urmatoare posibile generate in urma aplicarii unuia din cei 2 algoritmi.
```python
 def muta(self, tabla_de_joc, configuratie_curenta)
```

:chart: Estimarea scorului

Se face prin 2 metode.

:fox_face: Clasa Vulpe
```python
    def estimare_vulpe(tabla_de_joc, configuratie_anterioara, configuratie_curenta):
        return len(configuratie_anterioara.gaste) - len(configuratie_curenta.gaste)
```
Returneaza diferenta care reprezinta cate gaste a mancat vulpea de la ultima mutare in joc.

:duck: Clasa Gaste
```python
    def estimare_gaste(tabla_de_joc, configuratie_curenta, dummy):
        nr_gaste = 0

        for nr_alt_nod in tabla_de_joc.muchii[configuratie_curenta.vulpe]:
            if nr_alt_nod in configuratie_curenta.gaste:
                nr_gaste += 1

        return nr_gaste
```
Returneaza nr de gaste care inconjoara vulpea in configuratia curenta.