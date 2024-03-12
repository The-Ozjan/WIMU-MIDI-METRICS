# Opracowanie nowych metryk do ewaluacji muzyki symbolicznej w formacie MIDI (kontynuacja)

Temat realizowany przez zespół nr 6 w składzie:

- Jakub Sadowski
- Wiktor Targosiński
- Hubert Wysocki

## Wstęp

Projekt jest kontynuacją projektu o takim samym tytule z semestru 23Z. Rozszerzone zostanie repozytorium [WIMU10](https://github.com/Dove6/WIMU10). Głównym celem jest zbadanie metryk dla muzyki generowanej w zapisie symbolicznym, w formacie MIDI [^back1999].

Repozytorium zawierać będzie również przykładowy program (skrypt) konsolowy prezentujący sposób korzystania z API.
Program pozwalał będzie na wyznaczenie metryk dla wybranych plików w trybie wsadowym.

## Planowane funkcjonalności

Planowane rozszerzenie istniejącego projektu zawierać będzie:

A. Metryki dotyczące:

- rytmu - synkopa, metrum
- wysokości/harmonii - zmiany tonacji
- agogiki - zmiany tempa

B. Porównanie zależności naszych (oraz uprzednio opracowanych) metryk z istniejącymi w bibliotece MusPy.  
C. Porównanie jakości tokenizatorów MIDI dostępnych w bibliotece MidiTok.  
D. Eksperymentalne metryki korzystające z embeddingów CLAMP.  
E. (opcjonalnie) Zastosowanie istniejących i opracowanych metryk MIDI do innych zapisów symbolicznych, np. ABC.

## Zbiory danych

Eksperymenty dotyczące metryk które chcemy zbadać, wykonane zostaną dla danych ze  zbiorów zaproponowanych w pracy [WIMU10](https://github.com/Dove6/WIMU10). W jego skład wchodzą zbiory:

- The Lakh MIDI Dataset [^raffel2016dataset] [^raffel2016],  
- MAESTRO [^hawthorne2019],  
- NES-MDB (Nintendo Entertainment System Music Database) [^donahue2018],  
- MusicNet [^thickstun2017],  
- EMOPIA [^hung2021],  

oraz utwory w MIDI wygenerowane z użyciem istniejących, wytrenowanych modeli uczenia maszynowego (technologia GAN [^dong2017] lub Transformer [^huang2018]). Uzyskane przez nas wyniki zostaną porównane z dostępnymi metrykami w bibliotece MusPy. Po wykonanych badaniach wszystkie uzyskane wyniki zostaną podsumowane.

## Planowany zakres eksperymentów

Planujemy wykonać część zadań, które zostały pominięte w poprzedniej realizacji projektu, oraz dołożyć parę innych:

1. Dla wybranych zbiorów danych porównamy metryki z MusPy z naszymi.
   Sprawdzimy, czy są od siebie zależne, tzn. czy kierunek zmiany obu metryk jest skorelowany.
2. (opcjonalnie) Zbadamy, jak mają się wartości metryk na wybranych utworach do naszych odczuć.
   Zrobimy to w sposób porównawczy, prezentując badanej osobie dwa utwory o różnych wartościach metryk.
   Potencjalnie wykorzystamy do oceny skalę Likerta z ogólnymi stwierdzeniami postaci "Utwór nr 1 brzmi lepiej niż utwór nr 2".
3. Dokonamy porównania jakościowego tokenizatorów z biblioteki MidiTok.
4. Przeanalizujemy korelację embeddingów CLAMP z naszymi metrykami, oraz tymi z MusPy. Utworzymy eksperymentalne metryki korzystające z embeddingów.

## Planowany stack technologiczny

Docelowy format: biblioteka.

Narzędzia:

- język: Python
- środowisko wirtualne: venv
- autoformatowanie i linter: ruff
- przetwarzanie: NumPy, MusPy
- testy: pytest
- zbieranie logów: logging
- dokumentacja: sphinx
- interfejs konsolowy: argparse
- wizualizacja: matplotlib

## Harmonogram i planowany postęp

Oznaczenia kategorii zadań znajdują się w rozdziale Planowane funkcjonalności. Harmonogram służy jako przewodnik w realizacji projektu i może ulec zmianie. W przypadku decyzji o realizacji opcjonalnego zagadnienia E, oznaczać to będzie zmianę planu dla pewnych tygodni.

- 11.03 - 17.03 - szczegółowe zapoznanie się z istniejącym projektem
- 18.03 - 24.03  
- 25.03 - 31.03 - Demonstracja postępu analizy literaturowej oraz konfiguracja środowiska wykonawczego
- 01.04 - 07.04 - A
- 08.04 - 14.04 - A
- 15.04 - 21.04 - A/B  
- 22.04 - 28.04 - B
- 29.04 - 05.05 - majówka
- 06.05 - 12.05 - B/C
- 13.05 - 19.05 - C
- 20.05 - 26.05 - C
- 27.05 - 02.06 - C/D
- 03.06 - 09.06 - D
- 10.06 - 16.06 - etap finałowy

## Bibliografia

[^back1999]: ["Standard MIDI-File Format Spec. 1.1, updated", David Back, 1999](https://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html)
<!-- [^dai2022]: ["What is missing in deep music generation? A study of repetition and structure in popular music", Shuqi Dai & Huiran Yu & Roger B. Dannenberg, 2022](https://arxiv.org/abs/2209.00182)  
[^chi2020]: ["Generating Music with a Self-Correcting Non-Chronological Autoregressive Model", Wayne Chi et al., 2020](https://arxiv.org/abs/2008.08927)  
[^dong2020]: ["MusPy: A toolkit for symbolic music generation", Hao-Wen Dong et al., 2020](https://arxiv.org/abs/2008.01951)  
[^yang2020]: ["On the evaluation of generative models in music", Li-Chia Yang & Alexander Lerch, 2020](https://www.researchgate.net/publication/328728367_On_the_evaluation_of_generative_models_in_music)  
[^ji2020]: ["A Comprehensive Survey on Deep Music Generation: Multi-level Representations, Algorithms, Evaluations, and Future Directions", Shulei Ji & Jing Luo & Xinyu Yang, 2020](https://arxiv.org/abs/2011.06801)  
[^xiong2023]: ["A Comprehensive Survey for Evaluation Methodologies of AI-Generated Music", Zeyu Xiong et al., 2023](https://arxiv.org/abs/2308.13736)   -->
[^dong2017]: ["MuseGAN: Multi-track Sequential Generative Adversarial Networks for Symbolic Music Generation and Accompaniment", Hao-Wen Dong et al., 2017](https://arxiv.org/abs/1709.06298)  
[^huang2018]: ["Music Transformer: Generating music with long-term structure", Cheng-Zhi Anna Huang et al., 2018](https://arxiv.org/abs/1809.04281)  
[^raffel2016dataset]: ["The Lakh MIDI Dataset", Collin Raffel, accessed 14.11.2023](https://colinraffel.com/projects/lmd/)
[^raffel2016]: ["Learning-Based Methods for Comparing Sequences, with Applications to Audio-to-MIDI Alignment and Matching", Collin Raffel, 2016](https://academiccommons.columbia.edu/doi/10.7916/D8N58MHV)
<!-- [^dong2017dataset]: ["Lakh Pianoroll Dataset", Hao-Wen Dong et al., accessed 17.11.2023](https://salu133445.github.io/lakh-pianoroll-dataset/) -->
[^hawthorne2019]: ["Enabling Factorized Piano Music Modeling and Generation with the MAESTRO Dataset", Curtis Hawthorne et al., 2019](https://openreview.net/forum?id=r1lYRjC9F7)
<!-- [^bittner2022]: ["A Lightweight Instrument-Agnostic Model for Polyphonic Note Transcription and Multipitch Estimation", Rachel M. Bittner et al., 2022](https://arxiv.org/abs/2203.09893) -->
[^donahue2018]: ["The NES Music Database: A multi-instrumental dataset with expressive performance attributes", Donahue et al., 2018](https://arxiv.org/abs/1806.04278)
[^thickstun2017]: ["Learning Features of Music from Scratch", John Thickstun et al., 2017](https://arxiv.org/abs/1611.09827)
<!-- [^gardner2022]: ["MT3: Multi-Task Multitrack Music Transcription", Josh Gardner et al., 2022](https://arxiv.org/abs/2111.03017v4) -->
[^hung2021]: ["EMOPIA: A Multi-Modal Pop Piano Dataset For Emotion Recognition and Emotion-based Music Generation", Hsiao-Tzu Hung et al., 2021](https://arxiv.org/abs/2108.01374)
<!-- [^bertin-mahieux2011]: ["The Million Song Dataset", Thierry Bertin-Mahieux, 2011](https://academiccommons.columbia.edu/doi/10.7916/D8NZ8J07)
[^manilow2019]: ["Cutting Music Source Separation Some Slakh: A Dataset to Study the Impact of Training Data Quality and Quantity", Ethan Manilow et al., 2019](https://arxiv.org/abs/1909.08494)
[^manilow2020]: ["Simultaneous Separation and Transcription of Mixtures with Multiple Polyphonic and Percussive Instruments", Ethan Manilow et al., 2020](https://arxiv.org/abs/1910.12621)
[^xi2018]: [Guitarset: A Dataset for Guitar Transcription, Qingyang Xi et al., 2018](https://archives.ismir.net/ismir2018/paper/000188.pdf)
[^li2018]: ["Creating a multi-track classical music performance dataset for multi-modal music analysis: Challenges, insights, and applications", Bochen Li et al., 2018](https://labsites.rochester.edu/air/publications/li2018creating.pdf)
[^kong2020]: ["High-resolution Piano Transcription with Pedals by Regressing Onset and Offset Times", Qiuqiang Kong et al., 2020](https://arxiv.org/abs/2010.01815) -->
