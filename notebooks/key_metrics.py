import music21 as m21
import muspy as mp
from pathlib import Path
from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import metrics_key as mk
import mido
import matplotlib.pyplot as plt

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
strin11 = mp.to_music21(track)
print('aaala ', strin11.analyze('key'))
print(mk.get_key_from_muspy_music(track))
print(track.key_signatures)

mid = mido.MidiFile(path)
key_list = mk.get_keys_from_sampled_midi(mid, sample_duration= 10.0, only_change=True)
print(key_list)
y, x = mk.compute_key_signatures_hist(key_list)
print(y)
print(x)
