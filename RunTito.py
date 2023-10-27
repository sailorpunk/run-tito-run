
import machine
import thumby
import time
import random
import gc
from machine import freq

freq(125_000_000)

gc.enable() # This line helps make sure we don't run out of memory
gc.collect()
# Sensitive game parameters
XVel = 0.05
YVel = 0
Distance = 0
YPos = 0
Gravity = 0.15
MaxFPS = 60
Points = 0
GameRunning = True
SpritePos = random.randint(72, 300)
CloudPos = random.randint(60, 200)
JumpSoundTimer = 0
SuperTito = False
frameCount = 0
superJump = -2.5
jump = -2.0
point = 10
superPoint = 20
lastSpawn = 1

def superAudio():
    thumby.audio.play(350,50)
    thumby.audio.play(450,50)
    
# Sprite data

# BITMAP: width: 16, height: 8
PlayerRunFrame1 = bytearray([254,253,131,231,231,231,199,199,199,199,133,241,242,248,249,253])
PlayerRunFrame2 = bytearray([255,191,192,167,231,231,199,199,199,135,197,177,242,248,249,253])
SuperTitoFrame1 = bytearray([227,221,170,182,170,221,227,199,198,134,192,176,242,248,249,253])
SuperTitoFrame2 = bytearray([227,213,182,128,182,213,227,199,197,198,128,240,242,248,249,253])
           
CactusSpr1 = bytearray([255,3,121,29,61,3,255,255])
CactusSpr2 = bytearray([255,227,239,0,0,223,199,255])
StarSpr = bytearray([223,175,111,239,115,221,254,221,115,239,111,175,223,
           247,233,238,247,247,242,242,242,247,247,238,233,247])
CloudSpr = bytearray([0x9F, 0x4F, 0x63, 0x59, 0xBD, 0x73, 0x73, 0x65, 0x5C, 0x7E, 0x7E, 0x51, 0x57, 0x4F, 0x1F, 0xBF])
CactusSpr = CactusSpr1
SpawnSprite = CactusSpr

thumby.display.fill(0)
thumby.display.drawText("RUN TITO,", 12, 0, 1)
thumby.display.drawText("  RUN!", 15, 9, 1)
thumby.display.setFPS(60)
thumby.saveData.setName("RunTitoRun")

while(thumby.buttonA.pressed() == True or thumby.buttonB.pressed() == True):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 0)
        thumby.display.drawText("Press A/B", 9, 32, 1)
    else:
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 1)
        thumby.display.drawText("Press A/B", 9, 32, 0)
    thumby.display.update()
    pass
while(thumby.buttonA.pressed() == False and thumby.buttonB.pressed() == False):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 0)
        thumby.display.drawText("Press A/B", 9, 32, 1)
    else:
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 1)
        thumby.display.drawText("Press A/B", 9, 32, 0)
    thumby.display.update()
    pass
while(thumby.buttonA.pressed() == True or thumby.buttonB.pressed() == True):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 0)
        thumby.display.drawText("Press A/B", 9, 32, 1)
    else:
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 1)
        thumby.display.drawText("Press A/B", 9, 32, 0)
    thumby.display.update()
    pass
        
        
while(GameRunning):
    t0 = time.ticks_us() # Check the time

    # Is the player on the ground and trying to jump?
    if(JumpSoundTimer < 0):
        JumpSoundTimer = 0
    if((thumby.buttonA.pressed() == True or thumby.buttonB.pressed() == True) and YPos == 0.0):
        # Jump!
        JumpSoundTimer = 200
        if (SuperTito):
            YVel = superJump
        else:
            YVel = jump

    # Handle "dynamics"
    YPos += YVel
    YVel += Gravity
    Distance += XVel
    JumpSoundTimer -= 15

    if(JumpSoundTimer > 0):
        thumby.audio.set(500-JumpSoundTimer)
    else:
        thumby.audio.stop()

    # Accelerate the player just a little bit
    if (SuperTito):
        XVel += 0.00003
    else: XVel += 0.000025
    
    # Make sure we haven't fallen below the ground
    if (YPos > 0):
        YPos = 0.0
        YVel = 0.0
    
    # Has the player hit a cactus?
    collision = SpritePos < 5 and SpritePos > -5 and YPos > -6
    
    if (not collision):
        frameCount = 0

    elif (collision):
        if (SuperTito and SpawnSprite == CactusSpr):
            frameCount = 1
            if (frameCount == 1):
                SuperTito = False

        elif (SpawnSprite == CactusSpr and frameCount == 0):
            GameRunning = False
            thumby.display.fill(1)
            thumby.audio.stop()
            thumby.display.drawText("Dammit Tito!", 1, 1, 0)
            thumby.display.drawText(str(int(Distance))+"m", 26, 9, 0)
            high = -1
            if (thumby.saveData.hasItem("highscore")):
                high = int(thumby.saveData.getItem("highscore"))
                thumby.display.drawText("High: " + str(high)+"m", 8, 17, 0)
            if (Distance > high):
                thumby.saveData.setItem("highscore", Distance)
                thumby.saveData.save()
            thumby.display.drawText("Again?", 19, 25, 0)
            thumby.display.drawText("A:Y B:N", 16, 33, 0) 
            thumby.display.update()
            thumby.audio.playBlocking(300, 250)
            thumby.audio.play(260, 250)
            
            while (thumby.inputPressed() == False):
                pass # Wait for the user to give us something
        
            while (GameRunning == False):
                if (thumby.buttonA.pressed() == True == 1):
                    # Restart the game
                    XVel = 0.05
                    YVel = 0
                    Distance = 0
                    YPos = 0
                    Points = 0
                    GameRunning = True
                    SpritePos = random.randint(72, 300)
                    CloudPos = random.randint(60, 200)
                elif (thumby.buttonB.pressed() == True):
                    # Quit
                    machine.reset()
            else: 
                pass
        
        elif (SpawnSprite == StarSpr):
            SuperTito = True
            superAudio()
            
    # Is the cactus out of view?
    if (SpritePos < -24):
        # "spawn" another one (Set its position some distance ahead and change the sprite)
        if (SuperTito):
            Points += superPoint
        else: 
            Points += point
        thumby.audio.play(440, 300)
        SpritePos = random.randint(72, 500)
      
        # spawn selector
        random.seed(time.ticks_ms())
        if (SpawnSprite == CactusSpr and random.randint(0, 1) == 0):
            CactusSpr = CactusSpr1
            lastSpawn = 0
        else:
            CactusSpr = CactusSpr2
            lastSpawn = 0
        if (random.random() <= .8 or lastSpawn == 1):
            SpawnSprite = CactusSpr
            lastSpawn = 0
        else:
            SpawnSprite = StarSpr
            lastSpawn = 1

            
    # Is the cloud out of view?
    if (CloudPos < -32):
        # "spawn" another one
        CloudPos = random.randint(40, 200)

    # More dynaaaaaaaaaaaamics
    SpritePos -= XVel * 16
    CloudPos -= XVel * 2

    # Draw game state
    thumby.display.fill(1)
    if (len(SpawnSprite) == 8):
        thumby.display.blit(SpawnSprite, int(16 + SpritePos), 24, 8, 8, 1, 0, 0)
    else:
        thumby.display.blit(SpawnSprite, int(16 + SpritePos), 20, 13, 13, 1, 0, 0)
        
    thumby.display.blit(CloudSpr, int(16 + CloudPos), 8, 16, 8, 1, 0, 0)

    # Regular Tito animation
    if (not SuperTito):
        if (t0 % 250000 < 125000 or YPos != 0.0):
        # Player is in first frame of run animation
            thumby.display.blit(PlayerRunFrame1, 8, int(23 + YPos), 16, 8, 1, 0, 0)
        else:
            # Player is in second frame of run animation
            thumby.display.blit(PlayerRunFrame2, 8, int(24 + YPos), 16, 8, 1, 0, 0)
    
    # Super Tito animation    
    if (SuperTito):
        if (t0 % 250000 < 125000 or YPos != 0.0):
            # Player is in first frame of run animation
            thumby.display.blit(SuperTitoFrame1, 8, int(23 + YPos), 16, 8, 1, 0, 0)
        else:
            # Player is in second frame of run animation
            thumby.display.blit(SuperTitoFrame2, 8, int(24 + YPos), 16, 8, 1, 0, 0)

    thumby.display.drawFilledRectangle(0, 31, thumby.display.width, 9, 0) # Ground
    thumby.display.drawText(str(int(Points)), 0, 0, 0) # Current points
    thumby.display.drawText("pts", len(str(int(Points))) * 8, 0, 0)
    thumby.display.drawText(str(int(Distance)), 0, 32, 1) # Current distance
    thumby.display.drawText("m", len(str(int(Distance))) * 8, 32, 1)
    thumby.display.update()

    # Spin wheels until we've used up one frame's worth of time
    while (time.ticks_us() - t0 < 1000000.0 / MaxFPS):
        pass