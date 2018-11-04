# -*- coding: utf-8 -*-
import pygame
import random
import sys

# pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
# turn all of pygame on.
pygame.init()
screen = pygame.display.set_mode((288, 512))
background = pygame.image.load("./assets/background.png")
pygame.display.set_caption("Flappy Bird")                                           

bgm=pygame.mixer.Sound('sound/bgm.wav')
channel_1=pygame.mixer.Channel(1)
channel_1.play(bgm)

#⑦新的代码：创建变量score
score=0


class Bird(pygame.sprite.Sprite):
#⑦新的代码：声明是全局变量
    #精灵对象：鸟
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.birdSprites = [pygame.image.load("assets/0.png"), pygame.image.load("assets/1.png") ,pygame.image.load("assets/2.png") ]      #生成一个列表
        self.a = 0
        self.birdX = 50
        #初始x坐标
        self.birdY = 100
        #初始y坐标
        self.jumpSpeed = 7
        #跳跃速度
        self.gravity = 0.4
        #在图像表面加载可以用来碰撞检测的矩形
        self.rect=self.birdSprites[self.a].get_rect()
        self.rect.center=(self.birdX,self.birdY)
        #跳跃重力

    def birdUpdate(self):
        self.jumpSpeed -= self.gravity
        self.birdY -= self.jumpSpeed
#②新的代码
        self.rect.center=(self.birdX,self.birdY)
        # print(self.rect,self.birdY)

        if self.jumpSpeed < 0: # 当y向量<0时，鸟下坠
            self.a = 1
        if self.jumpSpeed > 0:#否者上升
            self.a = 2

        if newBird.rect.top>ground.rect.top:
            self.rect.centery=ground.rect.top
#⑦新的代码
        else:
            print(self.rect.left, newWall.wallUpRect.right)
            global score   
            if self.rect.left == newWall.wallUpRect.right :

                score = score+1


#⑤新的代码
    def birdCrush(self):
        global keep_going
        resultU=self.rect.colliderect(newWall.wallUpRect)
        resultD=self.rect.colliderect(newWall.wallDownRect)
        

        if resultU or resultD or newBird.rect.bottom>=ground.rect.top:

            hit=pygame.mixer.Sound('sound/hit.wav')
            channel_3=pygame.mixer.Channel(2)
            channel_3.play(hit)

            keep_going=False






class Wall():
    def __init__(self):
        self.wallUp = pygame.image.load("assets/bottom.png")
        self.wallDown = pygame.image.load("assets/top.png")
        self.wallUpRect=self.wallUp.get_rect()
        self.wallDownRect=self.wallDown.get_rect()


        self.gap = 50                                                                                              #缝隙间隔
        self.wallx = 288
        self.offset = random.randint(-50, 50) #offset是相对于当前的位置移动的距离

#③新的代码
        self.wallUpY=360 + self.gap - self.offset
        self.wallDownY=0- self.gap - self.offset
        
#④新的代码
        self.wallUpRect.center=(self.wallx,self.wallUpY)
        self.wallDownRect.center=(self.wallx,self.wallDownY)

    def wallUpdate(self):
        self.wallx -= 2  #速度为2
#④新的代码
        self.wallUpRect.center=(self.wallx,self.wallUpY)
        self.wallDownRect.center=(self.wallx,self.wallDownY)
        # print(self.wallDownRect.center,self.wallx)

        if self.wallx < -80: #循环
            self.wallx = 288
            self.offset = random.randint(-50, 50)
            self.wallUpY=360 + self.gap - self.offset
            self.wallDownY=0- self.gap - self.offset

#⑨新的代码

class Text():
    """docstring for showText"""

    def __init__(self,content):
        red=(100,50,50)   
        self.color=red 
        self.font=pygame.font.SysFont(None,52)
        #SysFont(字体名, 大小) -> Font
        contentStr=str(content)
        self.image=self.font.render(contentStr,True,self.color)
        #pygame.font.render(你想要渲染的文字内容, 渲染出来的文字是否更平滑呢, 文字的颜色）


    def updateText(self,content):
        contentStr=str(content)
        self.image=self.font.render(contentStr,True,self.color)


class Ground():
    def __init__(self):
        self.image=pygame.image.load("assets/ground.png")
        self.rect=self.image.get_rect()
        self.rect.bottom=560
        self.rect.left=-30



#①初始化界面，创建小鸟，水管，文字对象
newBird=Bird() #创建对象
newWall=Wall()
#⑨新的代码
coolText=Text(score)
keep_going = True
clock =pygame.time.Clock()

#11新的代码
endText=Text("END")

ground=Ground()


highest_score=0



while True: #主循环

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #直接退出主循环,结束所有进程
            sys.exit()

        if keep_going:
            if (event.type == pygame.MOUSEBUTTONDOWN):
                newBird.jumpSpeed = 7

                channel_2=pygame.mixer.Channel(3)
                fly=pygame.mixer.Sound('sound/fly.WAV')
                channel_2.play(fly)

        else:
            if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        #重置游X戏参数，重新开始
                        keep_going=True
                        score=0 
                        newBird.birdX = 50                                                             #初始x坐标
                        newBird.birdY = 100   
                        newWall.wallx=288
                        newBird.jumpSpeed=7

#绘制           
    screen.blit(background,(0, 0))
    screen.blit(newBird.birdSprites[newBird.a],newBird.rect)
    screen.blit(newWall.wallUp,newWall.wallUpRect)
    screen.blit(newWall.wallDown,newWall.wallDownRect)
    screen.blit(coolText.image,(10,10))

    screen.blit(ground.image,ground.rect)

#更新
    newWall.wallUpdate()
    newBird.birdUpdate()


#是否绘制分数，检测小鸟撞毁
    if keep_going:
        newBird.birdCrush()   
        coolText.updateText(score) 
    else:
        screen.blit(endText.image,(110,230))   

        if score> highest_score:
            highest_score=score
        highest_score_text=Text('best play:'+str(highest_score))

        screen.blit(highest_score_text.image,(50,270))



    
    pygame.display.update()   
    clock.tick(60)    

 
