import pygame as pg
from pygame.locals import *
from random import randint as r
import os
import sqlite3
import json

import variables as v


from sys import exit
try:
    from functions import\
        get_value,\
        backup_image,\
        add_setting,\
        fullend,\
        load_menu,\
        move,\
        load_image,\
        load_image_with_no_file,\
        pikup,\
        score,\
        gamov
except FileNotFoundError:
    x=input('Не найдет файл functions.py\nНажмите любую клавишу для продолжения…')
    exit()



# база настроек

if os.path.exists('data/settings.db')==False:
    conn=sqlite3.connect('data/settings.db')
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings
                (setting TEXT NOT NULL, value TEXT NOT NULL)''')
    conn.commit()
    conn.close()

    add_setting('playerName',os.getlogin())
    add_setting('windowName','Змейка')
    add_setting('backgroundColor','0,0,0,')
    add_setting('backgroundPhotoIndicator','True')
    add_setting('selectedMusic',v.music_file_names[0])
    add_setting('musicValume','0.5')
    add_setting('windowSize','900,900,')
    add_setting('record','0')
    add_setting('label','True')
    add_setting('fps','15')
    add_setting('windowTitleBar','False')
    add_setting('lang','en')
    add_setting('keyUp','119')      #
    add_setting('keyDown','115')    #
    add_setting('keyRight','100')   #
    add_setting('keyLeft','97')     #
    add_setting('keyExit','127')    #
    add_setting('keyMenuOpen','27') #
    add_setting('keyMenuStart','1025,1')
    add_setting('keyMenuOtherGames','1025,2')
    add_setting('keyMenuExit','1025,1')
    add_setting('keyMenuSettings','')
    add_setting('keyMenuPsihodelOn','')
    add_setting('keyMenuPsihodelOff','')


v.lang='ru'#get_value('lang')
with open(f"data/translations/{v.lang}.json", "r",encoding="utf-8") as file:
    v.translations=json.load(file)

def keyUnpack(fullkey):
    newKey=['','']
    Flag=True
    for i in fullkey:
        if Flag:
            newKey[0]+=i
        else:
            newKey[1]+=i
        if i==',':
            Flag=False
    return newKey
# клавиши

v.Up=int(get_value('keyUp'))
v.Down=int(get_value('keyDown'))
v.Right=int(get_value('keyRight'))
v.Left=int(get_value('keyLeft'))

v.MenuOpen=int(get_value('keyMenuOpen'))
v.Exit=int(get_value('keyExit'))

v.MenuStart=keyUnpack(get_value('keyMenuStart'))
v.MenuOtherGames=keyUnpack(get_value('keyMenuOtherGames'))



# фпс

v.fps=int(get_value('fps'))



v.Player_name=get_value('playerName')

timeless=''
indic=-1

# настройка окна

pg.init()
pg.mixer.init()


for i in get_value('windowSize'):
    if i==',':
        indic+=1
        v.size[indic]=int(timeless)
        timeless=''
    else:
        timeless+=i


pg.display.set_caption(get_value('windowName'))

if get_value('windowTitleBar')=='False':
    v.win=pg.display.set_mode(v.size,pg.NOFRAME)
elif get_value('windowTitleBar')=='True':
    v.win=pg.display.set_mode(v.size)



# музыка

v.game_sound=pg.mixer.Sound('music/'+get_value('selectedMusic'))
v.game_sound.set_volume(float(get_value('musicValume')))




# задний фон

if get_value('backgroundPhotoIndicator')=='True':       v.background_photo_indicator=True
elif get_value('backgroundPhotoIndicator')=='False':    v.background_photo_indicator=False



v.score_max=int(float(get_value('record')))



# цвет фона

v.dolax=get_value('backgroundColor')



for i in v.dolax:
    if i!=',':
        v.dolax2+=i
    if i==',':
        v.dolax3.append(v.dolax2)
        v.dolax2=''


v.dolax_screen_color=(int(v.dolax3[0]),\
                      int(v.dolax3[1]),\
                      int(v.dolax3[2]))


# зимняя змея
if v.winter:
    try:
        try:
            v.head_image,v.head_rect=load_image("photo/new year snake.png",
                                                400,300,
                                                40,40)
            v.bodi_image,v.bodi_rect=load_image("photo/new year snake segment.png",
                                                370,300,
                                                35,35)
        except:
            backup_image('https://i.imgur.com/cw5kbMr.png','photo/new year snake.png')
            backup_image('https://i.imgur.com/OgqpRiK.png','photo/new year snake segment.png')

            v.head_image,v.head_rect=load_image("photo/new year snake.png",
                                                400,300,
                                                40,40)
            v.bodi_image,v.bodi_rect=load_image("photo/new year snake segment.png",
                                                370,300,
                                                35,35)
    except:
        v.head_image,v.head_rect=load_image_with_no_file((0,255,0),
                                                         400,300,
                                                         40,40)
        v.bodi_image,v.bodi_rect=load_image_with_no_file((0,255,0),
                                                         370,300,
                                                         35,35)


# летняя змея
if not v.winter:
    try:
        try:
            v.head_image,v.head_rect=load_image("photo/snake.png",\
                                            r(0,v.size[0]-30),\
                                            r(0,v.size[1]-30),30,30)
            v.bodi_image,v.bodi_rect=load_image("photo/snake segment.png",\
                                            r(0,v.size[0]-25),\
                                            r(0,v.size[1]-25),25,25)
        except:
            backup_image('https://i.imgur.com/CJvWSbU.png','photo/snake.png')
            backup_image('https://i.imgur.com/KOqDM9w.png','photo/snake segment.png')

            v.head_image,v.head_rect=load_image("photo/snake.png",\
                                            r(0,v.size[0]-30),\
                                            r(0,v.size[1]-30),30,30)
            v.bodi_image,v.bodi_rect=load_image("photo/snake segment.png",\
                                            r(0,v.size[0]-25),\
                                            r(0,v.size[1]-25),25,25)
    except:
        v.head_image,v.head_rect=load_image_with_no_file((0,255,0),\
                                                    r(0,v.size[0]-30),\
                                                    r(0,v.size[1]-30),30,30)
        v.bodi_image,v.bodi_rect=load_image_with_no_file((0,255,0),\
                                                    r(0,v.size[0]-25),\
                                                    r(0,v.size[1]-25),25,25)
v.snake=[v.head_rect,v.bodi_rect]


# яблоко
try:
    try:
        v.apple_image,v.apple_rect=load_image("photo/aple.png",\
                                        r(0,v.size[0]-40),\
                                        r(0,v.size[1]-50),40,50)
    except:
        backup_image('https://i.imgur.com/54AIiPl.png','photo/aple.png')
        v.apple_image,v.apple_rect=load_image("photo/aple.png",\
                                        r(0,v.size[0]-40),\
                                        r(0,v.size[1]-50),40,50)
except:
    v.apple_image,v.apple_rect=load_image_with_no_file((255,255,0),\
                                                r(0,v.size[0]-40),\
                                                r(0,v.size[1]-50),40,50)


# ель
try:
    v.el_image,v.el_rect=load_image("photo/el.png",
                                    800,800,
                                    100,100)
except:
    backup_image('https://i.imgur.com/fzh7pAn.png','photo/el.png')
    v.el_image,v.el_rect=load_image("photo/el.png",
                                    800,800,
                                    100,100)


# фон
try:
    v.bg=pg.image.load("photo/image.png")

except:
    backup_image('https://i.imgur.com/Lzl6zSf.png','photo/image.png')
    v.bg=pg.image.load("photo/image.png")








'''                                   ИГРОВОЙ ЦИКЛ                                        '''
'''#######################################################################################'''



load_menu()


while v.ply:
    #try:
    if True:
        if v.random_name_ndicator==True:
            v.rand_slovo_name=list(v.rand_slovo_list[r(1,len(v.rand_slovo_list)-1)].lower())
            v.rand_slovo_name[0]=v.rand_slovo_name[0].upper()
            for i in v.rand_slovo_name:
                v.rand_slovo_name2+=i

            pg.display.set_caption(v.rand_slovo_name2)

        if v.qwertyuiop==0:
            if not v.timer<0:
                v.timer-=1
                v.game_point+=0.05

        if v.qwertyuiop==1:
            v.timer+=1

        if v.timer<0:
            fullend(True)

        v.win.fill(v.dolax_screen_color)

        for event in pg.event.get():
            if event.type==pg.QUIT:
                v.ply=False

        v.KEYS=pg.key.get_pressed()

        if v.background_photo_indicator:
            v.win.blit(v.bg,(0,0))

        if v.winter:
            pass
            #v.win.blit(v.el_image,v.el_rect)
        v.win.blit(v.head_image,v.head_rect)
        v.win.blit(v.apple_image,v.apple_rect)

        for seg in v.snake[1:]:
            v.win.blit(v.bodi_image,seg)


        move(v.head_rect,v.snake)
        pikup()
        score()

        if gamov():
            fullend(True)

        pg.display.update()
        v.clock.tick(v.fps)
    #except Exception as e:
     #   write_error_to_file(str(e))

fullend(False)
#pyinstaller --onefile --icon=photo/icon.ico game.py