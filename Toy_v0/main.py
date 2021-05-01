# simple run

from Model import SimModel

model = SimModel(51,51)
for i in range(30):
    model.step()
