import pygame
import sys
import random
import mysql.connector
from tkinter import *
# from ballonshooter import *
import tkinter_nav as tknav
from math import*

pygame.init()
id = None
width = 500
height = 500


display= pygame.display.set_mode((width,height))

clock =pygame.time.Clock()

margin = 100
lowerbound=100

score=0




#colors

white=(230,230,230)
lightblue=(174,214,234)
red=(231,76,60)
lightgreen=(25,111,61)
darkgray=(40,55,71)
darkblue=(21,67,96)
green=(35,155,86)
yeelow=(244,206,63)
blue=(46,134,193)
purple=(55,89,182)
orange=(243,156,18)
font=pygame.font.SysFont("snap itc",25)

class Ballon:
    def __init__(self,speed):
        self.a=random.randint(40,50)
        self.b=self.a+random.randint(0,10)

        self.x=random.randrange(margin,width-self.a-margin)
        self.y=height-lowerbound

        self.angle=90
        self.speed=-speed

        self.probpool=[-1,-1,-1,0,0,0,0,1,1,1]
        self.length=random.randint(50,100)
        self.color=random.choice([red,green,purple,orange,yeelow,blue])
    def move(self):
        direction=random.choice(self.probpool)
        if direction==-1:
            self.angle+=-10

        elif direction==0:
            self.angle+=0
        else:
            self.angle+=10

        self.y+=self.speed* sin(radians(self.angle))
        self.x+=self.speed *cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x< 0):
            if self.y > height/5:
                self.x = self.speed*cos(radians(self.angle))

            else:
             self.reset()

        if self.y+ self.b<0 or self.y>height+ 30:
            self.reset()


    def reset(self):
        self.a = random.randint(40, 50)
        self.b = self.a + random.randint(0, 10)

        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerbound

        self.angle = 90
        self.speed -=0.002

        self.probpool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, orange, yeelow, blue])

    def show(self):
        pygame.draw.line(display,darkblue,(self.x + self.a/2, self.y + self.b),(self.x+self.a/2,self.y+self.b + self.length))
        pygame.draw.ellipse(display,self.color,(self.x,self.y,self.a,self.b))
        pygame.draw.ellipse(display,self.color,(self.x +self.a/2 -5,self.y+ self.b -3,10,10))
    def burst(self):
        global score
        poss=pygame.mouse.get_pos()
        if onballon(self.x,self.y,self.a,self.b,poss):
            score+=1
            print(score)
            mySqlUpdate(score)
            self.reset()
ballons=[]
noBallons=10



def mySqlUpdate(score):
            global id
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sk"
            )
            mycursor = mydb.cursor()

            sql = "UPDATE players SET Scored=%s WHERE id=%s"
            # val = ("1",2,0)
            strvar=score
            b1 = (score, id,)
            mycursor.execute(sql, b1)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")

for i in range(noBallons):
    obj=Ballon(random.choice([1,1,2,2,2,2,3,3,3,4]))
    ballons.append(obj)


def pointer():
    poss = pygame.mouse.get_pos()
    r =25
    l =30
    color = lightgreen

    for i in range(noBallons):
        if (onballon(ballons[i].x,ballons[i].y,ballons[i].a,ballons[i].b,poss)) :
            color = red

    pygame.draw.ellipse(display, color, (poss[0] -r/2,poss[1] -r/2,r,r),4)
    pygame.draw.line(display, color, (poss[0], poss[1]-1/2), (poss[0], poss[1]-1), 4)
    pygame.draw.line(display, color, (poss[0]+1/2, poss[1]), (poss[0]+1, poss[1]), 4)
    pygame.draw.line(display, color, (poss[0], poss[1]+1/2), (poss[0], poss[1]+1), 4)
    pygame.draw.line(display, color, (poss[0]-1/2, poss[1]), (poss[0]-1, poss[1]), 4)

def lowerplatform():
    pygame.draw.rect(display,darkgray,(0,height- lowerbound,width,lowerbound))

def showscore():
    scoreText=font.render("Ballon Bursted : " +str(score),True,white)
    display.blit(scoreText,(100,height-lowerbound +30))

def close():
    pygame.quit()
    sys.exit()


def onballon(x,y,a,b,poss):
    if(x<poss[0]<x+a) and (y<poss[1]<y+b):
        return True
    else:
        False


def game():
    global score
    loop=True

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type==pygame.MOUSEBUTTONDOWN:
                for i in range(noBallons):
                    ballons[i].burst()




        display.fill(lightblue)
        for i in range(noBallons):
            ballons[i].show()





        for i in range(noBallons):
            ballons[i].move()
        pointer()
        lowerplatform()
        showscore()
        pygame.display.update()
        clock.tick(60)


#game()


window = Tk()
C = Canvas(window, bg="blue", height=200, width=100)
filename = PhotoImage(file = "bg.png")
background_label = Label(window, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
margin = 100
lowerbound=100
window.title("baloon popper game")
window.geometry('200x100')
window.configure(background = "white");
a = Label(window ,text = "First Name").grid(row = 0,column = 0)
b = Label(window ,text = "AGE").grid(row = 1,column = 0)

Name=StringVar()
Age=StringVar()
Entry(window,textvariable=Name).grid(row = 0,column = 1)
Entry(window,textvariable=Age).grid(row = 1,column = 1)

def clicked():
    print("Clicked")
    mySqlInsert()
    Name.set("")
    Age.set("")
    window.destroy()
    game()


def mySqlInsert():
    global id
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
        database="sk"
    )
    mycursor = mydb.cursor()

    sql = "INSERT INTO players(Name,Age,Scored) VALUES (%s,%s,%s)"
    # val = ("1",2,0)
    b1 = (Name.get(),Age.get(),"0")
    mycursor.execute(sql,b1)
    id = mycursor.lastrowid
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


btn = Button(window ,text="Submit",command=clicked).grid(row=6,column=0)

window.mainloop()