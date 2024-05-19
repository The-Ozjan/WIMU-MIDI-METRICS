from wimu10 import metrics_syncopation as sp  # noqa: E402


#calculates syncopation of given file, using model TOB
out = sp.calc_syncopation('TOB','test/B_flat_major.mid')
print(out)
