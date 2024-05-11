import syncopation as s
import LHL, PRS, SG, TMC, TOB, WNBD

models = [LHL, PRS, SG, TMC, TOB, WNBD]

outs1 = []
outs2 = []
for i in range(len(models)):
    filename = 'model' + str(i) + '.json'
    out = s.calculate_syncopation(models[i], 'test.rhy')
    outs1.append(out['syncopation_by_bar'])
    # out = s.calculate_syncopation(models[i], 'test2.mid')
    # outs2.append(out['syncopation_by_bar'])

for i in range(len(outs1)):
    print("model", i, outs1[i])#, [x - y for x, y in zip(outs2[i], outs1[i])])
