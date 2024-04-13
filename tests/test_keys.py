import muspy as mp
import numpy as np
from wimu10 import metrics_key as mk
import mido
import music21 as m21


def test_keys_from_sample_midi():
    music = mido.MidiFile('tests/data/some_repeats.mid')
    l1 = mk.get_keys_from_sampled_midi(music, sample_duration=5)
    l2 = mk.get_keys_from_sampled_midi(music, sample_duration=5)
    assert len(l1) == len(l2)
    print(l1, l2)
    assert l2[-1][0] == l1[-1][0]
    assert l2[0][0] == l1[0][0]


def test_get_key_from_music21_stream():
    music = m21.converter.parse('tests/data/some_repeats.mid')
    ret = mk.get_key_from_music21_stream(music)
    assert ret[0] == "a minor"
    assert isinstance(ret[1][0], float)

def test_get_key_from_music21_stream_krumhansl():
    music = m21.converter.parse('tests/data/some_repeats.mid')
    ret = mk.get_key_from_music21_stream(music, alg_name="key.krumhansl")
    assert ret[0] == "C major"
    assert isinstance(ret[1][0], float)

def test_get_key_from_music21_stream_bellman():
    music = m21.converter.parse('tests/data/some_repeats.mid')
    ret = mk.get_key_from_music21_stream(music, alg_name="key.bellman")
    assert ret[0] == "a minor"
    assert isinstance(ret[1][0], float)

def test_get_key_from_music21_stream_simple():
    music = m21.converter.parse('tests/data/some_repeats.mid')
    ret = mk.get_key_from_music21_stream(music, alg_name="key.simple")
    assert ret[0] == "C major"
    assert isinstance(ret[1][0], float)

def test_get_key_from_music21_stream_bellman():
    music = m21.converter.parse('tests/data/some_repeats.mid')
    ret = mk.get_key_from_music21_stream(music, alg_name="key.temperley")
    assert ret[0] == "a minor"
    assert isinstance(ret[1][0], float)

def test_get_key_from_muspy_music():
    music = mp.read_midi('tests/data/some_repeats.mid')
    ret = mk.get_key_from_muspy_music(music)
    assert ret[0] == "a minor"
    assert isinstance(ret[1][0], float)

def test_get_key_from_muspy_music_krumhansl():
    music = mp.read_midi('tests/data/some_repeats.mid')
    ret = mk.get_key_from_muspy_music(music, alg_name="key.krumhansl")
    assert ret[0] == "C major"
    assert isinstance(ret[1][0], float)

def test_compute_key_signatures_hist():
    key_list = [("C major", 0), ("C minor", 10), ("A major", 20), ("D minor", 30), ("C major", 40)
                , ("A major", 50), ("A major", 60), ("C minor", 70)]
    list_keys, list_names = mk.compute_key_signatures_hist(key_list)
    assert len(list_keys) == 4
    assert list_keys[0] == 2
    assert list_keys[1] == 2
    assert list_keys[2] == 3
    assert list_keys[3] == 1
    assert list_names[0] == "C major"
    assert list_names[1] == "C minor"
    assert list_names[2] == "A major"
    assert list_names[3] == "D minor"
