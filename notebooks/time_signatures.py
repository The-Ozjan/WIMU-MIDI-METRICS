from pathlib import Path

from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import timesignature_metrics as ts

# Prepare music instance
dataset = 'maestro'
download_muspy_midi(dataset)
path = Path(DATA_RAW_PATH + dataset + '/maestro-v3.0.0/2018/MIDI-Unprocessed_Chamber3_MID--AUDIO_10_R3_2018_wav--2.midi')

tsList = ts.find_time_signature(path)
tsList.show('text')