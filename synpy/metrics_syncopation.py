import matplotlib.pyplot as plt
from syncopation import calculate_syncopation
from readmidi import get_bars_from_midi, read_midi_file
import LHL, PRS, SG, TMC, TOB, WNBD  # noqa: E401
import mido

SYNCOPATION_DATA = dict[str]

SYNCOPATION_MODELS = {
    'LHL': LHL,
    'PRS': PRS,
    'SG': SG,
    'TMC': TMC,
    'TOB': TOB,
    'WNBD': WNBD
}


def calc_syncopation(model: str, file_path: str, parameters=None, outfile: str=None, debugPrint: bool=False) -> SYNCOPATION_DATA:

    if model not in SYNCOPATION_MODELS:
        raise(Exception('Chosen model do not exist!'))

    try:
        midi_music = read_midi_file(file_path)
    except (Exception):
        raise(Exception('Midi file is not valid!')) from None

    if len(midi_music.tracks) > 1 and model != 'TOB' and model != 'WNBD':
        raise(Exception('Chosen model do not accept multi-track files! Choose TOB or WNBD instead.'))

    barlist = get_bars_from_midi(midi_music)
    output = calculate_syncopation(SYNCOPATION_MODELS[model], source=barlist, parameters=parameters, outfile=outfile, debugPrint=debugPrint)

    return output

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

if __name__ == '__main__':
    out = calc_syncopation('TOB','test/B_flat_major.mid')
    syncopation_metrics_chart(out)
    syncopation_by_bar_plot(out)
