import syncopation as s
import LHL, PRS, SG, TMC, TOB, WNBD  # noqa: E401
from metrics_syncopation import syncopation_by_bar_plot

models = [LHL, PRS, SG, TMC, TOB, WNBD]
models = [TOB, WNBD]

outs1 = []
outs2 = []
for i in range(len(models)):
    filename = 'model' + str(i) + '.json'
    # out = s.calculate_syncopation(models[i], 'synpy/test_files/C_major.mid')
    out = s.calculate_syncopation(models[i], 'test_files/F_major.mid')
    outs1.append(out['syncopation_by_bar'])
    # out = s.calculate_syncopation(models[i], 'test2.mid')
    # outs2.append(out['syncopation_by_bar'])

syncopation_by_bar_plot(outs1[1])
print(len(outs1[0]))
for i in range(len(outs1)):
    print("model", i, outs1[i])#, [x - y for x, y in zip(outs2[i], outs1[i])])
