from wimu10 import metrics_syncopation as sp


if __name__ == '__main__':
#calculates syncopation of given file, using model TOB
    out = sp.calc_syncopation('TOB','data/midi_with_keys/B_flat_major.mid')
    sp.syncopation_metrics_chart(out)
    sp.syncopation_by_bar_plot(out)
