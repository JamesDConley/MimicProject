#James Conley - January 2018
import libpyAI as ai
import math
lastTurn = 1
def AI_loop():
    global lastTurn
    #Release keys
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeed(45)
    #Set variables"""
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    trackWall = ai.wallFeeler(500,  tracking)
    trackLWall = ai.wallFeeler(500,  tracking+3)
    trackRWall = ai.wallFeeler(500,  tracking - 3)
    frontWall = ai.wallFeeler(500,heading)
    flWall = ai.wallFeeler(500,  heading + 10)
    frWall = ai.wallFeeler(500,  heading - 10)
    leftWall = ai.wallFeeler(500,heading+90)
    rightWall = ai.wallFeeler(500,heading-90)
    trackWall = ai.wallFeeler(500,tracking)
    backWall = ai.wallFeeler(500, heading - 180)
    backLeftWall = ai.wallFeeler(500,  heading - 185)
    backRightWall = ai.wallFeeler(500,  heading - 175)
    speed = ai.selfSpeed()
   
    closest = min(frontWall, leftWall, rightWall, backWall)
    def closestWall(x): #Find the closest Wall
        return {
            frontWall : 1, 
            leftWall : 2, 
            rightWall : 3, 
            backWall : 4, 
            flWall : 5, 
            frWall : 6, 
        }[x]
    wallNum = closestWall(closest)
    
    #Code for finding the angle to the closest ship
    target = ai.closestShipId()
    targetX,  targetY = ai.screenEnemyX(0), ai.screenEnemyY(0)
    calcDir = 0
    
    if targetX- ai.selfX() != 0:
        calcDir = (math.degrees(math.atan2((targetY - ai.selfY()), (targetX- ai.selfX()))) + 360)%360
    targetDir = calcDir
    crashWall = min(trackWall,  trackLWall,  trackRWall) #The wall we are likely to crash into if we continue on our current course
    #Rules for turning
    if crashWall > 25*speed and closest > 30 and targetX != -1:  #If we are far enough away from a predicted crash and no closer than 25 pixels to a wall, and there isn't a wall between us and the closest enemy
        #print("Aiming",  targetDir,  " Current",  heading)
        diff = (calcDir - heading)
        if ai.shotAlert(0) > -1 and ai.shotAlert(0) < 35:
            ai.turnRight(1)
            ai.thrust(1)
        elif diff >= 0:
            if diff >= 180:
                a = 0
                ai.turnRight(1)     #If the target is to our right- turn right
            elif diff != 0 :              
                a = 0
                
                ai.turnLeft(1)      #If the target is to our left - turn left
        else :
            if diff > -180:
                a = 0
                ai.turnRight(1)     #If the target is to our right - turn right
            else :
                a = 0
                ai.turnLeft(1)      #If the target is to our left - turn left
    else : #Rules for avoiding death
       # if crashWall/ai.selfSpeed() > ai.closestShot() :
       #We find a target heading using our current trajectory and the closest wall then turn in it's direction
        targetHeading = heading
        print(heading)
        if wallNum == 1or wallNum == 6 or wallNum == 5:    #Front Wall is Closest
            if lastTurn == 1:
                targetHeading += 270
                targetHeading = (targetHeading)%360
            else :
                targetHeading +=90
                targetHeading = targetHeading%360
            
            print("front")
        elif wallNum == 2  :  # Left Wall is Closest
            targetHeading += 270
            targetHeading = (targetHeading)%360
            lastTurn = 1
            print("leftwall")
        elif wallNum == 3  :
            targetHeading = targetHeading + 90
            targetHeading = (targetHeading)%360
            lastTurn = 2
            print("rightWall")
        else :
            if backLeftWall < backRightWall:
                lastTurn = 2
                targetHeading += 5
                targetHeading = (targetHeading)%360
            if backLeftWall > backRightWall:
                lastTurn = 1
                targetHeading -= 5
                targetHeading = (targetHeading)%360
       
        speedConcern = ai.selfSpeed() - 4
        
        if speedConcern < 0:
            speedConcern = 0
        elif speedConcern > 5:
            speedConcern = 5
        
        #targetHeading = (targetHeading*(1-(speedConcern/5))) + (((tracking+170)%360)*(speedConcern/5))
        if speedConcern > 2:
            targetHeading = (tracking + 180)%360
        
        diff = (targetHeading - heading)
        print("targetHEading : ", targetHeading,  " heading : ",  heading)
        if diff >= 0:
            if diff >= 180:
                ai.turnRight(1)     #If the targetHEading is to our right- turn right
                
                print("right")
            elif diff != 0 :                       
                ai.turnLeft(1)      #If the targeHeadingt is to our left - turn left
                print("left")
        else :
            if diff > -180:
                print("right")
                ai.turnRight(1)     #If the targetHeading is to our right - turn right
                #print("right")
            else :
                print("left")
                ai.turnLeft(1)      #If the targetHeading is to our left - turn left
            #print("nice")
    
    #Rules for thrusting
    
    if speed < 5 and frontWall > 200:   #If we are moving slowly and we won't ram into anything, accelerate
        ai.thrust(1)
    elif crashWall < 25*speed  and (abs(tracking - heading) > 120):  #If we are getting close to a wall, and we can thrust away from it, do so
        ai.thrust(1)
    elif backWall < 30: #If there is a wall very close behind us, get away from it
        ai.thrust(1)
    
    if abs(calcDir - heading) < 15 : #If we are close to the current proper trajectory for a shot then fire
        ai.fireShot()
    
    #"""

ai.start(AI_loop,["-name","smarto","-join","localhost"])    



