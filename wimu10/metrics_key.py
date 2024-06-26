import music21 as m21
import muspy as mp
from typing import Dict, List, Tuple
from muspy.utils import NOTE_MAP
import numpy as np
from numpy.typing import NDArray
import mido
from wimu10.midi_clip import midi_clip
from wimu10.midi_duration import midi_duration
import logging
import copy
from typing import Optional

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

ALGORITHM_DICT: Dict[str, str] = {
    'AardenEssen': 'key.aarden',
    'KrumhanslSchmuckler': 'key.krumhansl',
    'BellmanBudge': 'key.bellman',
    'SimpleWeights': 'key.simple',
    'TemperleyKostkaPayne': 'key.temperley',
}


class PartKey:
    """
    Class containing part of music key and beginning time 
    """
    def __init__(self, key: Optional[str] = None, begin: float = 0) -> None:
        """
        key: containing nake of key
        begin: time of key begin in music
        """
        if not (begin >= 0 and (isinstance(begin, float) or isinstance(begin, int))):
            raise ValueError
        self.key = key
        self.begin = begin


MidiKeys = List[PartKey]


def get_key_from_music21_stream(stream: m21.stream.base.Score, alg_name: str = 'key.aarden') -> Tuple[str, int, int]:
    """
    Function for key from music getting via music21 library
    
    stream: music21 stream with symbolic music
    alg_name: Name of algorithm from music21 library for key extraction

    returns: tuple of key name, correlation coefficient and tonal certainty
    """
    analize = stream.analyze(alg_name)
    return str(analize), analize.correlationCoefficient, analize.tonalCertainty()


def get_key_from_muspy_music(music: mp.Music, alg_name: str = 'key.aarden') -> Tuple[str, int, int]:
    """
    Function for key from music getting via music21 library
    
    music: muspy Music with symbolic music
    alg_name: Name of algorithm from music21 library for key extraction

    returns: tuple of key name, correlation coefficient and tonal certainty
    """
    stream = mp.to_music21(music)
    return get_key_from_music21_stream(stream=stream, alg_name=alg_name)


def compute_key_signatures_hist(key_list: MidiKeys) -> Tuple[List[int], List[str]]:
    """
    Function for keys in music histogram computing

    key_list: list with PartKeys of music track

    returns: tuple of two lists. First list with amount of each key in track and second with key names
    """
    key_dic = {}
    for key in key_list:
        if key.key in key_dic.keys():
            key_dic[key.key] += 1
        else:
            key_dic[key.key] = 1
    return list(key_dic.values()), list(key_dic.keys())


def similarity_key_score(key_list1: MidiKeys, key_list2: MidiKeys) -> float:
    """
    Function for similarity score computing. It tests if music have in the same time same key

    key_list1: list with PartKeys of first music
    key_list2: list with PartKeys of second music

    returns: score in float
    """
    score = 0
    index_key1 = 0
    index_key2 = 0
    amount = 0
    is_index1_changed = False
    is_index2_changed = False
    while index_key1 < len(key_list1) and index_key2 < len(key_list2):
        amount += 1
        key1_name = key_list1[index_key1].key.capitalize()
        key2_name = key_list2[index_key2].key.capitalize()
        if key1_name[0] == key2_name[0]:
            score += 0.5
            if key1_name == key2_name:
                score += 0.5
        if index_key1 == len(key_list1) - 1 and index_key2 == len(key_list2) - 1:
            index_key1 += 1
            index_key2 += 1
        else:
            if index_key1 < len(key_list1) - 1 and (
                len(key_list2) - 1 == index_key2
                or (
                    key_list1[index_key1 + 1].begin <= key_list2[index_key2 + 1].begin
                    and key_list1[index_key1 + 1].begin >= key_list2[index_key2].begin
                )
            ):
                is_index1_changed = True
            if index_key2 < len(key_list2) - 1 and (
                len(key_list1) - 1 == index_key1
                or (
                    key_list2[index_key2 + 1].begin <= key_list1[index_key1 + 1].begin
                    and key_list2[index_key2 + 1].begin >= key_list1[index_key1].begin
                )
            ):
                is_index2_changed = True

            if is_index1_changed:
                index_key1 += 1
                is_index1_changed = False
            if is_index2_changed:
                index_key2 += 1
                is_index2_changed = False

    return score / amount if (not amount == 0) else amount


def key_similarity_matrix(track_list: List[MidiKeys]) -> NDArray:
    """
    Function for key similarity matrix computing

    track_list: list of tracks containing list of track PartKeys

    returns: numpy array with similaritie scores rows and columns are music tracs
    """
    track_len = len(track_list)
    similarity_matrix = np.zeros([track_len, track_len])
    for row in range(track_len):
        for col in range(track_len):
            similarity_matrix[row, col] = similarity_key_score(track_list[row], track_list[col])
    return similarity_matrix


def keys_in_tracks_matrix(track_list: List[MidiKeys], norm: bool = True) -> NDArray:
    """
    Function for computing matrix of keys amount in tracks

    track_list: list of tracks containing list of track PartKeys
    norm: bool value if matrix should contain normalised values

    returns: matrix where rows are keys and columns are tracks
    """
    track_len = len(track_list)
    key_matrix = np.zeros([len(ALL_KEY_NOTE), track_len])
    for column in range(track_len):
        for key in track_list[column]:
            row = ALL_KEY_NOTE[key.key.capitalize()]
            key_matrix[row, column] += 1 / len(track_list[column]) if (norm) else 1
    return key_matrix


def get_keys_from_sampled_midi(
    midi: mido.MidiFile, sample_duration: float = 10.0, alg_name: str = 'key.aarden', only_change: bool = False
) -> MidiKeys:
    """
    Function for computing PartKeys  from track

    midi: mido MidiFile with midi track
    sample_duration: duration of sample from track which is used for key computing
    alg_name: Name of algorithm from music21 library for key extraction
    only_change: left only new keys in list

    returns: List of PartKeys
    """
    ori_ratio = midi_duration(copy.deepcopy(midi))
    begin = 0.0
    key_list = []
    list_index = 0
    while begin + sample_duration <= ori_ratio:
        cutted = midi_clip(midi, begin, begin + sample_duration)
        cutted_muspy = mp.from_mido(cutted)
        try:
            key, _, _ = get_key_from_muspy_music(cutted_muspy, alg_name=alg_name)
            if not only_change or list_index == 0 or not key_list[-1][0] == key:
                key_list.append(PartKey(key, begin))
        except:
            # logging.error("Couldn't compute key")
            pass
        begin += sample_duration / 2
        list_index += 1
    return key_list


def diff_alg_keys(music: mp.Music) -> NDArray:
    """
    Function for getting single keys for track from all algorithms

    music: muspy Music class with symbolic music

    returns: numpy array where rows are keys and columns are algorithms
    """
    output = np.zeros([len(ALL_KEY_NOTE), len(ALGORITHM_DICT)])
    col = 0
    for key_alg in ALGORITHM_DICT.keys():
        key, _, _ = get_key_from_muspy_music(music, alg_name=ALGORITHM_DICT[key_alg])
        row = ALL_KEY_NOTE[key.capitalize()]
        output[row, col] = 1
        col += 1
    return output


def diff_alg_keys_music_list(music_list: List[mp.Music]) -> NDArray:
    """
    Function for getting normalised value of keys amount from different keys algorithm for whole track

    music_list: list with tracks in muspy Music classes

    returns: numpy array with normalised value of keys amount from different keys algorithm for whole track
    """
    music_list_len = len(music_list)
    output = np.zeros([len(ALL_KEY_NOTE), music_list_len])
    col = 0
    for music in music_list:
        for key_alg in ALGORITHM_DICT.keys():
            key, _, _ = get_key_from_muspy_music(music, alg_name=ALGORITHM_DICT[key_alg])
            row = ALL_KEY_NOTE[key.capitalize()]
            output[row, col] += 1.0 / float(len(ALGORITHM_DICT))
        col += 1
    return output


def key_for_whole_music_matrix(music_list: List[mp.Music], alg: str = 'key.aarden') -> NDArray:
    """
    Function for creating matrix with key from whole track computed by selected algorithm

    music_list: list with tracks in muspy Music classes
    alg_name: Name of algorithm from music21 library for key extraction

    returns: numpy array where rows are possible keys, columns are tracks
    """
    music_list_len = len(music_list)
    output = np.zeros([len(ALL_KEY_NOTE), music_list_len])
    col = 0
    for music in music_list:
        key, _, _ = get_key_from_muspy_music(music, alg_name=alg)
        row = ALL_KEY_NOTE[key.capitalize()]
        output[row, col] = 1
        col += 1
    return output
