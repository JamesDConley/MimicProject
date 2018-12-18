import sys

configFileHandle = open("xdmConfig.txt",  'r')
configText = configFileHandle.read()

mimicFileHandle = open("mimic.py",  'r')
mimicText = mimicFileHandle.read()
    
newControllerHandle = open("generatedMimic.py",  'w')
newText = mimicText.replace("REPLACEME",  configText)
#newText = newText.replace("DUMMYCODEHERE",  "     print(\"dummy\")")
newFFControllerHandle = open("generatedFFMimic.py", 'w')




newFFControllerHandle.write(newText.replace("Lstm",  "ff"))
insertableString = """
import libpyAI as ai
class BotData:
    def __init__(self,  filename):
        self.fileHandle = open(filename,  'w')
        
        self.turnDR = DataRecorder()
        self.thrustDR = DataRecorder()
        self.shootDR = DataRecorder()
        
        #TurnThrustShoot - that is the order
        self.inputDR = DataRecorder()
        self.outputDR = DataRecorder()
        self.lines = []
        self.turnedLeft,  self.turnedRight,  self.thrusted,  self.shot = 0, 0, 0, 0
    def writeDeath(self):
        self.fileHandle.write("DEAD")
    def length(self):
        return len(self.lines)
    def addInput(self,  data):
        self.turnDR.add(data)
        self.thrustDR.add(data)
        self.shootDR.add(data)
    def addTurnInput(self,  data):
        self.turnDR.add(data)
    def addThrustInput(self,  data):
        self.thrustDR.add(data)
    def addShootInput(self,  data):
        self.shootDR.add(data)
    def updateInputs(self):
        
"""    
insertableString+=configText

insertableString+="""        
    def addOutput(self,  data):
        self.outputDR.add(data)
    def updateOutputs(self):
        self.addOutput(self.turnedLeft)
        self.addOutput(self.turnedRight)
        self.addOutput(self.thrusted)
        self.addOutput(self.shot)
        self.shot = 0
        
    def reset(self):
        self.inputDR.reset()
        self.outputDR.reset()
        
    def resetInput(self):
        self.inputDR.reset()
    def savePair(self):
        self.inputDR.add(self.turnDR.getString())
        self.inputDR.add(self.thrustDR.getString())
        self.inputDR.add(self.shootDR.getString())
        
        self.lines.append(self.inputDR.getString())
        self.lines.append(self.outputDR.getString())
        
        self.turnDR.reset()
        self.thrustDR.reset()
        self.shootDR.reset()
        self.inputDR.reset()
        self.outputDR.reset()
        self.outputDR.reset()
    def deleteData(self,  pairs):
        self.lines = self.lines[0:-2*pairs]
    def writeData(self):
        for line in self.lines:
            self.fileHandle.write(line + "\\n")
    def tturnRight(self, num):
        if num == 1:
            self.turnedRight = 1
            ai.turnRight(1)
        else :
            ai.turnRight(0)
            self.turnedRight = 0
    def tturnRightDummy(self, num):
        if num == 1:
            self.turnedRight = 1
            #ai.turnRight(1)
        else :
            #ai.turnRight(0)
            self.turnedRight = 0
    def tturnLeft(self, num):
        if num == 1:
            self.turnedLeft = 1
            ai.turnLeft(1)
        else:
            ai.turnLeft(0)
            self.turnedLeft = 0
    def tturnLeftDummy(self, num):
        if num == 1:
            self.turnedLeft = 1
            #ai.turnLeft(1)
        else:
            #ai.turnLeft(0)
            self.turnedLeft = 0
    def tthrust(self, num):
        global thrusted
        if num == 1:
            ai.thrust(1)
            self.thrusted = 1
        else:
            ai.thrust(0)
            self.thrusted = 0
    def tthrustDummy(self, num):
        global thrusted
        if num == 1:
            #ai.thrust(1)
            self.thrusted = 1
        else:
            #ai.thrust(0)
            self.thrusted = 0
    def tshoot(self):
        ai.fireShot()
        self.shot = 1
    def tshootDummy(self):
        #ai.fireShot()
        self.shot = 1
class DataRecorder:
    def __init__(self):
        self.baseString = "["
    def reset(self):
        self.baseString = "["
    def add(self,  el):
       self.baseString = self.baseString + str(el) + ","
    def getString(self):
        return self.baseString[0:len(self.baseString)-1] + "]"
"""
loopCode = """
    #Inserted Code
    lastLoop = 0
    if ai.selfAlive():
        lastLoop = 1 
        DataMinerBD.updateInputs()
        DataMinerBD.updateOutputs()
        DataMinerBD.savePair()
        if DataMinerBD.length()%100 == 0:
                print(DataMinerBD.length())
        if DataMinerBD.length() > """ + sys.argv[2] + """:
            DataMinerBD.writeData()
            print("Finished")
            ai.quitAI()
    else:
        if lastLoop == 1:
            DataMinerBD.writeDeath()
"""
insertableString+= "\nDataMinerBD = BotData(\"data.txt\")"
if len(sys.argv) < 2: 
    print("Please run this script with the path to the xpilot bot as the first argument")
    exit()
try:
    ogFileHandle = open(sys.argv[1],  'r')
    ogContents = ogFileHandle.read()
    ogFileHandle.close()
    index = ogContents.find(".start(")
    nextCharacter = "("
    baseIndex = index
    while nextCharacter != "\n":
        index+=1
        nextCharacter = ogContents[index]
    startLine = ogContents[baseIndex:index].replace(" ", "")
    loopName = startLine[7:startLine.index(',')]
    
    loopIndex = ogContents.find("def " + loopName)
    loopStartIndex = ogContents.find("\n",  loopIndex)
    
    
    alteredContents = ogContents[0: loopStartIndex+1] + loopCode + ogContents[loopStartIndex+1:]
    alteredContents = alteredContents.replace(" ai.thrust(",  " DataMinerBD.tthrust(")
    alteredContents = alteredContents.replace(" ai.turnLeft(",  " DataMinerBD.tturnLeft(")
    alteredContents = alteredContents.replace(" ai.turnRight(",  " DataMinerBD.tturnRight(")
    alteredContents = alteredContents.replace(" ai.fireShot(",  " DataMinerBD.tshoot(")
    alteredContents = insertableString + alteredContents
    
    newFileHandle = open("dataGenBot.py",  'w')
    newFileHandle.write(alteredContents)
    #AT THIS POINT - Correctly generated everything but DUMMYCODEHERE is still in the mimic
    
    ogFileHandle = open(sys.argv[1],  'r')
    ogContents = ogFileHandle.read()
    
    
    newAlteredContents = ogContents[0:ogContents.index("ai.start(")] + "dummyLoop()" + ogContents[ogContents.find("\n",  loopIndex)]
    newAlteredContents = newAlteredContents.replace(loopName,  "dummyLoop")
    
    newAlteredContents = '          '.join(newAlteredContents.splitlines(True))
    newAlteredContents = newAlteredContents.replace(" ai.thrust(",  " DataMinerBD.tthrustDummy(")
    newAlteredContents = newAlteredContents.replace(" ai.turnLeft(",  " DataMinerBD.tturnLeftDummy(")
    newAlteredContents = newAlteredContents.replace(" ai.turnRight(",  " DataMinerBD.tturnRightDummy(")
    newAlteredContents = newAlteredContents.replace(" ai.fireShot(",  " DataMinerBD.tshootDummy(")
    mimicFileHandle = open("mimic.py",  'r')
    mimicText = mimicFileHandle.read()
    
    newControllerHandle = open("generatedMimic.py",  'w')
    newText = mimicText.replace("REPLACEME",  configText)
    newText = newText.replace("HEADERHERE", insertableString )
    newText = newText.replace("DUMMYCODEHERE", newAlteredContents)
    newControllerHandle.write(newText)
    
    #Generate the Mimic Code
    
except:
    print("Make sure the paths are valid and you run this script as root")
    
