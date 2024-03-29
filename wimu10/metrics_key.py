
import music21 as mus
from collections.abc import Collection

#file_path = "WIMU-MIDI-METRICS\data\generated\gmt\gmt-000.mid"
file_path = "symphon.mid"    
midi_stream = mus.converter.parse(file_path)
def calc_measure(stri):
    num_measures = 0
    for part in stri.parts:
        # Zlicz takti w każdej części
        num_measures += len(part.getElementsByClass(mus.stream.Measure))
    return num_measures
    # key.aarden
    # key
    # key.krumhansl
    # key.bellman
    # key.simple
    # key.temperley

def get_key_from_stream(stream: mus.stream.base.Score, alg_name: str = "key.aarden")-> Collection[str, (int, int)]:
    analize = stream.analyze(alg_name)
    return str(analize), (analize.correlationCoefficient, analize.tonalCertainty()) 

def get_keys_from_divided_stream(stream: mus.stream.base.Score, alg_name: str = "key.aarden", amount: int=1 )-> Collection[int]:
    key_list = []
    if amount <=0:
        pass
    else:
        stream_len = calc_measure(stream)
        print(len(stream))
        step = max(int(stream_len/amount), 1)
        for i in range(0, stream_len-step,  step):
            end_stream = min(i+step, stream_len)
            new_stream = stream.measures(i, end_stream)
            key, _ = get_key_from_stream(stream=new_stream, alg_name=alg_name)
            key_list.append(key)
    return key_list


a, b = get_key_from_stream(midi_stream.measures(0, 20, collect='TimeSignature'))
print(a)
print(type(a))
print(b)
print(get_keys_from_divided_stream(midi_stream, amount=8))
