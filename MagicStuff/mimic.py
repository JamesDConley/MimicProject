from pybrain.tools.customxml.networkreader import NetworkReader
from pybrain.structure.modules import LSTMLayer
from pybrain.structure.modules import SoftmaxLayer
from pybrain.structure.modules import SigmoidLayer
import libpyAI as ai
import math

HEADERHERE

class controller:
    
    def __init__(self):
        self.steeringNet = NetworkReader.readFrom('LstmSteeringNetwork.xml')
        self.thrustingNet = NetworkReader.readFrom('LstmThrustingNetwork.xml')
        self.shootingNet = NetworkReader.readFrom('LstmShootingNetwork.xml')
        self.steerInputs = []
        self.thrustInputs = []
        self.shootInputs = []
        
        
    def addInput(self,  input):
        self.steerInputs.append(input)
        self.thrustInputs.append(input)
        self.shootInputs.append(input)
    def addTurnInput(self,  data):
        self.steerInputs.append(data)
    def addThrustInput(self,  data):
        self.thrustInputs.append(data)
    def addShootInput(self,  data):
        self.shootInputs.append(data)
    def resetInputs(self):
        self.steerInputs = []
        self.thrustInputs = []
        self.shootInputs = []
    def printInputs(self):
        print(self.steerInputs)
        print(self.thrustInputs)
        print(self.shootInputs)
    def dummyCode(self):
DUMMYCODEHERE

    def getInputs(self):
REPLACEME
    def act(self):
        if ai.selfAlive():
            self.getInputs()
            #self.printInputs()
            steerOutput = self.steeringNet.activate(self.steerInputs)[0]
            thrustOutput = self.thrustingNet.activate(self.thrustInputs)[0]
            shootOutput = self.shootingNet.activate(self.shootInputs)[0]
            print([steerOutput,  thrustOutput,  shootOutput])
            if steerOutput > .5:
                ai.turnLeft(1)
                ai.turnRight(0)
            else:
                ai.turnRight(1)
                ai.turnLeft(0)
            if thrustOutput > .5:
                ai.thrust(1)
            else :
                ai.thrust(0)
            if shootOutput > .5:
                ai.fireShot()
            self.resetInputs()
        else:
            self.steeringNet.reset()
            self.thrustingNet.reset()
            self.shootingNet.reset()
        
con = controller()
global loopCount,  lastLoop
loopCount = 0
lastLoop = 0
def AI_loop():
    
    if ai.selfAlive():
        
        global loopCount,  lastLoop
        con.act()
        loopCount+=1
        con.dummyCode()
        DataMinerBD.updateInputs()
        DataMinerBD.updateOutputs()
        DataMinerBD.savePair()
        if loopCount % 100 == 0:
            print(loopCount)
        if loopCount > 1000:
            DataMinerBD.writeData()
            ai.quitAI()
        lastLoop = 1
    else:
        if lastLoop == 1:
            DataMinerBD.writeDeath()
    lastLoop = 0
ai.start(AI_loop,["-name","Mimic","-join","localhost"])    
