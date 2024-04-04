import music21 as m21
import muspy as mp
from pathlib import Path
from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import metrics_key as mk
import mido
import matplotlib.pyplot as plt
import numpy as np
import os

# Prepare music instance
dataset = 'maestro'
folder = '/maestro-v3.0.0/2018'
files = range(0, 10)
download_muspy_midi(dataset)
#path1 = Path(DATA_RAW_PATH + dataset + '/_converted/0001.json')
path = Path(DATA_RAW_PATH + dataset + '/maestro-v3.0.0/2018/MIDI-Unprocessed_Chamber3_MID--AUDIO_10_R3_2018_wav--2.midi')
path2 = Path(DATA_RAW_PATH + dataset + '/maestro-v3.0.0/2018/MIDI-Unprocessed_Chamber6_MID--AUDIO_20_R3_2018_wav--2.midi')
#music = mp.load_json(path1)


midi_stream = m21.converter.parse(path)
# measures()
a, b = mk.get_key_from_music21_stream(midi_stream.measures(0, 20, collect='TimeSignature'))
print(a)
# 
track = mp.read_midi(path)
strin11 = mp.to_music21(track)
print(mk.get_key_from_muspy_music(track))
print(track.key_signatures)

# Creating heatmap
dataset_path = Path(DATA_RAW_PATH + dataset + folder)
dir_list = os.listdir(dataset_path)
tracks_keys = []
for file in files:
    p = Path(DATA_RAW_PATH + dataset + folder +'/'+dir_list[file])
    key_list = mk.get_keys_from_sampled_midi(mido.MidiFile(p), sample_duration=40.0)
    tracks_keys.append(key_list)

labels = mk.ALL_KEY_NOTE.keys()
fig, ax = plt.subplots(nrows=1, ncols=2)
# Plot Heatmap for transition matrix
matrix = mk.keys_in_tracks_matrix(tracks_keys)
im = ax[0].imshow(matrix)
ax[0].figure.colorbar(im, ax=ax[0])
#ax[0].set_xticks(np.arange(len(labels)), labels=labels)
ax[0].set_yticks(np.arange(len(labels)), labels=labels)
plt.setp(ax[0].get_xticklabels(), rotation=90, ha='right', rotation_mode='anchor')
ax[0].invert_yaxis()
ax[0].set_title('Chord transition heatmap')
plt.show()