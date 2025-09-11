import pygame as pg
from pygame.locals import *
from random import randint as r
import os
import sqlite3
import json
import datetime
import variables as v


from sys import exit

from functions import\
    get_value,\
    add_setting,\
    fullend,\
    load_menu,\
    move,\
    load_image,\
    load_image_with_no_file,\
    pikup,\
    score,\
    gamov



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

v.game_sound=pg.mixer.Sound('assets/music/gameplay/'+get_value('selectedMusic'))
v.game_sound.set_volume(float(get_value('musicValume')))




# задний фон

if get_value('backgroundPhotoIndicator')=='True':       v.background_photo_indicator=True
elif get_value('backgroundPhotoIndicator')=='False':    v.background_photo_indicator=False



v.score_max=int(float(get_value('record')))



# цвет фона

v.background_color=get_value('backgroundColor')



for i in v.background_color:
    if i!=',':
        v.dolax2+=i
    if i==',':
        v.dolax3.append(v.dolax2)
        v.dolax2=''


v.screen_colors=(v.background_color)


# зима
if datetime.datetime.now().month in [12,1,2]:
    skins=["assets/textures/new year snake.png",            r(0,v.size[0]-40),r(0,v.size[1]-40), 40,40,
           "assets/textures/new year snake segment.png",    r(0,v.size[0]-35),r(0,v.size[1]-35), 35,35]
    print('Winter skins will be applied')
else:
    skins=["assets/textures/snake.png",            r(0,v.size[0]-30),r(0,v.size[1]-30), 30,30,
           "assets/textures/snake segment.png",    r(0,v.size[0]-25),r(0,v.size[1]-25), 25,25]


try:
    v.head_image,v.head_rect=load_image(skins[0],
                                        skins[1],skins[2],  # координаты
                                        skins[3],skins[4])  # размеры
    v.bodi_image,v.bodi_rect=load_image(skins[5],
                                        skins[6],skins[7],  # координаты
                                        skins[8],skins[9])  # размеры

except:
    v.head_image,v.head_rect=load_image_with_no_file((0,255,0),
                                                    skins[1],skins[2],  # координаты
                                                    skins[3],skins[4])  # размеры
    v.bodi_image,v.bodi_rect=load_image_with_no_file((0,255,0),
                                                    skins[6],skins[7],  # координаты
                                                    skins[8],skins[9])  # размеры
    print("Сouldn't restore snake texture, replaced with simple shapes")

v.snake=[v.head_rect,v.bodi_rect]




'''
try:
    v.head_image,v.head_rect=load_image(skins[0],
                                            r(0,v.size[0]-30),
                                            r(0,v.size[1]-30),30,30)
    v.bodi_image,v.bodi_rect=load_image("assets/textures/snake segment.png",
                                            r(0,v.size[0]-25),
                                            r(0,v.size[1]-25),25,25)

except:
    v.head_image,v.head_rect=load_image_with_no_file((0,255,0),
                                                    r(0,v.size[0]-30),
                                                    r(0,v.size[1]-30),30,30)
    v.bodi_image,v.bodi_rect=load_image_with_no_file((0,255,0),
                                                    r(0,v.size[0]-25),
                                                    r(0,v.size[1]-25),25,25)'''



# яблоко
try:
    v.apple_image,v.apple_rect=load_image("assets/textures/apple.png",\
                                          r(0,v.size[0]-40),\
                                          r(0,v.size[1]-50),40,50)

except:
    v.apple_image,v.apple_rect=load_image_with_no_file((255,255,0),\
                                                r(0,v.size[0]-40),\
                                                r(0,v.size[1]-50),40,50)



# фон
try:
    v.bg=pg.image.load("assets/textures/image.png")

except:
    pass





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

        v.win.fill(v.screen_colors)

        for event in pg.event.get():
            if event.type==pg.QUIT:
                v.ply=False

        v.KEYS=pg.key.get_pressed()

        if v.background_photo_indicator:
            v.win.blit(v.bg,(0,0))

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