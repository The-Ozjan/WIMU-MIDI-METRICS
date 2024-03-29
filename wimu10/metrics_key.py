
import music21 as mus
from collections.abc import Collection
import muspy as mp
from typing import Dict, List
from muspy.utils import NOTE_MAP

file_path = "amaj.mid"    
midi_stream = mus.converter.parse(file_path)


INVERT_NOTE_MAP: Dict[int, str] = {v: k for k, v in NOTE_MAP.items()}

class KeyDuration:
    def __init__(self, start:int, stop:int, key:str) -> None:
        self.start = start
        self.stop = stop
        self.key = key
        

def get_key_from_music21_stream(stream: mus.stream.base.Score, alg_name: str = "key.aarden")-> Collection[str, (int, int)]:
    # key.aarden
    # key
    # key.krumhansl
    # key.bellman
    # key.simple
    # key.temperley
    analize = stream.analyze(alg_name)
    return str(analize), (analize.correlationCoefficient, analize.tonalCertainty()) 

def get_key_from_muspy_music(music: mp.Music, alg_name: str = "key.aarden")-> Collection[str, (int, int)]:
    stream = mp.to_music21(music)
    return get_key_from_music21_stream(stream=stream, alg_name=alg_name)

def compute_key_signatures_hist(music: mp.Music)->Collection[List[int], List[int]]:
    key_signature = music.key_signatures
    hist_maj = [0] * 12
    hist_min = [0] *12
    for key in key_signature:
        if key.mode == "major":
            hist_maj[key.root] += 1
        elif  key.mode == "minor":
            hist_min[key.root] +=2
    return hist_maj, hist_min



a, b = get_key_from_music21_stream(midi_stream.measures(0, 20, collect='TimeSignature'))
print(a)

track = mp.read_midi(file_path)
strin11 = mp.to_music21(track)
print("aaala ", strin11.analyze("key"))
print(get_key_from_muspy_music(track))

print(track.key_signatures)
