import music21 as m21


def find_tempo(midi_file_path: str):
    """
    Gathers information about music tempo from a MIDI file

    midi_file_path: specify a path to the file you want to analyze

    returns: list of time offsets when the data appears, list of tempo values throughout the file
    """
    midi_stream = m21.converter.parse(midi_file_path)
    metronome = midi_stream.flatten().getElementsByClass(m21.tempo.MetronomeMark)
    offsets = []
    marks = []

    for mark in metronome:
        offsets.append(mark.offset)
        marks.append(mark.number)

    return offsets, marks
