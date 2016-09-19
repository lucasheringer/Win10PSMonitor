#python meters interface for the windows health Monitor
import pygame
from pygame.locals import *
import os
import json
import urllib
import time
import subprocess

FPS = 5
#url = "http://10.42.0.1/results.json"
newUrl = "http://192.168.1.209:8085/data.json"
#testing webhook

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

#img3 = pygame.image.load('c:\Users\lucas\Documents\PoweShell\HardwareMonitor\Clean-Background-320x240.bmp')
#shutDownImg64 = pygame.image.load('c:\Users\lucas\Documents\PoweShell\HardwareMonitor\shutdown-icon-red-64p.bmp')

#Reading Json from apache
def getJson():
    tries = 5
    while tries >= 0:
        try:
            response = urllib.urlopen(newUrl)
            data = json.loads(response.read())
            T_CPUTEMP = (data['Children'][0]['Children'][1]['Children'][1]['Children'][4]['Value']) # CPU temperature
            T_CPU = (data['Children'][0]['Children'][1]['Children'][2]['Children'][0]['Value']) #Load
            T_MEM = (data['Children'][0]['Children'][2]['Children'][0]['Children'][0]['Value']) #Memory
            T_GPU0TEMP = (data['Children'][0]['Children'][3]['Children'][1]['Children'][0]['Value']) #gpu0 temperature
            T_GPU0 = (data['Children'][0]['Children'][3]['Children'][2]['Children'][0]['Value']) #gpu0 Load
            T_GPU0MEM = (data['Children'][0]['Children'][3]['Children'][2]['Children'][3]['Value']) #gpu0 Memory
            T_GPU1TEMP = (data['Children'][0]['Children'][4]['Children'][1]['Children'][0]['Value']) #gpu1 temperature
            T_GPU1 = (data['Children'][0]['Children'][4]['Children'][2]['Children'][0]['Value']) #GPU1 Load
            T_GPU1MEM = (data['Children'][0]['Children'][4]['Children'][2]['Children'][3]['Value']) #GPU1 Memory

            CPU = float(T_CPU.split(' ',1)[0])
            MEM = float(T_MEM.split(' ',1)[0])
            GPU0 = float(T_GPU0.split(' ',1)[0])
            GPU0MEM = float(T_GPU0MEM.split(' ',1)[0])
            GPU1 = float(T_GPU1.split(' ',1)[0])
            GPU1MEM = float(T_GPU1MEM.split(' ',1)[0])
            CPUTEMP = float(T_CPUTEMP.split(' ',1)[0])
            GPU0TEMP = float(T_GPU0TEMP.split(' ',1)[0])
            GPU1TEMP = float(T_GPU1TEMP.split(' ',1)[0])

            return CPU, MEM, GPU0, GPU0MEM, GPU1, GPU1MEM, CPUTEMP, GPU0TEMP, GPU1TEMP
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
    pygame.draw.rect(lcd,BLACK,(x+1, y+100, w+65, h-98)) #booton line cpu x+1, y+200, w+65, h-198
    pygame.draw.rect(lcd,BLACK,(x+1, y-1, w+64, h-98)) #top line cpu     x+1, y-1, w+64, h-198

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

#myfont = pygame.font.SysFont("comicsans", 16) #RobotoCondensed-BoldItalic.ttf
#myfontTime = pygame.font.SysFont("monospace", 16)
#myfontLarge = pygame.font.SysFont("monospace", 24)


pygame.display.update()
while True:
    CPU, MEM, GPU0, GPU0MEM, GPU1, GPU1MEM, CPUTEMP, GPU0TEMP, GPU1TEMP = getJson()
    realDate = (time.strftime("%d/%m/%Y"))
    realTime = (time.strftime("%H:%M:%S"))
    lcd.blit(img3,(0,0))
    SCPU = CPU * 2
    SMEM = MEM * 2
    SGPU0 = GPU0 * 2
    label = myfontTime.render((str(realDate)+" - "+str(realTime)), 1, WHITE)
    #CPU load
    lcd.blit(label, (5, 220))
    drawRectLarge(5,17,1,100)
    pygame.draw.rect(lcd,RED,(6,118-CPU,65,CPU))
    label = myfont.render((str("%.2f" % CPU)+" %"), 1, BLACK)
    lcd.blit(label, (20, 80))
    label = myfont.render(("CPU:"), 1, BLACK)
    lcd.blit(label, (20, 60))
    #Memory usage
    drawRectLarge(5,120,1,100)
    pygame.draw.rect(lcd,GREEN,(5,220-MEM,65,MEM))
    label = myfont.render((str("%.2f" % MEM)+" %"), 1, BLACK)
    lcd.blit(label, (20, 180))
    label = myfont.render(("MEM:"), 1, BLACK)
    lcd.blit(label, (20, 160))
    #GPU0 CPU load
    drawRectLarge(75,17,1,100)
    pygame.draw.rect(lcd,BLUE,(75,117-GPU0,65,GPU0))
    label = myfont.render((str("%.2f" % GPU0)+" %"), 1, BLACK)
    lcd.blit(label, (85, 80))
    label = myfont.render(("GPU0:"), 1, BLACK)
    lcd.blit(label, (85, 60))
    #GPU0 Memory usage
    drawRectLarge(75,120,1,100)
    pygame.draw.rect(lcd,GREEN,(75,220-GPU0MEM,65,GPU0MEM))
    label = myfont.render((str("%.2f" % GPU0MEM)+" %"), 1, BLACK)
    lcd.blit(label, (85, 180))
    label = myfont.render(("GPU0M   :"), 1, BLACK)
    lcd.blit(label, (82, 160))
    #GPU1 CPU load
    drawRectLarge(145,17,1,100)
    pygame.draw.rect(lcd,BLUE,(145,117-GPU1,65,GPU1))
    label = myfont.render((str("%.2f" % GPU1)+" %"), 1, BLACK)
    lcd.blit(label, (155, 80))
    label = myfont.render(("GPU1:"), 1, BLACK)
    lcd.blit(label, (155, 60))
    #GPU1 Memory usage
    drawRectLarge(145,120,1,100)
    pygame.draw.rect(lcd,GREEN,(145,220-GPU1MEM,65,GPU1MEM))
    label = myfont.render((str("%.2f" % GPU1MEM)+" %"), 1, BLACK)
    lcd.blit(label, (155, 180))
    label = myfont.render(("GPU1M:"), 1, BLACK)
    lcd.blit(label, (152, 160))

    #CPU TEmp
    pygame.draw.rect(lcd,RED,(231, 37, 65, 20))
    drawRectSmall(230,17,1,42)
    label = myfont.render(("CPU:"), 1, BLACK)
    lcd.blit(label, (240, 0))
    label = myfont.render(("Temp:"), 1, BLACK)
    lcd.blit(label, (240, 17))
    label = myfont.render(str("%.2f" % CPUTEMP)+" c", 1, BLACK)
    lcd.blit(label, (240, 37))

    #GPU0 Temp
    drawRectSmall(230,75,1,42)
    pygame.draw.rect(lcd,RED,(231, 95, 65, 20))
    label = myfont.render(("GPU's:"), 1, BLACK)
    lcd.blit(label, (240, 56))
    label = myfont.render(("Temp 0:"), 1, BLACK)
    lcd.blit(label, (235, 76))
    label = myfont.render(str("%.2f" % GPU0TEMP)+" c", 1, BLACK)
    lcd.blit(label, (240, 96))

    #GPU1 Temp
    drawRectSmall(230,120,1,42)
    pygame.draw.rect(lcd,RED,(231, 140, 65, 20))
    label = myfont.render(("Temp 1:"), 1, BLACK)
    lcd.blit(label, (235, 120))
    label = myfont.render(str("%.2f" % GPU1TEMP)+" c", 1, BLACK)
    lcd.blit(label, (240, 140))
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
