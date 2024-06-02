from wimu10 import metrics_syncopation as sp
import pytest
import numpy as np


def test_wrong_model():
    with pytest.raises(Exception, match='Chosen model do not exist!'):
        sp.calc_syncopation('aaa', 'tests/data/syncopation/test4.mid')

def test_invalid_file():
    with pytest.raises(Exception, match='Midi file is not valid!'):
        sp.calc_syncopation('TOB', 'tests/data/syncopation/test3.rhy')

def test_multitrack_wrong_model():
    for model in sp.SYNCOPATION_MODELS:
        if model == 'TOB' or model == 'WNBD':
            continue
        with pytest.raises(Exception, match='Chosen model do not accept multi-track files! Choose TOB or WNBD instead.'):
            sp.calc_syncopation(model, 'tests/data/syncopation/test32.mid')

def test_multitrack():
    out = sp.calc_syncopation('TOB', 'tests/data/syncopation/test32.mid')
    assert len(out['syncopation_by_bar']) == out['number_of_bars']
    out = sp.calc_syncopation('WNBD', 'tests/data/syncopation/test32.mid')
    assert len(out['syncopation_by_bar']) == out['number_of_bars']




def test_4_4_all_models():
    """ First 4 bars in test file have intentionally no or little syncopation.
        (different models might interpret them slightly different)
        Mean syncopation of first 4 bars should me significantly lower than the rest.
    """
    for model in sp.SYNCOPATION_MODELS:
        out = sp.calc_syncopation(model, 'tests/data/syncopation/test3.mid')
        bars = out['syncopation_by_bar']
        assert np.mean(bars[:4]) < np.mean(bars[4:])
    return

def test_3_4():
    """ First 4 bars in test file have intentionally no or little syncopation.
        (different models might interpret them slightly different)
        Mean syncopation of first 4 bars should me significantly lower than the rest.
    """
    out = sp.calc_syncopation('TOB', 'tests/data/syncopation/test4.mid')
    bars = out['syncopation_by_bar']
    assert np.mean(bars[:4]) < np.mean(bars[4:])
    out = sp.calc_syncopation('WNBD', 'tests/data/syncopation/test4.mid')
    bars = out['syncopation_by_bar']
    assert np.mean(bars[:4]) < np.mean(bars[4:])


def test_6_8():
    """ First 4 bars in test file have intentionally no or little syncopation.
        (different models might interpret them slightly different)
        Mean syncopation of first 4 bars should me significantly lower than the rest.
    """
    out = sp.calc_syncopation('TOB', 'tests/data/syncopation/test6.mid')
    bars = out['syncopation_by_bar']
    assert np.mean(bars[:4]) < np.mean(bars[4:])
    out = sp.calc_syncopation('WNBD', 'tests/data/syncopation/test6.mid')
    bars = out['syncopation_by_bar']
    assert np.mean(bars[:4]) < np.mean(bars[4:])

