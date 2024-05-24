from wimu10 import metrics_tempo as mt


def test_result_len():
    offsets, marks = mt.find_tempo('tests/data/4by4.mid')
    mtList1 = list(zip(offsets, marks))
    offsets, marks = mt.find_tempo('tests/data/2by4-6by8.mid')
    mtList2 = list(zip(offsets, marks))
    offsets, marks = mt.find_tempo('tests/data/3by4-2by4.mid')
    mtList3 = list(zip(offsets, marks))

    assert len(mtList1) == 1
    assert len(mtList2) == 1240
    assert len(mtList3) == 2488


def test_result_element_len():
    offsets, marks = mt.find_tempo('tests/data/4by4.mid')
    mtList1 = list(zip(offsets, marks))
    offsets, marks = mt.find_tempo('tests/data/2by4-6by8.mid')
    mtList2 = list(zip(offsets, marks))
    offsets, marks = mt.find_tempo('tests/data/3by4-2by4.mid')
    mtList3 = list(zip(offsets, marks))
    mtLists = [mtList1, mtList2, mtList3]

    for result in mtLists:
        for element in result:
            assert len(element) == 2


def test_variable_types():
    offsets, marks = mt.find_tempo('tests/data/4by4.mid')
    mtList1 = list(zip(offsets, marks))
    offsets, marks = mt.find_tempo('tests/data/2by4-6by8.mid')
    mtList2 = list(zip(offsets, marks))
    offsets, marks = mt.find_tempo('tests/data/3by4-2by4.mid')
    mtList3 = list(zip(offsets, marks))
    mtLists = [mtList1, mtList2, mtList3]

    for result in mtLists:
        assert isinstance(result, list)
        for element in result:
            assert isinstance(element, tuple)
            for offset, mark in element:
                assert isinstance(offset, float)
                assert isinstance(mark, int)


def test_get_time_signatures():
    offsets, marks = mt.find_tempo('tests/data/4by4.mid')
    mtList1 = list(zip(offsets, marks))
    offsets, marks = mt.find_tempo('tests/data/2by4-6by8.mid')
    mtList2 = list(zip(offsets, marks))
    offsets, marks = mt.find_tempo('tests/data/3by4-2by4.mid')
    mtList3 = list(zip(offsets, marks))

    assert (0.0, 120) in mtList1
    assert (0.0, 100) in mtList2
    assert (722.0, 91) in mtList2
    assert (0.0, 100) in mtList3
    assert (1333.75, 56) in mtList3
