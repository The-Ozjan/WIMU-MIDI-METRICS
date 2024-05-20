import music21 as m21
import muspy as mp
from pathlib import Path
from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import metrics_key as mk
import mido
import matplotlib.pyplot as plt
import numpy as np
import os
import copy

# Parameters
dataset = 'maestro'
folder = '/maestro-v3.0.0/2018'
files = range(0, 3)
is_hist = True
is_multiple_keys = True
is_keys_different_alg = True
alg = 'key.aarden'
step = 30.0
path_for_hist = Path('data/midi_with_keys/C_major.mid')

# Prepare music instance
download_muspy_midi(dataset)
# path1 = Path(DATA_RAW_PATH + dataset + '/_converted/0001.json')
path = Path(DATA_RAW_PATH + dataset + '/maestro-v3.0.0/2018/MIDI-Unprocessed_Chamber3_MID--AUDIO_10_R3_2018_wav--2.midi')
path2 = Path(DATA_RAW_PATH + dataset + '/maestro-v3.0.0/2018/MIDI-Unprocessed_Chamber6_MID--AUDIO_20_R3_2018_wav--2.midi')

# Creating histogram
if is_hist:
    list_for_hist = mk.get_keys_from_sampled_midi(mido.MidiFile(path_for_hist), sample_duration=step, alg_name=alg)
    hist, lab = mk.compute_key_signatures_hist(list_for_hist)
    plt.bar(lab, hist)
    plt.xticks(rotation=45)
    plt.show()

# Creating heatmap
if is_multiple_keys:
    dataset_path = 'data/midi_with_keys'
    dir_list = os.listdir(Path(dataset_path))
    tracks_keys = []
    for file in files:
        p = Path(dataset_path + '/' + dir_list[file])
        key_list = mk.get_keys_from_sampled_midi(mido.MidiFile(p), sample_duration=step, alg_name=alg)
        tracks_keys.append(key_list)

    labels = mk.ALL_KEY_NOTE.keys()
    fig, ax = plt.subplots(nrows=1, ncols=2)

    # Plot Heatmap for keys in track matrix
    matrix = mk.keys_in_tracks_matrix(tracks_keys)
    im = ax[0].imshow(matrix)
    ax[0].figure.colorbar(im, ax=ax[0])
    ax[0].set_yticks(np.arange(len(labels)), labels=labels)
    ax[0].set_xticks(np.arange(len(dir_list[0: max(files)+1])), labels=dir_list[0: max(files)+1])
    plt.setp(ax[0].get_xticklabels(), rotation=90, ha='right', rotation_mode='anchor')
    ax[0].invert_yaxis()
    ax[0].set_title('Keys in tracks heatmap')

    # Similatity matrix
    similarity_matrix = mk.key_similarity_matrix(tracks_keys)
    im2 = ax[1].imshow(similarity_matrix)
    ax[1].figure.colorbar(im2, ax=ax[1])
    ax[1].set_xticks(np.arange(len(dir_list[0: max(files)+1])), labels=dir_list[0: max(files)+1])
    ax[1].set_yticks(np.arange(len(dir_list[0: max(files)+1])), labels=dir_list[0: max(files)+1])
    plt.setp(ax[1].get_xticklabels(), rotation=90, ha='right', rotation_mode='anchor')
    ax[1].invert_yaxis()
    ax[1].set_title('Keys similarity in tracks heatmap')
    plt.show()

if is_keys_different_alg:
    music_list = []
    dir_list = os.listdir(Path(DATA_RAW_PATH + dataset + folder))
    for file in files:
        p = Path(DATA_RAW_PATH + dataset + folder + '/' + dir_list[file])
        music_list.append(mp.read_midi(p))
    
    matrix = mk.diff_alg_keys_music_list(music_list)

    labels = mk.ALL_KEY_NOTE.keys()
    fig, ax = plt.subplots(nrows=1, ncols=2)
    # Plot Heatmap for key by different alg in track matrix
    im = ax[0].imshow(matrix)
    ax[0].figure.colorbar(im, ax=ax[0])
    ax[0].set_yticks(np.arange(len(labels)), labels=labels)
    ax[0].set_xticks(np.arange(len(dir_list[0: max(files)+1])), labels=dir_list[0: max(files)+1])
    plt.setp(ax[0].get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
    ax[0].invert_yaxis()
    ax[0].set_title('Key by different alg in tracks heatmap')


    #  matrix
    matrix_key = mk.key_for_whole_music_matrix(music_list)
    im2 = ax[1].imshow(matrix_key)
    ax[1].figure.colorbar(im2, ax=ax[1])
    ax[1].set_xticks(np.arange(len(dir_list[0: max(files)+1])), labels=dir_list[0: max(files)+1])
    ax[1].set_yticks(np.arange(len(labels)), labels=labels)
    plt.setp(ax[1].get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
    ax[1].invert_yaxis()
    ax[1].set_title('Key in tracks heatmap')
    plt.show()