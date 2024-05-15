import matplotlib.pyplot as plt
from syncopation import calculate_syncopation
from readmidi import MidiFile, get_bars_from_midi, read_midi_file
from copy import deepcopy


def syncopation_plot(synp_per_bar: list[float]) -> None:
    x = range(len(synp_per_bar))
    plt.bar(x, synp_per_bar)
    plt.title('Wykres siły synkopy')
    plt.xlabel('takty')
    plt.ylabel('Siła synkopy')
    plt.show()

    return

# def calc_syncopation(model, file_path: str, parameters=None, outfile=None, barRange=None, debugPrint=False):

#     output = []
#     midi_music = read_midi_file(file_path)
#     # tracks = deepcopy(midi_music.tracks)
#     # for track in tracks:
#     #     midi_music.tracks = [track]
#     #     midi_music.format = 0
#     barlist = get_bars_from_midi(midi_music)
#     output.append(calculate_syncopation(model, barlist, parameters, outfile, barRange, debugPrint))

#     return output

# if __name__ == '__main__':
#     out = calc_syncopation(None,'test_files/F_major.mid')
#     print('done')
