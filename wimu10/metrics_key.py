import music21 as m21
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
    'C# major': 2,
    'C# minor': 3,
    'D major': 4,
    'D minor': 5,
    'D# major': 6,
    'D# minor': 7,
    'E major': 8,
    'E minor': 9,
    'F major': 10,
    'F minor': 11,
    'F# major': 12,
    'F# minor': 13,
    'G major': 14,
    'G minor': 15,
    'G# major': 16,
    'G# minor': 17,
    'A major': 18,
    'A minor': 19,
    'A# major': 20,
    'A# minor': 21,
    'B major': 22,
    'B minor': 23,
}


def get_key_from_music21_stream(stream: m21.stream.base.Score, alg_name: str = 'key.aarden') -> Collection[str, (int, int)]:
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


