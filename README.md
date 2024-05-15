# Opracowanie nowych metryk do ewaluacji muzyki symbolicznej w formacie MIDI (kontynuacja)

Projekt realizowany przez zespół nr 6 w składzie:

- Jakub Sadowski
- Wiktor Targosiński
- Hubert Wysocki

[Design proposal](DESIGN_PROPOSAL.md)

## Planowane funkcjonalności

Stan obecny planowanej funkcjonalności projektu:

A. Metryki dotyczące:

- rytmu - synkopa ⏳, metrum ✔️
- wysokości/harmonii - zmiany tonacji ✔️
- agogiki - zmiany tempa ❌

B. (opcjonalnie) Porównanie zależności naszych (oraz uprzednio opracowanych) metryk z istniejącymi w bibliotece MusPy. ❓  
C. Porównanie jakości tokenizatorów MIDI dostępnych w bibliotece MidiTok. ❌  
D. Eksperymentalne metryki korzystające z embeddingów CLAMP. ⏳  
E. (opcjonalnie) Zastosowanie istniejących i opracowanych metryk MIDI do innych zapisów symbolicznych, np. ABC. ❌

W procesie tworzenia projektu postanowiliśmy pominąć punkty B oraz C i skupić się bardziej na metrykach korzystających z embeddingów CLAMP. Jeśli wystarczy czasu, rozważamy powrót do punktu B.

## Aktualny harmonogram

- 11.03 - 17.03 - szczegółowe zapoznanie się z istniejącym projektem
- 18.03 - 24.03  
- 25.03 - 31.03 - Demonstracja postępu analizy literaturowej oraz konfiguracja środowiska wykonawczego
- 01.04 - 07.04 - A
- 08.04 - 14.04 - A
- 15.04 - 21.04 - A  
- 22.04 - 28.04 - A
- 29.04 - 05.05 - majówka
- 06.05 - 12.05 - A/D
- 13.05 - 19.05 - A/D
- 20.05 - 26.05 - D
- 27.05 - 02.06 - D
- 03.06 - 09.06 - D/B?
- 10.06 - 16.06 - etap finałowy
