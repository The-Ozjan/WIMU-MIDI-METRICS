import muspy as mp
import numpy as np
from wimu10 import metrics_key as mk
import mido
import music21 as m21
import copy


def test_keys_from_sample_midi():
    music = mido.MidiFile('tests/data/some_repeats.mid')
    l1 = mk.get_keys_from_sampled_midi(copy.deepcopy(music), sample_duration=5)
    l2 = mk.get_keys_from_sampled_midi(copy.deepcopy(music), sample_duration=5)
    assert len(l1) == len(l2)
    assert l2[-1].key == l1[-1].key
    assert l2[0].key == l1[0].key


def test_get_key_from_music21_stream():
    music = m21.converter.parse('tests/data/some_repeats.mid')
    ret = mk.get_key_from_music21_stream(music)
    assert ret[0] == 'a minor'
    assert isinstance(ret[1], float)


def test_get_key_from_music21_stream_krumhansl():
    music = m21.converter.parse('tests/data/some_repeats.mid')
    ret = mk.get_key_from_music21_stream(music, alg_name='key.krumhansl')
    assert ret[0] == 'C major'
    assert isinstance(ret[1], float)


def test_get_key_from_music21_stream_bellman():
    music = m21.converter.parse('tests/data/some_repeats.mid')
    ret = mk.get_key_from_music21_stream(music, alg_name='key.bellman')
    assert ret[0] == 'C major'
    assert isinstance(ret[1], float)


def test_get_key_from_music21_stream_simple():
    music = m21.converter.parse('tests/data/some_repeats.mid')
    ret = mk.get_key_from_music21_stream(music, alg_name='key.simple')
    assert ret[0] == 'C major'
    assert isinstance(ret[1], float)


def test_get_key_from_music21_stream_temperley():
    music = m21.converter.parse('tests/data/some_repeats.mid')
    ret = mk.get_key_from_music21_stream(music, alg_name='key.temperley')
    assert ret[0] == 'a minor'
    assert isinstance(ret[2], float)


def test_get_key_from_muspy_music():
    music = mp.read_midi('tests/data/some_repeats.mid')
    ret = mk.get_key_from_muspy_music(music)
    assert ret[0] == 'a minor'
    assert isinstance(ret[2], float)


def test_get_key_from_muspy_music_krumhansl():
    music = mp.read_midi('tests/data/some_repeats.mid')
    ret = mk.get_key_from_muspy_music(music, alg_name='key.krumhansl')
    assert ret[0] == 'C major'
    assert isinstance(ret[2], float)


def test_compute_key_signatures_hist():
    key_list = [
        mk.PartKey('C major', 0),
        mk.PartKey('C minor', 10),
        mk.PartKey('A major', 20),
        mk.PartKey('D minor', 30),
        mk.PartKey('C major', 40),
        mk.PartKey('A major', 50),
        mk.PartKey('A major', 60),
        mk.PartKey('C minor', 70),
    ]
    list_keys, list_names = mk.compute_key_signatures_hist(key_list)
    assert len(list_keys) == 4
    assert list_keys[0] == 2
    assert list_keys[1] == 2
    assert list_keys[2] == 3
    assert list_keys[3] == 1
    assert list_names[0] == 'C major'
    assert list_names[1] == 'C minor'
    assert list_names[2] == 'A major'
    assert list_names[3] == 'D minor'


def test_similarity_key_score_same():
    key_list = [
        mk.PartKey('C major', 0),
        mk.PartKey('C minor', 10),
        mk.PartKey('A major', 20),
        mk.PartKey('D minor', 30),
        mk.PartKey('C major', 40),
        mk.PartKey('A major', 50),
        mk.PartKey('A major', 60),
        mk.PartKey('C minor', 70),
    ]
    assert mk.similarity_key_score(key_list, key_list) == 1.0


def test_similarity_key_score_different():
    key_list = [
        mk.PartKey('C major', 0),
        mk.PartKey('C minor', 10),
        mk.PartKey('A major', 20),
        mk.PartKey('D minor', 30),
        mk.PartKey('C major', 40),
        mk.PartKey('A major', 50),
        mk.PartKey('A major', 60),
        mk.PartKey('C minor', 70),
    ]
    key_list2 = [mk.PartKey('F major', 0), mk.PartKey('D major', 10), mk.PartKey('G- major', 20)]
    assert mk.similarity_key_score(key_list, key_list2) == 0.0


def test_similarity_key_score_some_similarities():
    key_list = [
        mk.PartKey('C major', 0),
        mk.PartKey('C minor', 10),
        mk.PartKey('A major', 20),
        mk.PartKey('D minor', 30),
        mk.PartKey('C major', 40),
        mk.PartKey('A major', 50),
        mk.PartKey('A major', 60),
        mk.PartKey('C minor', 70),
    ]
    key_list2 = [mk.PartKey('C major', 0), mk.PartKey('C major', 10), mk.PartKey('G- major', 20)]
    assert mk.similarity_key_score(key_list, key_list2) == 0.1875
    key_list2 = [mk.PartKey('C major', 0), mk.PartKey('C major', 15), mk.PartKey('A minor', 55), mk.PartKey('G- major', 90)]
    assert abs(mk.similarity_key_score(key_list, key_list2) - 0.363) <= 0.001


def test_similarity_key_score_smaller_first():
    key_list = [
        mk.PartKey('C major', 0),
        mk.PartKey('C minor', 10),
        mk.PartKey('A major', 20),
        mk.PartKey('D minor', 30),
        mk.PartKey('C major', 40),
        mk.PartKey('A major', 50),
        mk.PartKey('A major', 60),
        mk.PartKey('C minor', 70),
    ]
    key_list2 = [mk.PartKey('C major', 0), mk.PartKey('C major', 10), mk.PartKey('G- major', 20)]
    assert mk.similarity_key_score(key_list2, key_list) == 0.1875
    key_list2 = [mk.PartKey('C major', 0), mk.PartKey('C major', 15), mk.PartKey('A minor', 55), mk.PartKey('G- major', 90)]
    assert abs(mk.similarity_key_score(key_list2, key_list) - 0.363) <= 0.001


def test_key_similarity_matrix():
    key_list = [
        mk.PartKey('C major', 0),
        mk.PartKey('C minor', 10),
        mk.PartKey('A major', 20),
        mk.PartKey('D minor', 30),
        mk.PartKey('C major', 40),
        mk.PartKey('A major', 50),
        mk.PartKey('A major', 60),
        mk.PartKey('C minor', 70),
    ]
    key_list2 = [mk.PartKey('C major', 0), mk.PartKey('C major', 10), mk.PartKey('G- major', 20)]
    key_list3 = [mk.PartKey('C major', 0), mk.PartKey('C major', 15), mk.PartKey('A minor', 55), mk.PartKey('G- major', 90)]
    key_list4 = [mk.PartKey('F major', 0), mk.PartKey('D major', 10), mk.PartKey('G- major', 20)]
    matrix = mk.key_similarity_matrix([key_list, key_list2, key_list3, key_list4, key_list])
    assert matrix[0, 0] == 1.0
    assert matrix[0, 1] == 0.1875 and matrix[1, 0] == 0.1875
    assert abs(matrix[0, 2] - 0.363) <= 0.001 and abs(matrix[2, 0] - 0.363) <= 0.001
    assert matrix[0, 3] == 0.0 and matrix[3, 0] == 0.0
    assert matrix[0, 4] == 1.0 and matrix[4, 0] == 1.0


def test_keys_in_tracks_matrix():
    key_list = [
        mk.PartKey('C major', 0),
        mk.PartKey('C minor', 10),
        mk.PartKey('A major', 20),
        mk.PartKey('D minor', 30),
        mk.PartKey('C major', 40),
        mk.PartKey('A major', 50),
        mk.PartKey('A major', 60),
        mk.PartKey('C minor', 70),
    ]
    key_list2 = [mk.PartKey('C major', 0), mk.PartKey('C major', 10), mk.PartKey('G- major', 20)]
    key_list3 = [mk.PartKey('E- major', 0), mk.PartKey('B minor', 15), mk.PartKey('G- major', 90)]
    matrix = mk.keys_in_tracks_matrix([key_list, key_list2, key_list3])
    assert matrix[0, 0] == 2.0 / 8.0
    assert matrix[1, 0] == 2.0 / 8.0
    assert matrix[18, 0] == 3.0 / 8.0
    assert matrix[5, 0] == 1.0 / 8.0
    assert matrix[0, 1] == 2.0 / 3.0
    assert matrix[30, 1] == 1.0 / 3.0
    assert matrix[30, 2] == 1.0 / 3.0
    assert matrix[28, 2] == 1.0 / 3.0
    assert matrix[23, 2] == 1.0 / 3.0
