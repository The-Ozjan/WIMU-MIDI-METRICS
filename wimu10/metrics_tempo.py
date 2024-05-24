import music21 as m21

file_path = r"C:\Users\Hubert\PycharmProjects\WIMU-MIDI-METRICS\data\known_time_signatures\sonate_27_(c)hisamori-ts34-24.mid"


def find_tempo(midi_file_path):
    midi_stream = m21.converter.parse(midi_file_path)
    metronome = midi_stream.flatten().getElementsByClass(m21.tempo.MetronomeMark)
    offsets = []
    marks = []

    for mark in metronome:
        offsets.append(mark.offset)
        marks.append(mark.number)

    return offsets, marks
