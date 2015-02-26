# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 21:20:09 2015

@author: zhangbohun
"""
import pygame
import random
from sys import exit

#初始化窗口
pygame.init()
pygame.display.set_caption('打打打打打飞机')#设置窗口标题
screen=pygame.display.set_mode((370,600))
pygame.mouse.set_visible(False)#隐藏光标

#加载素材
#图片
boom1=pygame.image.load("resources/image/boom1.png")
boom2=pygame.image.load("resources/image/boom2.png")
bullet=pygame.image.load("resources/image/bullet.png")
plane = pygame.image.load("resources/image/plane.png")
enemy = pygame.image.load("resources/image/enemy.png")
pygame.display.set_icon(plane)#顺便设置窗口icon
background1 = pygame.image.load("resources/image/bg_01.png")
background2 = pygame.image.load("resources/image/bg_02.png")
start=pygame.image.load("resources/image/start.png")
pause=pygame.image.load("resources/image/pause.png")

#音效
pygame.mixer.init()
Xexplosion = pygame.mixer.Sound("resources/audio/explosion.wav")
Xshoot = pygame.mixer.Sound("resources/audio/shoot.wav")
Xgame_over = pygame.mixer.Sound("resources/audio/game_over.wav")
Xexplosion.set_volume(1)
Xshoot.set_volume(0.5)
Xgame_over.set_volume(4.5)
#背景音乐
pygame.mixer.music.load('resources/audio/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)
    
#背景切换参数
i=0
#得分
score=0
font = pygame.font.SysFont('微软雅黑', 36)  
#子弹
bullets = []
#敌机
enemies = []
#记录敌机爆炸位置
boomplace=[]
#游戏结束标志
game_over=False
#飞机位置初始化
pygame.mouse.set_pos(185, 550)

#程序主循环
while True:
    #背景切换
    i+=1
    if i<100:
        screen.blit(background1, (0, 0))
        screen.blit(pause, (0, 0)) 
    elif i<200:
        screen.blit(background2, (0, 0))
        screen.blit(pause, (0, 0)) 
    else:
        i=0
    
    #鼠标控制我的飞机  
    x,y=pygame.mouse.get_pos()
    x-= plane.get_width() / 2
    y-= plane.get_height() / 2
    screen.blit(plane, (x, y))

    #子弹发射，移动，消失   
    if i%25==0:
        l,m,r =pygame.mouse.get_pressed()
        if l==True:
            bullets.append([x+plane.get_width() / 2,y])
            Xshoot.play()#播放音效
            for place in bullets:
                if place[1]<=0:
                    bullets.remove(place)
        for place in bullets:
                place[1]-=55         
    for place in bullets:      
        screen.blit(bullet, (place[0],place[1] )) 
            
    #敌机生成，移动，消失
    if i%100==0:
        enemies.append([random.choice(range(0,370-enemy.get_width())),-enemy.get_width() / 2])
        for place in enemies:
            if place[1]>=600:
                enemies.remove(place)
        for place in enemies:
            place[1]+=35
    
    for place in enemies:      
        screen.blit(enemy, (place[0],place[1] )) 
    
    #敌机爆炸显示
    for place in boomplace: 
        if place[2]>0:
            screen.blit(boom1, (place[0],place[1] )) 
            place[2]-=1

    #子弹碰撞检测
    for bulletplace in bullets:
        for enemyplace in enemies:
            if (bulletplace[0] > enemyplace[0] and bulletplace[0] < enemyplace[0] + enemy.get_width()) and (bulletplace[1] > enemyplace[1] and bulletplace[1] < enemyplace[1] + enemy.get_height()):
                screen.blit(boom1, (enemyplace[0],enemyplace[1] ))
                boomflag=75
                enemyplace.append(boomflag)
                boomplace.append(enemyplace)
                enemies.remove(enemyplace)
                bullets.remove(bulletplace)
                Xexplosion.play()#播放音效
                score+=100
                   
    #飞机碰撞检测
    for enemyplace in enemies:
        if (x + 0.7*plane.get_width() > enemyplace[0]) and (x + 0.3*plane.get_width() < enemyplace[0] + enemy.get_width()) and (y + 0.7*plane.get_height() > enemyplace[1]) and (y + 0.3*plane.get_height() < enemyplace[1] + enemy.get_height()):
            enemies.remove(enemyplace)
            if i<100:
                screen.blit(background1, (0, 0))
            elif i<200:
                screen.blit(background2, (0, 0)) 
            Xgame_over.play()#播放音效
            #重绘图案    
            screen.blit(pause, (0, 0))    
            screen.blit(boom2, (x, y))
            for place in bullets:      
                screen.blit(bullet, (place[0],place[1] )) 
            for place in enemies:      
                screen.blit(enemy, (place[0],place[1] ))   
            #显示最终得分
            text = font.render("Final Score: %d" % score, 1, (0, 0, 0))
            screen.blit(text, (78, 270)) 
            text = font.render("Press Right Button to Restart", 1, (0, 0, 0))
            screen.blit(text, (15, 320)) 
            pygame.display.update()#显示重绘
            
            game_over=True
            while game_over==True and r==False :
                l,m,r =pygame.mouse.get_pressed()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
            #重置游戏
            i=0
            score=0
            bullets = []
            enemies = []
            boomplace=[]
            x,y=185- plane.get_width() / 2, 550- plane.get_height() / 2
                
    #检测暂停，继续
    l,m,r =pygame.mouse.get_pressed()
    if r==True:
        #重绘背景
        if i<100:
            screen.blit(background1, (0, 0))
        elif i<200:
            screen.blit(background2, (0, 0))
        #重绘图案    
        screen.blit(start, (0, 0))    
        screen.blit(plane, (x, y))
        for place in bullets:      
            screen.blit(bullet, (place[0],place[1] )) 
        for place in enemies:      
            screen.blit(enemy, (place[0],place[1] )) 
        for place in boomplace: 
            if place[2]>0:
                screen.blit(boom1, (place[0],place[1] )) 
                place[2]-=1
        text = font.render(u"%d" % score, 1, (0, 0, 0))
        screen.blit(text, (50, 0))
        if game_over==True:
            x,y=185, 550#重置飞机位置
            game_over=False
            text = font.render("Press Left Button to Start", 1, (0, 0, 0))
            screen.blit(text, (35, 300)) 
        else:
            x,y=pygame.mouse.get_pos()#保存飞机位置
            text = font.render("Press Left Button to Continue", 1, (0, 0, 0))
            screen.blit(text, (10, 300)) 
        pygame.display.update()#更新重绘
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            l,m,r =pygame.mouse.get_pressed()
            #继续
            if l==True:
                pygame.mouse.set_pos(x, y)#鼠标返回暂停前位置
                break
                      
    text = font.render(u"%d" % score, 1, (0, 0, 0))
    screen.blit(text, (50, 0))       
    #检测是否结束        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    pygame.display.update()