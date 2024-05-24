from pathlib import Path

from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import metrics_tempo as mt

# Prepare music instance
dataset = 'maestro'
download_muspy_midi(dataset)
path = Path(DATA_RAW_PATH + dataset + '/maestro-v3.0.0/2018/MIDI-Unprocessed_Chamber3_MID--AUDIO_10_R3_2018_wav--2.midi')
file_path = r"C:\Users\Hubert\PycharmProjects\WIMU-MIDI-METRICS\data\known_time_signatures\sonate_27_(c)hisamori-ts34-24.mid"

time_offsets, tempo_marks = mt.find_tempo(file_path)
print(time_offsets, tempo_marks)
