from music21 import *

#file_path = "WIMU-MIDI-METRICS\data\generated\gmt\gmt-000.mid"
file_path = "symphon.mid"

def find_key_signature_aradnessen(midi_file_path):
    # Wczytaj plik MIDI
    midi_stream = converter.parse(midi_file_path)
    
    #ana = analysis.discrete.analyzeStream(midi_stream, 'aarden')
    ana =  midi_stream.analyze('aarden')
    print(ana.correlationCoefficient)
    print(ana.tonalCertainty())

    for i in range(0,180,20):
        s = midi_stream.measures(i, i+20)
        a = s.analyze('aarden')
        print(a)
        #print(a.correlationCoefficient)
        #print(a.tonalCertainty())
    return ana
    


print("Tonacja utworu:", find_key_signature_aradnessen(file_path))