# Miary synkopy

W ramach projektu biblioteka SynPy została przepisana z Pythona wersji 2 do Pythona wersji 3.
Biblioteka implementuje kilka modeli rozpoznawania synkopy w utworach zapisanych w formacie symbolicznym.
Stanowi platformę do analizy synkopy w utworach i ułatwia wyrażenie jej w formacie liczbowym, a także umożliwia porównywanie modeli ze sobą.


## Zbiory danych

## Opis modeli

### Longuet-Higgins and Lee 1984 (LHL)

Model rozkłada strumień dźwięków do struktury drzewiastej, gdzie elementy rytmu występujące wyżej w hierarchii mają wyższą "siłę".
W ten sposób możliwe jest ustanowienie podstawowego wzoru rytmicznego.
Według tego modelu synkopa występuje, gdy po nucie w "słabszej" pozycji występuje przerwa w "silniejszej" pozycji. 

### Pressing 1997 (PRS)

Model analizuje sekwencje rytmiczne w utworze i nadaje każdej sekwencji wynik w zależności od wykrytego wzoru rytmicznego.
Predefiniowane wzory, do których porównywane są sekwencje w utworze, mają z góry ustalony wynik.

### Toussaint 2002 ‘Metric Complexity’ (TMC)

Model definiuje poziom synkopy jako różnicę między zmierzoną złożonością rytmiczną danej sekwencji,
a najmniejszą możliwą złożonością rytmiczną sekwencji składającej się z takiej samej liczby nut.

### Sioros and Guedes 2011 (SG)

Podobnie jak model LHL, ten model stosuje podejście hierarchiczne do analizy sekwencji nut.
W tym modelu poziom synkopy jest wyliczany na podstawie dynamiki oraz położenia analizowanej nuty w hierarchii rytmicznej,
a także położenia nuty poprzedzającej i następującej.

### Keith 1991 (KTH)

Model nadaje najwyższą wartość synkopy nutom, które ropoczynają się i kończą w słabej części taktu.

### Toussaint 2005 ‘Off-Beatness’ (TOB)

Nuty synkopowane to te, które występują poza głównym taktem, przy czym takt jest definiowany jako
elementy w sekwencji, które występują w regularnych odstępach czasowych w cyklu.

### Gomez 2005 ‘Weighted Note-to-Beat Distance’(WNBD)

Nuta ma tym wyższą wartośc synkopy, im dalej znajduje się od najbliższego taktu (występuje poza taktem).
Synkopa jest silniejsza, jeśli nuta czasem trwania przekracza kolejny takt.

## Wnioski


## Przyszłe rozszerzenia

## Bibliografia
Song, Chunyang & Pearce, Marcus & Harte, Christopher. (2015).
[SYNPY: A PYTHON TOOLKIT FOR SYNCOPATION MODELLING](https://www.researchgate.net/publication/344730580_SYNPY_A_PYTHON_TOOLKIT_FOR_SYNCOPATION_MODELLING)