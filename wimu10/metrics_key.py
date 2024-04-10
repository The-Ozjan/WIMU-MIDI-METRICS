import music21 as m21
from collections.abc import Collection
import muspy as mp
from typing import Dict, List
from muspy.utils import NOTE_MAP
import numpy as np
from numpy.typing import NDArray
import mido
from wimu10.midi_clip import midi_clip
from wimu10.midi_duration import midi_duration
import logging

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
    'C- major': 24,
    'C- minor': 25,
    'D- major': 26,
    'D- minor': 27,
    'E- major': 28,
    'E- minor': 29,
    'G- major': 30,
    'G- minor': 31,
    'A- major': 32,
    'A- minor': 33,
    'B- major': 34,
    'B- minor': 35,
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


def compute_key_signatures_hist(key_list: List[Collection[str, float]]) -> Collection[List[int], List[str]]:
    key_dic = {}
    for key, _ in key_list:
        if key in key_dic.keys():
            key_dic[key] += 1
        else:
            key_dic[key] = 1
    return list(key_dic.values()), list(key_dic.keys())


def similarity_key_score(key_list1: List[Collection[(str, float)]], key_list2: List[Collection[(str, float)]]) -> float:
    score = 0
    index_key1 = 0
    index_key2 = 0
    amount = 0
    while index_key1 < len(key_list1) and index_key2 < len(key_list2):
        amount += 1
        key1_name = key_list1[index_key1][0].capitalize()
        key2_name = key_list2[index_key2][0].capitalize()
        if key1_name[0] == key2_name[0]:
            score += 0.5
            if key1_name == key2_name:
                score += 0.5
        if index_key1 == len(key_list1) - 1 and index_key2 == len(key_list2) - 1:
            index_key1 += 1
            index_key2 += 1
        else:
            if index_key1 < len(key_list1) - 1 and (
                len(key_list2) - 1 == index_key2 or key_list1[index_key1 + 1][1] <= key_list2[index_key2 + 1][1]
            ):
                index_key1 += 1
            if index_key2 < len(key_list2) - 1 and (
                len(key_list1) - 1 == index_key1 or key_list2[index_key2 + 1][1] <= key_list1[index_key1 + 1][1]
            ):
                index_key2 += 1

    return score / amount if (not amount == 0) else amount


def key_similarity_matrix(track_list: List[List[Collection[(str, float)]]]) -> NDArray:
    track_len = len(track_list)
    similarity_matrix = np.zeros([track_len, track_len])
    for row in range(track_len):
        for col in range(track_len):
            similarity_matrix[row, col] = similarity_key_score(track_list[row], track_list[col])
    return similarity_matrix


def keys_in_tracks_matrix(track_list: List[List[Collection[(str, float)]]], norm: bool = True) -> NDArray:
    track_len = len(track_list)
    key_matrix = np.zeros([len(ALL_KEY_NOTE), track_len])
    for column in range(track_len):
        for key in track_list[column]:
            row = ALL_KEY_NOTE[key[0].capitalize()]
            key_matrix[row, column] += 1 / len(track_list[column]) if (norm) else 1
    return key_matrix


def get_keys_from_sampled_midi(
    midi: mido.MidiFile, sample_duration: float = 10.0, alg_name: str = 'key.aarden', only_change: bool = False
) -> List[Collection[(str, float)]]:
    ori_ratio = midi_duration(midi)
    begin = 0.0
    key_list = []
    list_index = 0
    while begin + sample_duration <= ori_ratio:
        cutted = midi_clip(midi, begin, begin + sample_duration)
        cutted_muspy = mp.from_mido(cutted)
        try:
            key, metrics = get_key_from_muspy_music(cutted_muspy, alg_name=alg_name)
            if not only_change or list_index == 0 or not key_list[-1][0] == key:
                key_list.append((key, begin))
        except:
            logging.error("Couldn't compute key")
        begin += sample_duration / 2
        list_index += 1
    return key_list
