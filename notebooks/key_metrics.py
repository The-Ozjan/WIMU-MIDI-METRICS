import music21 as m21
import muspy as mp
from pathlib import Path

from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import metrics_key as mk

# file_path2 = f'data\\raw\maestro\maestro-v3.0.0\{2018}\MIDI-Unprocessed_Schubert7-9_MID--AUDIO_16_R2_2018_wav.midi'
# path = 'data/processed/dynamicsrand/dynamicsrand-003.mid'

# Prepare music instance
dataset = 'maestro'
download_muspy_midi(dataset)
# path = Path(DATA_RAW_PATH + dataset + '/_converted/0001.json')
path = Path(DATA_RAW_PATH + dataset + '/maestro-v3.0.0/2018/MIDI-Unprocessed_Chamber3_MID--AUDIO_10_R3_2018_wav--2.midi')
# music = mp.load_json(path)

midi_stream = m21.converter.parse(path)

a, b = mk.get_key_from_music21_stream(midi_stream.measures(0, 20, collect='TimeSignature'))
print(a)

track = mp.read_midi(path,backend="pretty_midi")
# track = mp.load_json(path)
strin11 = mp.to_music21(track)
print('aaala ', strin11.analyze('key'))
print(mk.get_key_from_muspy_music(track))
print(mk.compute_key_signatures_hist(track))
# print(mk.similarity_key_score(track2, track))
print(track.key_signatures)
# print(mk.key_similarity_matrix([track, track2, track, track2]))
# print(mk.keys_in_tracks_matrix([track, track, track2, track2]))
