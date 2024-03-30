
import music21 as mus
from collections.abc import Collection
import muspy as mp
from typing import Dict, List
from muspy.utils import NOTE_MAP

file_path = "amaj.mid"
file_path2 = "symphon.mid"    
midi_stream = mus.converter.parse(file_path)


INVERT_NOTE_MAP: Dict[int, str] = {v: k for k, v in NOTE_MAP.items()}

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
            hist_min[key.root] +=1
    return hist_maj, hist_min

def similarity_key_score(music1: mp.Music, music2: mp.Music)-> float:
    key1 = music1.key_signatures
    key2 = music2.key_signatures
    score = 0
    index_key1 = 0
    index_key2 = 0
    amount = 0
    while index_key1 < len(key1) and index_key2 < len(key2):
        amount += 1
        if(key1[index_key1].root == key2[index_key2].root):
            score += 0.5
            if(key1[index_key1].mode == key2[index_key2].mode):
                score += 0.5
        if(index_key1 == len(key1)-1 and index_key2 == len(key2)-1):
            index_key1 += 1
            index_key2 +=1
        else:
            if(index_key1 < len(key1)-1 and( len(key2) -1 == index_key2 or key1[index_key1+1].time <= key2[index_key2+1].time)):
                index_key1 += 1
            if(index_key2 < len(key2)-1 and( len(key1) -1 == index_key1 or key2[index_key2+1].time <= key1[index_key1+1].time)):
                index_key2 += 1

    return score/amount if(not amount == 0)  else amount


a, b = get_key_from_music21_stream(midi_stream.measures(0, 20, collect='TimeSignature'))
print(a)

track = mp.read_midi(file_path)
track2 = mp.read_midi(file_path2)
strin11 = mp.to_music21(track)
print("aaala ", strin11.analyze("key"))
print(get_key_from_muspy_music(track))
print(compute_key_signatures_hist(track))
print(similarity_key_score(track2, track))
print(track.key_signatures)
