from pathlib import Path
from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import metrics_tempo as mt
import matplotlib.pyplot as plt

# Prepare music instance
dataset = 'maestro'
download_muspy_midi(dataset)
path = Path(DATA_RAW_PATH + dataset + '/maestro-v3.0.0/2018/MIDI-Unprocessed_Chamber3_MID--AUDIO_10_R3_2018_wav--2.midi')

time_offsets, tempo_marks = mt.find_tempo(path)
results = list(zip(time_offsets, tempo_marks))
print(results)

plt.plot(time_offsets, tempo_marks)
plt.grid()
plt.xlabel("Czas")
plt.ylabel("BPM")
plt.show()
