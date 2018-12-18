#James Conley - January 2018
import libpyAI as ai
import math




global maxSpeed,  shotAngle,  wallClose
maxSpeed = 5
shotAngle = 9
wallClose = 15






previousScore = 0
def AI_loop():
    global maxSpeed,  shotAngle,  wallClose,  dead,  previousScore
    global turnedLeft,  turnedRight,  thrusted,  shot
    
    
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
    llWall = ai.wallFeeler(500,  heading + 100)
    rlWall = ai.wallFeeler(500,  heading + 80)
    
    rightWall = ai.wallFeeler(500,heading-90)
    lrWall = ai.wallFeeler(500,  heading - 80)
    rrWall = ai.wallFeeler(500,  heading - 100)
    
    trackWall = ai.wallFeeler(500,tracking)
    backWall = ai.wallFeeler(500, heading - 180)
    backLeftWall = ai.wallFeeler(500,  heading - 190)
    backRightWall = ai.wallFeeler(500,  heading - 170)
    speed = ai.selfSpeed()
    
   
    
    closest = min(frontWall, leftWall, rightWall, backWall,  flWall,  frWall)
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
    targetX,  targetY = ai.screenEnemyX(0), ai.screenEnemyY(0)
   
   
    #baseString = "["+str(flWall/500)+","+str(frontWall/500)+","+str(frWall/500) + "," + str(backLeftWall/500) + "," + str(backWall/500) + "," + str(backRightWall/500) + ","+str(leftWall/500)+","+str(rightWall/500)+","+str(trackLWall/500) + "," + str(trackWall/500) + ","+str(trackRWall/500) + "," + str(speed/10)
    
    calcDir = -1
    if targetX- ai.selfX() != 0:
        calcDir = (math.degrees(math.atan2((targetY - ai.selfY()), (targetX- ai.selfX()))) + 360)%360
    crashWall = min(trackWall,  trackLWall,  trackRWall) #The wall we are likely to crash into if we continue on our current course
    #Rules for turning
    if crashWall > wallClose*speed and closest > 25 and targetX != -1:  #If we are far enough away from a predicted crash and no closer than 25 pixels to a wall we can try and aim and kill them
        diff = (calcDir - heading)
        #if ai.shotAlert(0) > -1 and ai.shotAlert(0) < 35:   #If we are about to get shot
        #    tturnRight(1)                                                     #Screw aiming and turn right and thrust
        #    tthrust(1)                                                            #This is arguably a horrible strategy because our sideways profile is much larger, but it's required for the grade
        if diff >= 0:
            if diff >= 180:
                ai.turnRight(1)     #If the target is to our right- turn right
               
            else :                       
                ai.turnLeft(1)      #If the target is to our left - turn left
                
        else :
            if diff > -180:
                ai.turnRight(1)     #If the target is to our right - turn right
               
            else :
                ai.turnLeft(1)      #If the target is to our left - turn left
             
    else : #Rules for avoiding death
       # if crashWall/ai.selfSpeed() > ai.closestShot() :
        if wallNum == 1 or wallNum == 5 or wallNum == 6:    #Front Wall is Closest (Turn Away From It)
            ai.turnLeft(1)
           
        elif wallNum == 2 :  # Left Wall is Closest (Turn Away From It)
            ai.turnRight(1)
            
        elif wallNum == 3 :   #Right Wall is Closest (Turn Away From It)
            ai.turnLeft(1)
           
        else :                                                      #Back Wall is closest- turn so that we are facing directly away from it
            if backLeftWall < backRightWall:
               ai.turnRight(1)                                  #We need to turn right to face more directly away from it
              
              
            if backLeftWall > backRightWall:        # We need to turn left to face more directly away from it
               ai.turnLeft(1)
              
       
       
    
    #Rules for thrusting
    
    if speed < maxSpeed and frontWall > 100:   #If we are moving slowly and we won't ram into anything, accelerate
        ai.thrust(1)
    elif trackWall < 200  and (ai.angleDiff(heading,  tracking) > 120):  #If we are getting close to a wall, and we can thrust away from it, do so
        ai.thrust(1)
    elif backWall < 20: #If there is a wall very close behind us, get away from it
        ai.thrust(1)
    
    if abs(calcDir - heading) < shotAngle and calcDir != -1: #If we are close to the current proper trajectory for a shot then fire
        ai.fireShot()
   
    previousScore = ai.selfScore()
   

ai.start(AI_loop,["-name","OGAsmarto1","-join","localhost"])    




