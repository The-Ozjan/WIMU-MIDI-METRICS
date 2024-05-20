import music21 as m21

file_path = r"C:\Users\Hubert\PycharmProjects\WIMU-MIDI-METRICS\data\known_time_signatures\sonate_27_(c)hisamori-ts34-24.mid"


def find_time_signature(midi_file_path):
    midi_stream = m21.converter.parse(midi_file_path)
    tsList = midi_stream.flatten().getTimeSignatures()

    result = []
    for ts in tsList:
        result.append((ts.offset, ts.ratioString))

    return result
