from random import randint as r
import sqlite3
import pygame as pg
import os

#база данных рекордов
conn=sqlite3.connect('data\scores.db')
baza=conn.cursor()

baza.execute('''CREATE TABLE IF NOT EXISTS scores
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 score INTEGER NOT NULL)''')

Up=0
Down=0
Right=0
Left=0

MenuOpen=0
Exit=0

MenuStart=0
MenuOtherGames=0
MenuExit=0


lang=0
translations=0


z2=r(0,740)
z1=r(0,740)
z=r(0,740)

random_name_ndicator=False


don=False


music_file_names=[]


for filename in 'assets/music':
    if filename.endswith('.wav'):
        music_file_names.append(filename)

music_names=[]

for i in music_file_names:
    i=list(i)
    if i[-4:]==list('.wav'):
        for n in range(4):
            i.pop(-1)
    n=''
    for nii in i:
        n+=nii
    music_names.append(n)





Player_name=''


size=[900,900]

win=0

screen=pg.Surface(size)

clock=pg.time.Clock()

pg.init()
pg.mixer.init()


nym_sound=pg.mixer.Sound("assets/sounds/nym.wav")
nym_sound.set_volume(0.5)

menu_music=pg.mixer.Sound("assets/music/menu.wav")
menu_music.set_volume(0.1)



click_sound=pg.mixer.Sound("assets/sounds/click.wav")
click_sound.set_volume(0.5)

game_sound='0'

ply=True

timer=100

q=r(0,255)

psihodel_indicator=False

cxz=0

background_photo_indicator=True

background_color=(0,0,0)
dolax2=''
dolax3=[]

screen_colors=()

qwertyuiop=0

erro=0

SPEED=30

DIR=[SPEED,0]

head=pg.Rect(450,450,100,100)

game_point=0



image=pg.Surface((30,30))
image.fill((0,255,0))



head_image,head_rect='0','0'


bodi_image,bodi_rect='0','0'



apple_image,apple_rect='0','0'



cursor=''
cursor_rect=''

bg='0'


try:
    file=open('data/allwords.txt')
    rand_slovo_list=file.readlines()
    file.close()
except:
    print('не найден файл allwords.txt')


rand_slovo_name='0'

rand_slovo_name2=''

snake=[head_rect,bodi_rect]


KEYS=0

volume=0

root=0

score_max=0

fps=15