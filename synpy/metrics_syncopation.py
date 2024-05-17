import matplotlib.pyplot as plt
from syncopation import calculate_syncopation
from readmidi import MidiFile, get_bars_from_midi, read_midi_file
from copy import deepcopy
import LHL, PRS, SG, TMC, TOB, WNBD  # noqa: E401
import numpy as np

SYNCOPATION_DATA = dict[str]

def syncopation_by_bar_plot(data: SYNCOPATION_DATA) -> None:
    y = data['syncopation_by_bar']
    x = range(len(y))
    plt.bar(x, y)
    plt.title('Syncopation by bar')
    plt.xlabel('Bars')
    plt.ylabel('Syncopation strength')
    plt.show()
    return

def syncopation_metrics_chart(data: SYNCOPATION_DATA) -> None:
    max_syncopation = max(data['syncopation_by_bar'])
    bars_with_syncopation = len([i for i in data['syncopation_by_bar'] if i != 0])
    bars_with_syncopation_percent = 100 * bars_with_syncopation / data['number_of_bars']
    mean_non_zero_syncopation = data['summed_syncopation'] / bars_with_syncopation

    x = ['max', 'mean of non-zero', 'mean']
    y = [max_syncopation, mean_non_zero_syncopation, data['mean_syncopation_per_bar']]

    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5), gridspec_kw={'height_ratios': [3, 1]})
    ax1.bar(x, y)
    ax2.barh(1, bars_with_syncopation_percent)
    ax2.set_yticks([1])
    ax2.set_yticklabels([''])
    ax2.set_xticks(range(0,105,5))
    ax2.set_xlabel('Bars with non-zero syncopation (%)')
    plt.tight_layout()
    plt.show()
    return

def calc_syncopation(model, file_path: str, parameters=None, outfile=None, barRange=None, debugPrint=False) -> SYNCOPATION_DATA:

    # output = []
    midi_music = read_midi_file(file_path)
    # tracks = deepcopy(midi_music.tracks)
    # for track in tracks:
    #     midi_music.tracks = [track]
    #     midi_music.format = 0
    barlist = get_bars_from_midi(midi_music)
    # output.append(calculate_syncopation(model, barlist, parameters, outfile, barRange, debugPrint))
    output = calculate_syncopation(model, barlist, parameters, outfile, barRange, debugPrint)

    return output

if __name__ == '__main__':
    out = calc_syncopation(TOB,'test_files/B_flat_major.mid')
    syncopation_metrics_chart(out)
    syncopation_by_bar_plot(out)
