#python meters interface for the windows health Monitor
import pygame
from pygame.locals import *
import os
import json
import urllib
import time
import subprocess

FPS = 2
url = "http://10.42.0.1/results.json"

# Define basic colors
SHADOW = (192, 192, 192)
WHITE = (255, 255, 255)
LIGHTGREEN = (0, 255, 0 )
GREEN = (0, 200, 0 )
BLUE = (0, 0, 128)
LIGHTBLUE = (0, 0, 255)
RED = (200, 0, 0 )
LIGHTRED = (255, 100, 100)
PURPLE = (102, 0, 102)
LIGHTPURPLE = (153, 0, 153)
BLACK = (0, 0, 0)

img3 = pygame.image.load('/home/pi/Clean-Background-320x240.bmp')
shutDownImg64 = pygame.image.load('/home/pi/shutdown-icon-red-64p.bmp')

#Reading Json from apache
def getJson():
    tries = 5
    while tries >= 0:
        try:
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            CPU = (data['rows'][0]['c'][1]['v'])
            MEM = (data['rows'][1]['c'][1]['v'])
            DISK = (data['rows'][2]['c'][1]['v'])
            CPUTEMP = (data['rows'][3]['c'][1]['v'])
            CPUFAN = (data['rows'][4]['c'][1]['v'])
            return CPU, MEM, DISK, CPUTEMP, CPUFAN
        except ValueError:
            if tries == 0:
                print(ValueError)
            else:
                time.sleep(1)
                tries -= 1
                continue

def drawRectLarge(x, y, w, h):
    pygame.draw.rect(lcd,BLACK,(x, y, w, h)) #left line cpu   x, y, w, h
    pygame.draw.rect(lcd,BLACK,(x+66, y, w, h)) #right line cpu  x+66, y, w, h
    pygame.draw.rect(lcd,BLACK,(x+1, y+200, w+65, h-198)) #booton line cpu x+1, y+200, w+65, h-198
    pygame.draw.rect(lcd,BLACK,(x+1, y-1, w+64, h-198)) #top line cpu     x+1, y-1, w+64, h-198

def drawRectSmall(x, y, w, h):
    pygame.draw.rect(lcd,BLACK,(x, y, w, h)) #left line cpu   x, y, w, h
    pygame.draw.rect(lcd,BLACK,(x+66, y, w, h)) #right line cpu  x+66, y, w, h
    pygame.draw.rect(lcd,BLACK,(x+1, y+40, w+65, h-40)) #booton line cpu x+1, y+200, w+65, h-198
    pygame.draw.rect(lcd,BLACK,(x+1, y-1, w+64, h-40)) #top line cpu     x+1, y-1, w+64, h-198

os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
pygame.init()
pygame.display.set_caption('Win10 Monitor')
lcd = pygame.display.set_mode((320, 240))  #440,480
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
lcd.fill(WHITE)

#render text
myfont = pygame.font.Font("/usr/share/fonts/truetype/roboto/Roboto-Italic.ttf", 16) #RobotoCondensed-BoldItalic.ttf
myfontTime = pygame.font.Font("/usr/share/fonts/truetype/roboto/RobotoCondensed-BoldItalic.ttf", 16)
myfontLarge = pygame.font.Font("/usr/share/fonts/truetype/roboto/RobotoCondensed-BoldItalic.ttf", 24)
#myfont = pygame.font.Font("/usr/share/fonts/google-droid/DroidSans.ttf", 15)


pygame.display.update()
while True:
    CPU, MEM, DISK, CPUTEMP, CPUFAN = getJson()
    realDate = (time.strftime("%d/%m/%Y"))
    realTime = (time.strftime("%H:%M:%S"))
    lcd.blit(img3,(0,0))
    SCPU = CPU * 2
    SMEM = MEM * 2
    SDISK = DISK * 2
    label = myfontTime.render((str(realDate)+" - "+str(realTime)), 1, WHITE)
    lcd.blit(label, (5, 220))
    drawRectLarge(5,17,1,200)
    pygame.draw.rect(lcd,RED,(6,218-SCPU,65,SCPU))
    label = myfont.render((str(CPU)+" %"), 1, BLACK)
    lcd.blit(label, (20, 120))
    label = myfont.render(("CPU:"), 1, BLACK)
    lcd.blit(label, (20, 90))
    drawRectLarge(76,17,1,200)
    pygame.draw.rect(lcd,GREEN,(77,217-SMEM,65,SMEM))
    label = myfont.render((str(MEM)+" %"), 1, BLACK)
    lcd.blit(label, (90, 120))
    label = myfont.render(("MEM:"), 1, BLACK)
    lcd.blit(label, (90, 90))
    drawRectLarge(147,17,1,200)
    pygame.draw.rect(lcd,BLUE,(148,217-SDISK,65,SDISK))
    label = myfont.render((str(DISK)+" %"), 1, BLACK)
    lcd.blit(label, (160, 120))
    label = myfont.render(("DISK:"), 1, BLACK)
    lcd.blit(label, (160, 90))
    pygame.draw.rect(lcd,RED,(231, 37, 65, 20))
    drawRectSmall(230,17,1,42)
    label = myfont.render(("Temp:"), 1, BLACK)
    lcd.blit(label, (240, 17))
    label = myfont.render(str(CPUTEMP)+"c", 1, BLACK)
    lcd.blit(label, (240, 37))
    drawRectSmall(230,67,1,42)
    pygame.draw.rect(lcd,RED,(231, 87, 65, 20))
    label = myfont.render(("Fan:"), 1, BLACK)
    lcd.blit(label, (240, 67))
    label = myfont.render(str(CPUFAN)+"rpm", 1, BLACK)
    lcd.blit(label, (235, 87))
    lcd.blit(shutDownImg64,(240,160))
    pygame.display.update()
    for event in pygame.event.get():
        loopCheck = True
        if(event.type == pygame.MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            x, y = pos
            if x >= 250 and x <= 290 and y >= 160 and y <= 210:
                while loopCheck == True:
                    #print(str(event.type)+str(pos))
                    pygame.draw.rect(lcd,WHITE,(90, 60, 140, 40))
                    pygame.draw.rect(lcd,SHADOW,(90, 100, 140, 40))
                    pygame.draw.rect(lcd,BLACK,(90, 100, 140, 2))
                    pygame.draw.rect(lcd,BLACK,(160, 100, 2, 40))
                    label = myfontLarge.render("Are you sure?", 1, BLACK)
                    lcd.blit(label, (100, 61))
                    label = myfontLarge.render("YES         NO", 1, RED)
                    lcd.blit(label, (100, 100))
                    pygame.display.update()
                    clock.tick(5)
                    for event in pygame.event.get():
                        if(event.type == pygame.MOUSEBUTTONDOWN):
                            pos = pygame.mouse.get_pos()
                            x, y = pos
                            if x >= 100 and x <= 140 and y >= 100 and y <= 125:
                                pygame.quit()
                                subprocess.call("sudo shutdown -h now", shell=True)
                                #pygame.quit()
                                quit()
                                #print("Shutting down :( ")
                                loopCheck = False
                            elif x >= 180 and x <= 220 and y >= 100 and y <= 125:
                                #print("Returning to monitor :) ")
                                loopCheck = False
    clock.tick(FPS)
