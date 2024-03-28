
import music21 as mus
from collections.abc import Collection

#file_path = "WIMU-MIDI-METRICS\data\generated\gmt\gmt-000.mid"
file_path = "amaj.mid"

def find_key_signature_aradnessen(midi_file_path):
    # Wczytaj plik MIDI
    midi_stream = mus.converter.parse(midi_file_path)
    
    #ana = analysis.discrete.analyzeStream(midi_stream, 'aarden')
    # key.aarden
    # key
    # key.krumhansl
    # key.bellman
    # key.simple
    # key.temperley
    ana =  midi_stream.analyze('key.krumhansl')
    print(ana.correlationCoefficient)
    print(ana.tonalCertainty())
    print(type(midi_stream))
    # for i in range(0,180,20):
    #     s = midi_stream.measures(i, i+20)
    #     a = s.analyze('aarden')
    #     print(a)
    #     #print(a.correlationCoefficient)
    #     #print(a.tonalCertainty())
    return ana
    
midi_stream = mus.converter.parse(file_path)
    # key.aarden
    # key
    # key.krumhansl
    # key.bellman
    # key.simple
    # key.temperley

def get_key_from_stream(steram: mus.stream.base.Score, alg_name: str = "key.aarden")-> Collection[str, (int, int)]:
    analize = steram.analyze(alg_name)
    return str(analize), (analize.correlationCoefficient, analize.tonalCertainty()) 

a, b = get_key_from_stream(midi_stream)
print(a)
print(type(a))
print(b)