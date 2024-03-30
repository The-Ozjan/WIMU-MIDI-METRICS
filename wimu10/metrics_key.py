import music21 as mus
from collections.abc import Collection
import muspy as mp
from typing import Dict, List
from muspy.utils import NOTE_MAP
import numpy as np
from numpy.typing import NDArray

INVERT_NOTE_MAP: Dict[int, str] = {v: k for k, v in NOTE_MAP.items()}

ALL_KEY_NOTE: Dict[str, int] = {
    'C major': 0,
    'C minor': 1,
    'D major': 2,
    'D minor': 3,
    'E major': 4,
    'E minor': 5,
    'F major': 5,
    'F minor': 6,
    'G major': 7,
    'G minor': 8,
    'A major': 9,
    'A minor': 10,
    'B major': 11,
    'B minor': 12,
}


def get_key_from_music21_stream(stream: mus.stream.base.Score, alg_name: str = 'key.aarden') -> Collection[str, (int, int)]:
    # key.aarden
    # key
    # key.krumhansl
    # key.bellman
    # key.simple
    # key.temperley
    analize = stream.analyze(alg_name)
    return str(analize), (analize.correlationCoefficient, analize.tonalCertainty())


def get_key_from_muspy_music(music: mp.Music, alg_name: str = 'key.aarden') -> Collection[str, (int, int)]:
    stream = mp.to_music21(music)
    return get_key_from_music21_stream(stream=stream, alg_name=alg_name)


def compute_key_signatures_hist(music: mp.Music) -> Collection[List[int], List[int]]:
    key_signature = music.key_signatures
    hist_maj = [0] * 12
    hist_min = [0] * 12
    for key in key_signature:
        if key.mode == 'major':
            hist_maj[key.root] += 1
        elif key.mode == 'minor':
            hist_min[key.root] += 1
    return hist_maj, hist_min


def similarity_key_score(music1: mp.Music, music2: mp.Music) -> float:
    key1 = music1.key_signatures
    key2 = music2.key_signatures
    score = 0
    index_key1 = 0
    index_key2 = 0
    amount = 0
    while index_key1 < len(key1) and index_key2 < len(key2):
        amount += 1
        if key1[index_key1].root == key2[index_key2].root:
            score += 0.5
            if key1[index_key1].mode == key2[index_key2].mode:
                score += 0.5
        if index_key1 == len(key1) - 1 and index_key2 == len(key2) - 1:
            index_key1 += 1
            index_key2 += 1
        else:
            if index_key1 < len(key1) - 1 and (
                len(key2) - 1 == index_key2 or key1[index_key1 + 1].time <= key2[index_key2 + 1].time
            ):
                index_key1 += 1
            if index_key2 < len(key2) - 1 and (
                len(key1) - 1 == index_key1 or key2[index_key2 + 1].time <= key1[index_key1 + 1].time
            ):
                index_key2 += 1

    return score / amount if (not amount == 0) else amount


def key_similarity_matrix(track_list: List[mp.Music]) -> NDArray:
    track_len = len(track_list)
    similarity_matrix = np.zeros([track_len, track_len])
    for row in range(track_len):
        for col in range(track_len):
            similarity_matrix[row, col] = similarity_key_score(track_list[row], track_list[col])
    return similarity_matrix


def keys_in_tracks_matrix(track_list: List[mp.Music]) -> NDArray:
    track_len = len(track_list)
    key_matrix = np.zeros([12, track_len])
    for column in range(track_len):
        for sign in track_list[column].key_signatures:
            row = ALL_KEY_NOTE[INVERT_NOTE_MAP[sign.root] + ' ' + sign.mode]
            key_matrix[row, column] += 1
    return key_matrix


file_path2 = f'WIMU-MIDI-METRICS\data\\raw\maestro\maestro-v3.0.0\{2018}\MIDI-Unprocessed_Schubert7-9_MID--AUDIO_16_R2_2018_wav.midi'
file_path = 'WIMU-MIDI-METRICS\data\processed\dynamicsrand\dynamicsrand-003.mid'
midi_stream = mus.converter.parse(file_path)

a, b = get_key_from_music21_stream(midi_stream.measures(0, 20, collect='TimeSignature'))
print(a)

track = mp.read_midi(file_path)
track2 = mp.read_midi(file_path2)
strin11 = mp.to_music21(track)
print('aaala ', strin11.analyze('key'))
print(get_key_from_muspy_music(track))
print(compute_key_signatures_hist(track))
print(similarity_key_score(track2, track))
print(track.key_signatures)
print(key_similarity_matrix([track, track2, track, track2]))
print(keys_in_tracks_matrix([track, track, track2, track2]))
