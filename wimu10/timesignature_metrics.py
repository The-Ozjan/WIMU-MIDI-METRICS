import music21 as m21

file_path = r"C:\Users\Hubert\PycharmProjects\WIMU-MIDI-METRICS\data\known_time_signatures\6103d_moonlight_sonata_27-2_3_(nc)smythe-ts44.mid"


def find_time_signature(midi_file_path):
    midi_stream = m21.converter.parse(midi_file_path)
    tsList = midi_stream.flatten().getTimeSignatures()
    return tsList
