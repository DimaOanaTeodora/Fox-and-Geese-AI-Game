###  MouseInput
- clasa utila pt input mouse

### NodGraf
- coordonatele matrice si desenTabldeJoc

### TabalDeJoc
- generare tabla + desen

### ConfiguratieJoc
- o stare a jocului
- self.gaste + self.vulpe
- gastele si vulpea (lista de numere + numarul)
- castigatorul (daca exista) pt configuratia curenta
- afisare in consola configuratie curenta
- desenare cercuri pt gaste si vulpe

### Joc
- functionare joc si meniu
- calcul timpi de gandire si noduri generate
- initializare jucatori, meniu, font text
- grafica butoane meniu
- apasare butoane meniu in functie de un eveniment
- afisare randuri / castigator
- apelare la fiecare frame functia de update:
  - cauta gasticatorul din configuratia curenta
  - daca nu gaseste genereaza urmatoare condiguratie
  - afsare in consola timpi si la final nr noduri

### Functia start():
- titlu fereastra
- dimensiune ecran
- generare manager UI
- setare timp de start
- instanta catre clasa <b>Joc</b>
