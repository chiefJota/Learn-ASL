import pickle
import pygame
import sys
sys.path.insert(0, '../..')
import Leap
from pygameWindow_Del03 import PYGAME_WINDOW
import constants as constants

import numpy as np
import handDirection
import random
import time

from math import pi

##########################################
def login():
    global database
    global userRecord
    global userName
   
    #load database from pickled file
    database = pickle.load(open('/Users/chief/Desktop/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/CS228/Del10/userData/database.p','rb'))

    userName = raw_input("Please enter your name: ")
    #returning user
    if userName in database:
        #welcome back kid
        print("welcome back " + userName + ".")  
        #get number of logins associated with the user
        database[userName]['logins']+=1
    else:
        #set value for key
        database[userName] = {'logins' : 1}
        
        print("welcome " + userName + ".")  
        
    #print(database)
    #make dictionary to hold gesture info
    userRecord = database[userName]

    print(database)
##########################################

login()

pygameWindow = PYGAME_WINDOW()

##########################################
clf = pickle.load(open('/Users/chief/Desktop/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/CS228/Del7/userData/classifier.p', 'rb'))
testData = np.zeros((1,30),dtype ='f')
##########################################
#"global" x and y
x = 0
y = 0

#"global" min and max dimensions of windowsize
xMin = -175.0
xMax = 175.0
yMin = -175.0
yMax = 1.0

width = 5

k = 0

programState = 0
gloablNumFrames = 0
rightSign = 0
framesCorrect = 0
sucess = False
digitPresented = " "
framesGoneBy = 0

whichDigit = 0
framesToGuess = 35
signCorrect = 10
scaffoldingTwo = 4
scaffoldingThree = 6
correctSign = False
framesUntilCorrect = 10

currentSessionCorrect = 0
currSessionPresented = 0


########################################## 
    
def handLocation(base):
    isCentered = True
    if (base[0] < -90) and (base[2] > 90):
        isCentered = False
        handDirection.draw_rightUpImage()
    elif (base[0] < -90) and (base[2] < 10):
        isCentered = False 
        handDirection.draw_rightDownImage()
    elif (base[0] > 90) and (base[2] > 90):
        isCentered = False 
        handDirection.draw_leftUpImage()
    elif (base[0] > 90) and (base[2] < 10):
        isCentered = False 
        handDirection.draw_leftDownImage()
    elif(base[0] < -100):
        isCentered = False 
        handDirection.draw_rightImage()
    elif(base[0] > 100):
        isCentered = False 
        handDirection.draw_leftImage()
    elif(base[2] > 100):
        isCentered = False 
        handDirection.draw_upImage()
    elif(base[2] < 0):
        isCentered = False 
        handDirection.draw_downImage()

    return isCentered

########################################## 
#If the user is able to keep their hand at the origin for a sufficiently long period of time
#(you decide what that time span should be), provide a visual cue to the user that they have
#succeeded.
def isHandCentered(hand, framesCentered):
    global programState
    #middle finger
    theBird = hand.fingers[2]
    #base of middle finger
    birdBase = theBird.bone(0)
    # center of middle finger base
    centerBird  = birdBase.prev_joint
    #check if its centered
    isCentered = handLocation(centerBird)

    #if the hand is centered
    if(isCentered == True):
        framesCentered+=1
    #hand isnt centered    
    if(isCentered == False):
        framesCentered = 0

    #the hand has been centered for 25 frames    
    if(framesCentered > 10):
        programState = 2
    if(framesCentered < 10):
        programState = 1
    
    return framesCentered

########################################## 
#hand is present
def HandleState0(frame, handslist):
    global programState
    handDirection.draw_startUpImage()
    #if hands are detected
    if(HandOverDevice(frame, handslist)):
        programState = 1

########################################## 
#hand is present but not centered
def HandleState1(frame, handlist):
    global programState
    global framesGoneBy
    #if no hands are detected
    if(not HandOverDevice(frame, handlist)):
        programState = 0
        framesGoneBy = 0

########################################## 
#Now, if the users hand is centered, pick one of the 10 ASL numbers at random and show it
# to the user in the upper right panel. Also, show an image of the ASL gesture corresponding
# to this digit in the lower right panel so the user knows what to do
def HandleState2(frame, handlist):
    global programState
    global framesGoneBy
    displayASL()   
    if(not HandOverDevice(frame, handlist)):
        programState = 0
        framesGoneBy = 0

########################################## 
def HandleState3(frame, handlist):
    global programState, sucess
    successImage = pygame.image.load("/Users/chief/Desktop/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/CS228/Del10/ASLNUMS/aslSucess.jpg")
    successImage = pygameWindow.screen.blit(successImage, (constants.pygameWindowWidth/2 + constants.pygameWindowWidth/8, 150))  
    sucess = False
    
    if(not HandOverDevice(frame, handlist)):
        programState = 0

########################################## 
def HandOverDevice(frame, handlist):
    global k
    # #if the list is not empty
    frame = frame
    handlist = handlist
    if(len(handlist) > 0):
        k = 0
        isHandOverDevice = True
    else:
        isHandOverDevice = False
    return isHandOverDevice
    
##########################################
def displayASL():
    global aslNum, num
    global sucess
    global digitPresented
    global userRecord
    global aslDigit
    global whichDigit
    global daNumba
    global aslSign
    global key
    global convert
    global framesToGuess
    global timesCorrect
    global currentSessionCorrect
    global currSessionPresented
    global database
    global framesCorrect
    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 32)

    aslNum = range(0,10)
    #choose asl to gesture
    numToGesture = aslNum[whichDigit]
  
    if sucess == False:
        
        if(numToGesture == aslNum[0]):
            if('digit0presented' in userRecord):
                userRecord['digit0presented'] = userRecord['digit0presented'] + 1
            else:
                userRecord['digit0presented'] = 1
            aslDigit = font.render("Times Presented: " + str(userRecord['digit0presented']), True, (0, 0, 0))
            num = '0'

        if(numToGesture == aslNum[1]):
            if('digit1presented' in userRecord):
                userRecord['digit1presented'] = userRecord['digit1presented'] + 1
            else:
                userRecord['digit1presented'] = 1
            aslDigit = font.render("Times Presented: " + str(userRecord['digit1presented']), True, (0, 0, 0))
            num = '1'

        if(numToGesture == aslNum[2]):
            if('digit2presented' in userRecord):
                userRecord['digit2presented'] = userRecord['digit2presented'] + 1
            else:
                userRecord['digit2presented'] = 1
            aslDigit = font.render("Times Presented: " + str(userRecord['digit2presented']), True, (0, 0, 0))
            num = '2'

        if(numToGesture == aslNum[3]):
            if('digit3presented' in userRecord):
                userRecord['digit3presented'] = userRecord['digit3presented'] + 1
            else:
                userRecord['digit3presented'] = 1
            aslDigit = font.render("Times Presented: " + str(userRecord['digit3presented']), True, (0, 0, 0))
            num = '3'
        if(numToGesture == aslNum[4]):
            if('digit4presented' in userRecord):
                userRecord['digit4presented'] = userRecord['digit4presented'] + 1
                
            else:
                userRecord['digit4presented'] = 1
            aslDigit = font.render("Times Presented: " + str(userRecord['digit4presented']), True, (0, 0, 0))
            num = '4'

        if(numToGesture == aslNum[5]):
            if('digit5presented' in userRecord):
                userRecord['digit5presented'] = userRecord['digit5presented'] + 1
            else:
                userRecord['digit5presented'] = 1
            aslDigit = font.render("Times Presented: " + str(userRecord['digit5presented']), True, (0, 0, 0))
            num = '5'

        if(numToGesture == aslNum[6]):
            if('digit6presented' in userRecord):
                userRecord['digit6presented'] = userRecord['digit6presented'] + 1
            else:
                userRecord['digit6presented'] = 1
            aslDigit = font.render("Times Presented: " + str(userRecord['digit6presented']), True, (0, 0, 0))
            num = '6'

        if(numToGesture == aslNum[7]):
            if('digit7presented' in userRecord):
                userRecord['digit7presented'] = userRecord['digit7presented'] + 1
            else:
                userRecord['digit7presented'] = 1
            aslDigit = font.render("Times Presented: " + str(userRecord['digit7presented']), True, (0, 0, 0))
            num = '7'

        if(numToGesture == aslNum[8]):
            if('digit8presented' in userRecord):
                userRecord['digit8presented'] = userRecord['digit8presented'] + 1
            else:
                userRecord['digit8presented'] = 1
            aslDigit = font.render("Times Presented: " + str(userRecord['digit8presented']), True, (0, 0, 0))
            num = '8'

        if(numToGesture == aslNum[9]):
            if('digit9presented' in userRecord):
                userRecord['digit9presented'] = userRecord['digit9presented'] + 1
            else:
                userRecord['digit9presented'] = 1
            aslDigit = font.render("Times Presented: " + str(userRecord['digit9presented']), True, (0, 0, 0))
            num = '9'

    currSessionPresented = float(currSessionPresented)
    currentSessionCorrect  = float(currentSessionCorrect)

    draw_userProgress(currentSessionCorrect, currSessionPresented)
    draw_prevProgress(userRecord)
    compareUsers(database)
    drawGestureStatus(framesCorrect)
    
    sucess = True


    convert = str(whichDigit)
    key = (convert + " Sucessful signs") 

    pygameWindow.screen.blit(aslDigit,(675,900))  
    daNumba = pygame.image.load("/Users/chief/Desktop/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/CS228/Del9/ASLNUMS/"+num+".png")
    aslSign = pygame.image.load("/Users/chief/Desktop/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/CS228/Del9/ASLNUMS/asl"+num+".png")
    pygameWindow.screen.blit(daNumba, (750, 175))

    #display the asl gesture if sucessful for 3 times
    if((key not in userRecord) or (userRecord.get(key) <= scaffoldingTwo)):
        pygameWindow.screen.blit(aslSign, (675, 625))
        

    if(key in userRecord):
        timesCorrect = font.render("Times correct: " + str(userRecord[key]), True, (0, 0, 0))
        pygameWindow.screen.blit(timesCorrect,(675, 950))
        #the user has successfully signed the number 4 or more times
        #so hide the ASL gesture image
        if(userRecord.get(key) >= scaffoldingTwo):
            if(userRecord.get(key) >= scaffoldingThree):
                framesToGuess = 18
            else:
                framesToGuess = 35

    correctGesture(aslNum)
#############################################   
def correctGesture(aslNum):
    global programState
    global framesCorrect
    global sucess
    global predictedClass
    global framesGoneBy
    global whichDigit
    global framesToGuess
    global signCorrect
    global key
    global convert
    global color
    global correctSign
    global framesUntilCorrect
    global currentSessionCorrect
    global currSessionPresented
    

    predictedClass = clf.Predict(testData)

    if(predictedClass == aslNum[whichDigit]):
        correctSign = True
        framesCorrect+=1
        framesGoneBy+=1
       
    if(predictedClass != aslNum[whichDigit]):
        correctSign = False
        framesGoneBy+= 1 
        framesCorrect = 0
        programState = 2

    if(framesGoneBy >= framesToGuess):
        currSessionPresented +=1
        pickle.dump(database, open('userData/database.p','wb'))
        framesUntilCorrect = 10
        framesGoneBy = 0
        programState = 2
        sucess = False
    
    if(framesCorrect >= signCorrect):
        #framesCorrect = 10
        currSessionPresented += 1
        currentSessionCorrect += 1
        #increment whichDigit because of successful sign
        #only if digit is less than or equal to 9
        convert = str(whichDigit)
        key = (convert + " Sucessful signs")   
        
        if(whichDigit < 9):
            #create a dictionary for sucessful sign 
            if(key in userRecord):   
                #increment it 
                userRecord[key] = userRecord[key] + 1
            #not in dictionary
            else:
                userRecord[key] = 1
            whichDigit+=1
        #otherwise bring it back to 0
        elif(whichDigit == 9):
            if(key in userRecord):   
                #increment it 
                userRecord[key] = userRecord[key] + 1
            #not in dictionary
            else:
                userRecord[key] = 1
            whichDigit = 0

        framesGoneBy = 0
        programState = 3
        print("success")

        #dump contents of dictionary in pickled file
        pickle.dump(database, open('userData/database.p','wb'))

############################################# 
def drawGestureStatus(framesCorrect):

    color = (0, 0, 0)
    pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], 0, pi/2, 5)  
    pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], pi/2, pi, 5)    
    pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], pi, 3*pi/2, 5)    
    pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], 3*pi/2, 2*pi, 5)  

    cold = pygame.image.load("/Users/chief/Desktop/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/CS228/Del10/ASLNUMS/cold.png")
    warm = pygame.image.load("/Users/chief/Desktop/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/CS228/Del10/ASLNUMS/warm.png")
    hot = pygame.image.load("/Users/chief/Desktop/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/CS228/Del10/ASLNUMS/10Success.png")
    

    if(framesCorrect == 0):
        #display thumbs down 
        cold = pygameWindow.screen.blit(cold, (275, 515))  
        color = (255, 0, 0)
        pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], 0, pi/2, 5)  
        pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], pi/2, pi, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], pi, 3*pi/2, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], 3*pi/2, 2*pi, 5)  
    
    elif(framesCorrect > 0 and framesCorrect <= 9):
        #display thumbs up
        warm = pygameWindow.screen.blit(warm, (275, 515)) 
        color = (0, 255, 0)
        pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], 0, pi/2, 5)  
        pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], pi/2, pi, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], pi, 3*pi/2, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], 3*pi/2, 2*pi, 5)  
    
    elif(framesCorrect >= 10):
        #display gold thumbs up
        hot = pygameWindow.screen.blit(hot, (275, 515)) 
        color = (255, 215, 0)
        pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], 0, pi/2, 5)  
        pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], pi/2, pi, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], pi, 3*pi/2, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [212.5, 625, 250, 250], 3*pi/2, 2*pi, 5)   


############################################# 
def compareUsers(database):

    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 24)

    prevSeshSeen = 'prevSessionPresented'
    prevSeshCorrect = 'prevSessionCorrect'
    totalSeen = 0
    totalCorrect = 0
    for i in database:
        if(prevSeshSeen in database[i]):
            totalSeen += database[i][prevSeshSeen]
            if(prevSeshCorrect in database[i]):
                totalCorrect += database[i][prevSeshCorrect]
            else:
                totalCorrect += 0
        else:
            totalSeen += 0
    
    if(totalSeen == 0 or totalCorrect == 0):
        averageSuccess = 0.0
        averageSuccessPercentage = 0.0
    else:
        averageSuccess = float(totalCorrect/totalSeen)
        averageSuccessPercentage = round(float(averageSuccess * 100), 2)
    averageProgress = font.render("Avg Sucess %: " + str(averageSuccessPercentage), True, (0, 0, 255))
    pygameWindow.screen.blit(averageProgress, (5, 850))

    color = (0, 0, 0)

    pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], 0, pi/2, 5)  
    pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], pi/2, pi, 5)    
    pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], pi, 3*pi/2, 5)    
    pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], 3*pi/2, 2*pi, 5)  

    #if the userProgress is less than 25 make the color red
    if(averageSuccess <= 0.25):
        color = (255, 0, 0)
        pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], 0, pi/2, 5)  
       
    elif(averageSuccess >= 0.25 and averageSuccess <= 0.50):
        color = (255,140,0)
        pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], 0, pi/2, 5)  
        pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], pi/2, pi, 5)      
       
    elif(averageSuccess >= 0.50 and averageSuccess <= 0.75):
        color = (255, 255, 0)
        pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], 0, pi/2, 5)  
        pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], pi/2, pi, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], pi, 3*pi/2, 5)    

    elif(averageSuccess >= 0.75 and averageSuccess <= 1.00):
        color = (0, 255, 0)
        pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], 0, pi/2, 5)  
        pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], pi/2, pi, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], pi, 3*pi/2, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [25, 866, 100, 100], 3*pi/2, 2*pi, 5)   

#############################################       
# Draws a circle with the user progess                
def draw_userProgress(currentSessionCorrect, currSessionPresented):
    #arc(surface, color, rect, start_angle, stop_angle, width=1) 
    #calculate userProgress

    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 24)
    if(currSessionPresented == 0):
        currentSessionCorrect = 0
        progPercentage = 0.0
        userProgress = 0.0
    else:
        userProgress = float(currentSessionCorrect/currSessionPresented)
        progPercentage = round(float(userProgress*100),2)
    userProg = font.render("Cur. Sucess %: " + str(progPercentage), True, (0, 0, 255))
    pygameWindow.screen.blit(userProg,(5, 517))

    color = (0, 0, 0)

    pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], 0, pi/2, 5)  
    pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], pi/2, pi, 5)    
    pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], pi, 3*pi/2, 5)    
    pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], 3*pi/2, 2*pi, 5)  

    
    #if the userProgress is less than 25 make the color red
    if(userProgress <= 0.25):
        color = (255, 0, 0)
        pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], 0, pi/2, 5)  
       
    elif(userProgress >= 0.25 and userProgress <= 0.50):
        color = (255,140,0)
        pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], 0, pi/2, 5)  
        pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], pi/2, pi, 5)      
       
    elif(userProgress >= 0.50 and userProgress <= 0.75):
        color = (255, 255, 0)
        pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], 0, pi/2, 5)  
        pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], pi/2, pi, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], pi, 3*pi/2, 5)    

    elif(userProgress >= 0.75 and userProgress <= 1.00):
        color = (0, 255, 0)
        pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], 0, pi/2, 5)  
        pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], pi/2, pi, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], pi, 3*pi/2, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [25, 533, 100, 100], 3*pi/2, 2*pi, 5)   

    
############################################# 
def draw_prevProgress(userRecord):
    #arc(surface, color, rect, start_angle, stop_angle, width=1) 
    #calculate previous user progress

    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 24)

    prevSeshProgress = 'prevSessionPresented'
    prevSeshCorrect = 'prevSessionCorrect'

    color = (0, 0, 0)

    pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], 0, pi/2, 5)  
    pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], pi/2, pi, 5)    
    pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], pi, 3*pi/2, 5)    
    pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], 3*pi/2, 2*pi, 5)  

    if(prevSeshProgress and prevSeshCorrect in userRecord):
        prevGestureSeen = userRecord.get(prevSeshProgress)
        prevGestureCorrect = userRecord.get(prevSeshCorrect)
        if(prevGestureSeen == 0 and prevGestureCorrect == 0):
            prevSeshProgress = 0.0
            prevSeshPercentage = 0.0
        else:
            prevSeshProgress = float(prevGestureCorrect/prevGestureSeen)
            prevSeshPercentage = round(float(prevSeshProgress * 100),2)
        prevSeshProg= font.render("Lst. Sucess %: " + str(prevSeshPercentage), True, (0, 0, 255))


        #if the userProgress is less than 25 make the color red
        if(prevSeshProgress <= 0.25):
            color = (255, 0, 0)
            pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], 0, pi/2, 5)  
        
        elif(prevSeshProgress >= 0.25 and prevSeshProgress <= 0.50):
            color = (255,140,0)
            pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], 0, pi/2, 5)  
            pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], pi/2, pi, 5)   
        
        elif(prevSeshProgress >= 0.50 and prevSeshProgress <= 0.75):
            color = (255, 255, 0)
            pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], 0, pi/2, 5)  
            pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], pi/2, pi, 5)    
            pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], pi, 3*pi/2, 5)    

        elif(prevSeshProgress >= 0.75 and prevSeshProgress <= 1.00):
            color = (0, 255, 0)
            pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], 0, pi/2, 5)  
            pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], pi/2, pi, 5)    
            pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], pi, 3*pi/2, 5)    
            pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], 3*pi/2, 2*pi, 5)  
    #there is no previous session
    if(prevSeshProgress and prevSeshCorrect not in userRecord):
        prevSeshProg= font.render("Lst. Success %: " + str(0.0), True, (0, 0, 255))
        color = (255, 0, 0)
        pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], 0, pi/2, 5)  
        pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], pi/2, pi, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], pi, 3*pi/2, 5)    
        pygame.draw.arc(pygameWindow.screen, color, [25, 696, 100, 100], 3*pi/2, 2*pi, 5)  

    pygameWindow.screen.blit(prevSeshProg,(5, 680))
        
#############################################                     
def draw_panels():
    pygame.draw.line(pygameWindow.screen, (0,0,0),(constants.pygameWindowWidth/2, 0), (constants.pygameWindowWidth/2, constants.pygameWindowDepth), 2)
    pygame.draw.line(pygameWindow.screen, (0,0,0),(0, constants.pygameWindowDepth/2), (constants.pygameWindowWidth, constants.pygameWindowDepth/2), 2)
    pygame.draw.line(pygameWindow.screen, (0,0,0), (175, constants.pygameWindowDepth/2), (175, constants.pygameWindowDepth), 2)
    pygame.draw.line(pygameWindow.screen, (0,0,0), (0, 666), (175, 666), 2)
    pygame.draw.line(pygameWindow.screen, (0,0,0), (0, 833), (175, 833), 2)
##########################################  
def CenterData(testData):
    allXCoordinates = testData[0,::3]
    meanXValue = allXCoordinates.mean()
    testData[0,::3] = allXCoordinates-meanXValue

    allYCoordinates = testData[0,1::3]
    meanYValue = allYCoordinates.mean()
    testData[0,1::3] = allYCoordinates-meanYValue
    
    allZCoordinates = testData[0,2::3]
    meanZValue = allZCoordinates.mean()
    testData[0,2::3] = allZCoordinates-meanZValue
    return testData  
    
##########################################
def Handle_Vector_From_Leap(v):
    global x, y
    global xMin, xMax, yMin, yMax

    x = int(v[0])
    y = int(v[2])

    scaleX = Scale(x, xMin, xMax, 0, constants.pygameWindowWidth/2)
    scaleY = Scale(y, yMin, yMax, 0, constants.pygameWindowDepth/2)

    if(x < xMin):
        xMin = x
    if(x > xMax):
        xMax = x

    if(y < yMin):
        yMin = y
    if(y > yMax):
        yMax = y

    #Scale the two values like you did previously
    return scaleX, scaleY
    

##########################################
def Handle_Bone(bone):
    global width
    global base, tip
    #Modifying the code to make sure that it workss
    global xTip,yTip,zTip
    #Change color if the user is signing correctly or inccorrectly
    global color
    global correctSign

    baseInfo = Handle_Vector_From_Leap(base)
    tipInfo = Handle_Vector_From_Leap(tip)

    if(correctSign == True):
        color = (0, 255, 0)
    elif(correctSign == False):
        color = (255,0,0)
    #change to this eventually so that hand is drawn correctly
    pygameWindow.Draw_Line(color, baseInfo[0], baseInfo[1], tipInfo[0], tipInfo[1], width)
   
##########################################
def Handle_Finger(finger):
    global width
    global k 
    global base, tip
    global xTip,yTip,zTip
    global bone 
    global testData
    global predictedClass


    for b in range(0, 4):
        bone = finger.bone(b)

        base = bone.prev_joint
        tip  = bone.next_joint
        xTip = int(tip[0])
        yTip = int(tip[1])
        zTip = int(tip[2])

        if((b == 0 or (b == 3))):
            testData[0,k] = xTip
            testData[0, k+1] = yTip
            testData[0, k+2] = zTip
            k = k + 3

        if(b == 0):
            width = 5
        elif(b == 1):
            width = 4
        elif(b == 2):
            width = 3
        elif(b == 3):
            width  = 2
        elif(b == 4):
            width  = 1 
        Handle_Bone(bone)

    testData = CenterData(testData)
    
##########################################
def Handle_Frame(frame, numFrames):
    global x, y
    global xMin, xMax, yMin, yMax
    global gloablNumFrames
    hand = frame.hands[0]
    fingers = hand.fingers
    #print(str(len(fingers)))
    for finger in fingers:
        #print right after assignment 
        #print(finger)
        Handle_Finger(finger)    

    if(numFrames == 0):
        count = isHandCentered(hand, numFrames)
        gloablNumFrames = count
    # Check that the hand is centered
    gloablNumFrames = isHandCentered(hand, gloablNumFrames)

##########################################
#arg 1 should lie within a range defined by args 2 and 3.
#and should be scaled so that it lies within the new range
#defined by args 4 and 5
def Scale(fingerPosition, leapStart, leapEnd, appStart, appEnd):
    deviceRange = leapEnd - leapStart

    #xMin == xMax and yMin == yMax
    if(deviceRange == 0):
        curPosition = appStart

    else:
        appRange = appEnd - appStart
        curPosition = (((fingerPosition - leapStart) * appRange)/deviceRange) + appStart
    return int(curPosition)
##########################################

controller = Leap.Controller()
numFrames = 0
########################################## 
    
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            userRecord['prevSessionPresented'] = currSessionPresented
            userRecord['prevSessionCorrect'] = currentSessionCorrect
            pickle.dump(database, open('userData/database.p','wb'))
            pygame.quit()
            sys.exit()

    #prepare the window
    pygameWindow.Prepare()
    #draw the panels
    draw_panels()

    # #sandwich this between prepare and reveal
    frame = controller.frame()
    # #hands = frame.hands[0]
    handlist = frame.hands

    if(programState == 0):
        HandleState0(frame, handlist)
    if(programState == 1):
        correctSign = False
        HandleState1(frame, handlist)
    if(programState == 2):
        HandleState2(frame, handlist)
    if(programState == 3):
        HandleState3(frame, handlist)

    if(len(handlist) > 0):
        k = 0
        Handle_Frame(frame, numFrames)
        numFrames+=1
    #reveal window
    pygameWindow.Reveal()


