import music21 as mus

file_path = r"./data/known_time_signatures/6103d_moonlight_sonata_27-2_3_(nc)smythe-ts34.mid"


def find_time_signature(midi_file_path):
    midi_stream = mus.converter.parse(midi_file_path)
    tsList = midi_stream.flatten().getTimeSignatures()
    return tsList


tsList = find_time_signature(file_path)
tsList.show('text')