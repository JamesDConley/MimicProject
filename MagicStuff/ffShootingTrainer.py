from pybrain.datasets import SequentialDataSet
from itertools import cycle
from pybrain.tools.customxml.networkwriter import NetworkWriter
import sys
fileName  = sys.argv[1]
myFile = open(fileName,  "r")
lines = myFile.readlines()
inputData = []
outputData = []

for line in lines:
    allData = (eval(line))
    if len(allData) == 4:
        outputData.append([allData[3]])
    else:
        inputData.append(allData[2])
inputSize = len(inputData[0])
outputSize = len(outputData[0])


ds = SequentialDataSet(inputSize, outputSize)    
for i in range(0, len(outputData)):
    ds.addSample(inputData[i], outputData[i])

    
   
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import LSTMLayer
from pybrain.structure.modules import SigmoidLayer

net = buildNetwork(inputSize, inputSize, outputSize, 
                   hiddenclass=LSTMLayer,  outclass = SigmoidLayer,  outputbias=False, recurrent=True)
                   
from pybrain.supervised import RPropMinusTrainer
from sys import stdout


trainer = RPropMinusTrainer(net, dataset=ds)
train_errors = [] # save errors for plotting later
EPOCHS_PER_CYCLE = 5
CYCLES = int(sys.argv[2])
EPOCHS = EPOCHS_PER_CYCLE * CYCLES

import matplotlib.pyplot as plt
plt.xlabel('Training Epoch')
plt.ylabel('Shooting Error')
plt.ion()
plt.show()

for i in range(CYCLES):
    trainer.trainEpochs(EPOCHS_PER_CYCLE)
    train_errors.append(trainer.testOnData())
    epoch = (i+1) * EPOCHS_PER_CYCLE
    print("\r epoch {}/{}".format(epoch, EPOCHS), end="")
    print(" Shooting Error = \t",  train_errors[-1])
    stdout.flush()
    plt.plot(range(0, len(train_errors)), train_errors)
    plt.draw()
    plt.pause(0.0001)
    stdout.flush()
#train_errors = trainer.trainUntilConvergence()
print()
print("final error =", train_errors[-1])


NetworkWriter.writeToFile(net, 'ffShootingNetwork.xml')


