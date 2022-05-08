import pygame
import sys
import os
import time
from threading import Thread


#create window
os.environ["SDL_VIDEO_CENTERED"]="1"
pygame.init()
SCREENWIDTH=310
SCREENHEIGHT=400
#defs windows dimensions
SCREENSIZE=[SCREENWIDTH,SCREENHEIGHT]
SCREEN=pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('Calculator')

Icon = pygame.image.load(r'C:\Users\t\Documents\pythonFiles\htmlTutorial\coffeeWebsite\pics\cup.png')


pygame.display.set_icon(Icon)


fontSize=15
pygame.font.init()
myfont = pygame.font.SysFont('Lucida Console', fontSize)



calc=""
ans=0
reset=False
timeVar=True
stringPointer=0


class Button:
    def __init__(self,value="",tX=0,tY=0,W=0,H=0,func=False) -> None:
        self.val=value
        self.tX=tX
        self.tY=tY
        self.width=W
        self.height=H
        self.func=func

    def doFunc(self):
        if self.func:
            if self.val=='DEL':
                self.dele()
                return
            if self.val=='=':
                self.sum()
                return
            self.clear()
            return
        self.pressed()

    def pressed(self):
        global calc
        calc=calc.replace('|','')
        if reset==True:
            self.clear()

        calc+=self.val+'|'



    def sum(self):
        global ans,calc
        calc=calc.replace("|","")
        try:
            ans=eval(calc)
        except:
            ans="ERROR"

    def clear(self):
        global calc,ans
        calc=""
        ans=0

    def dele(self):
        global calc
        if not(timeVar):
            calc=calc[:-1]
            return
        calc=calc[:-2]+"|"

    

    def render(self):
        self.obj=pygame.Rect(self.tX,self.tY,self.width,self.height)
        pygame.draw.rect(SCREEN,(255,255,255),self.obj)
        number=myfont.render(self.val,False,(0,0,0))
        midX=((self.tX)+(self.width+self.tX))//2-5
        midY=((self.tY)+(self.height+self.tY))//2-7
        SCREEN.blit(number,(midX,midY))

def timeFunc():
    global calc,timeVar
    timeVar=True
    while True:
            timeVar=not(timeVar)
            if timeVar:
                calc=calc.replace('|','')
                calc+="|"
            else:
                calc=calc.replace('|','')
            time.sleep(.6)


def isClick(but:Button,pos:tuple)->bool:
    if pos[0]>=but.tX and pos[0]<=(but.tX+but.width) and pos[1]>=but.tY and pos[1]<=(but.tY+but.height):
        return True
    return False

buttons=[]
bW=50
bH=35
y=140
symb=[['<-','->'],
      ['7','8','9','+','-'],
      ['4','5','6','*','/'],
      ['1','2','3','DEL','AC'],
      ['0','.','(',')','=']]
funcs=['DEL','AC','=','<-','->']

for row in symb:
    x=10
    y+=bH+10
    for sign in row:
        state=False
        if sign in funcs:
            state=True
        but=Button(sign,x,y,bW,bH,state)
        buttons.append(but)
        x+=bW+10


timeThr=Thread(target=timeFunc)
timeThr.daemon=True
timeThr.start()

while True:
    SCREEN.fill((0,0,0))
    for but in buttons:
        but.render()
    #p1.createBlip()
    #this makes the image the backgroiiiiiiiuuund
    for events in pygame.event.get():
        if events.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if events.type==pygame.MOUSEBUTTONDOWN and events.button==1:
            pos=pygame.mouse.get_pos()
            for but in buttons:
                if isClick(but,pos):
                    but.doFunc()
                    break
    inp=myfont.render(calc,False,(255,255,255))
    an=myfont.render(str(ans),False,(255,255,255))
    SCREEN.blit(an,(275,80))
    SCREEN.blit(inp,(5,5))

    pygame.display.update()

