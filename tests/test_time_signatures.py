from wimu10 import metrics_time_signature as ts
import music21 as m21


def test_result_len():
    tsList1 = ts.find_time_signature('tests/data/4by4.mid')
    tsList2 = ts.find_time_signature('tests/data/2by4-6by8.mid')
    tsList3 = ts.find_time_signature('tests/data/3by4-2by4.mid')
    assert len(tsList1) == 1
    assert len(tsList2) == 8
    assert len(tsList3) == 8


def test_result_element_len():
    tsList1 = ts.find_time_signature('tests/data/4by4.mid')
    tsList2 = ts.find_time_signature('tests/data/2by4-6by8.mid')
    tsList3 = ts.find_time_signature('tests/data/3by4-2by4.mid')
    tsLists = [tsList1, tsList2, tsList3]

    for result in tsLists:
        for element in result:
            assert len(element) == 2


def test_variable_types():
    tsList1 = ts.find_time_signature('tests/data/4by4.mid')
    tsList2 = ts.find_time_signature('tests/data/2by4-6by8.mid')
    tsList3 = ts.find_time_signature('tests/data/3by4-2by4.mid')
    tsLists = [tsList1, tsList2, tsList3]

    for result in tsLists:
        assert isinstance(result, list)
        for element in result:
            assert isinstance(element, tuple)
            for offset, time_signature in element:
                assert isinstance(offset, float)
                assert isinstance(time_signature, str)


def test_get_time_signatures():
    tsList1 = ts.find_time_signature('tests/data/4by4.mid')
    tsList2 = ts.find_time_signature('tests/data/2by4-6by8.mid')
    tsList3 = ts.find_time_signature('tests/data/3by4-2by4.mid')
    assert (0.0, '4/4') in tsList1
    assert (0.0, '2/4') in tsList2
    assert (224.0, '6/8') in tsList2
    assert (0.0, '3/4') in tsList3
    assert (753.0, '2/4') in tsList3
