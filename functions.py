import sqlite3
import requests
import pygame as pg
from pygame.locals import *
import easygui as eg
import tkinter as tk
from random import randint as r
import shutil
import os
import datetime

from sys import exit
try:
    import variables as v
except FileNotFoundError:
    x=input(v.translations['variablesNotFound'])
    exit()
import variables as v

def write_error_to_file(error_message):
    current_time=datetime.datetime.now()
    error_file_name=f'''data/crash-reports/{current_time.strftime('%Y-%m-%d_%H.%M.%S')}.txt'''
    with open(error_file_name,'w') as file:
        file.write(error_message)
    crash_report_files=os.listdir('data/crash-reports')
    if len(crash_report_files)>100:
        oldest_file=min(crash_report_files,key=lambda x:os.path.getctime(os.path.join('data/crash-reports',x)))
        os.remove('data/crash-reports/'+str(oldest_file))
    pg.quit()
    input(f'{v.translations["crash"]} {error_file_name}')
    import time
    time.sleep(5)
    exit()
    



def get_value(setting):
    conn=sqlite3.connect('data/settings.db')
    cursor=conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE setting=?', (setting,))
    row=cursor.fetchone()
    if row:
        return row[0]
    else:
        return None



def add_setting(setting,value):
    conn=sqlite3.connect('data/settings.db')
    cursor=conn.cursor()
    cursor.execute('INSERT INTO settings (setting,value) VALUES (?,?)', (setting,value))
    conn.commit()
    conn.close()



def increase_volume():
    if v.volume.get()<10:
        v.volume.set(v.volume.get()+1)



def decrease_volume():
    if v.volume.get()>0:
        v.volume.set(v.volume.get()-1)




def on_closing():
    v.game_sound.set_volume(v.volume.get())
    update_value('musicValume',float('0.'+str(v.volume.get())))
    v.root.destroy()




def update_value(setting,value):
    conn=sqlite3.connect('data/settings.db')
    cursor=conn.cursor()
    cursor.execute('UPDATE settings SET value=? WHERE setting=?', (value,setting))
    conn.commit()
    conn.close()




def backup_image(img_url,save_path):
    response=requests.get(img_url,headers={'User-agent':'your bot 0.1'})
    #print(f'Файл восстановлен')
    if response.status_code==200:
        with open(save_path,'wb') as f:
            f.write(response.content)
    else:
        eg.msgbox(f'{v.translations["restoreError"]} {response.status_code}')




# Функция для добавления нового результата
def add_score(name,score):
    if score>0:
        v.baza.execute('INSERT INTO scores (name,score) VALUES (?, ?)', (name,score))
        v.conn.commit()
        # Сортируем таблицу после добавления нового результата
        v.baza.execute('CREATE TABLE temp AS SELECT * FROM scores ORDER BY score DESC')
        v.baza.execute('DROP TABLE scores')
        v.baza.execute('ALTER TABLE temp RENAME TO scores')
        v.conn.commit()
        v.baza.execute('SELECT COUNT(*) FROM scores')
        if v.baza.fetchone()[0]>10:
            v.baza.execute('DELETE FROM scores WHERE score = (SELECT MIN(score) FROM scores)')
            v.conn.commit()



# Функция для получения всех рекордов
def get_all_scores():
    v.baza.execute('SELECT name, score FROM scores')
    return v.baza.fetchall()



def score_save():
    if int(v.score_max)<v.game_point:
        update_value('record',str(v.game_point))

    v.baza.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    add_score(v.Player_name,int(v.game_point))




def fullend(onofindicator):
    update_value('playerName',v.Player_name)
    update_value('backgroundPhotoIndicator',str(v.background_photo_indicator))
    zxc=''
    for i in v.dolax_screen_color:
        zxc+=str(i)+','
    update_value('backgroundColor',zxc)

    if onofindicator:
        score_save()
        pg.quit()
        рекорды=get_all_scores()
        all_scores=''
        for i in range(0,10):
            try:
                all_scores+=f'{i+1}) {рекорды[i][0]} {рекорды[i][1]}\n'
            except:
                break
        if eg.msgbox(all_scores,title=v.translations['records'])!=None:
            v.click_sound.play()
        exit()
    else:
        score_save()
        pg.quit()
        exit()




def load_menu():
    items=[(350,140,v.translations['play'],(0,0,0),(255,0,0),0),
           (380,650,v.translations['quit'],(0,0,0),(255,0,0),1)]
    pg.key.set_repeat(0,0)
    pg.mouse.set_visible(True)
    v.don=False
    p1=0
    p2=0
    p3=0
    item=0

    '''def startFromMenu():
        v.click_sound.play()
        v.don=True
    def otherGames():
        v.click_sound.play()
        othgamesindicator=eg.ynbox('Установить другие игры?')
        if othgamesindicator!=None:
            v.click_sound.play()
        if othgamesindicator==True:
            исходная_папка=r'other/'
            work_table=os.path.expanduser('~/Desktop')
            try:
                for файл in os.listdir(исходная_папка):
                    путь_исходного_файла=os.path.join(исходная_папка,файл)
                    путь_назначения=os.path.join(work_table,файл)
                    shutil.copy2(путь_исходного_файла,путь_назначения)
                if eg.msgbox('Игры установленны')!=None:
                    v.click_sound.play()
            except Exception as ащибка:
                if eg.msgbox(f'Произошла ошибка: {ащибка}')!=None:
                    v.click_sound.play()'''


    while not v.don: 
        v.menu_music.play()
        v.screen.fill([p1,p2,p3])
        v.win.fill((p1,p2,p3))
        for e in pg.event.get():
            if e.type==pg.QUIT:
                fullend(False)

            if item==0:
                if e.type==pg.MOUSEBUTTONDOWN:
                    if e.button==1 or e.button==3:
                        v.click_sound.play()
                        v.don=True

                    if e.button==2:
                        v.click_sound.play()
                        othgamesindicator=eg.ynbox('Установить другие игры?')
                        if othgamesindicator!=None:
                            v.click_sound.play()
                        if othgamesindicator==True:
                            исходная_папка=r'other/'
                            work_table=os.path.expanduser('~/Desktop')
                            try:
                                for файл in os.listdir(исходная_папка):
                                    путь_исходного_файла=os.path.join(исходная_папка,файл)
                                    путь_назначения=os.path.join(work_table,файл)
                                    shutil.copy2(путь_исходного_файла,путь_назначения)
                                if eg.msgbox('Игры установленны')!=None:
                                    v.click_sound.play()
                            except Exception as ащибка:
                                if eg.msgbox(f'Произошла ошибка: {ащибка}')!=None:
                                    v.click_sound.play()
                '''
                if int(get_value('keyMenuStart')[0])==pg.MOUSEBUTTONDOWN:
                    if e.type==pg.MOUSEBUTTONDOWN:
                        if e.button==v.MenuStart[1]:
                            startFromMenu()
                        elif e.button==v.MenuOtherGames[1]:
                            otherGames()
                else:
                    if e.type==v.MenuStart[0]:
                        startFromMenu()
                if (e.type,e.button)==v.MenuStart or (e.type,e.key)==v.MenuStart:
                    startFromMenu()'''
                        

            elif item==1:
                if e.type==pg.MOUSEBUTTONDOWN and e.button==1:
                    v.click_sound.play()
                    fullend(False)
                elif e.type==pg.MOUSEBUTTONDOWN and e.button==2:
                    v.click_sound.play()    
                    p1=r(0,255)
                    p2=r(0,255)
                    p3=r(0,255)
                    #background_photo_indicator=False
                elif e.type==pg.MOUSEBUTTONDOWN and e.button==3:
                    zzz=eg.buttonbox(v.translations['menu'],choices=
                        [v.translations['playerName'],
                         v.translations['records'],
                         v.translations['settings']])
                    if zzz!=None:
                        v.click_sound.play()
                    if zzz==v.translations['playerName']:
                        v.Player_name_2=v.Player_name
                        Player_name=str(eg.enterbox(v.translations['enterName'],default=Player_name))
                        if v.Player_name!=None:
                            v.click_sound.play()
                        elif v.Player_name==None:
                            v.Player_name=v.Player_name_2
                        else:
                            if v.Player_name=='' or v.Player_name==' ' or v.Player_name==' ':
                                    v.Player_name=v.Player_name_2
                            if v.Player_name[0]==' ' or v.Player_name[0]==' ':
                                while True:
                                    if v.Player_name[0]==' ' or v.Player_name[0]==' ':
                                        v.Player_name[0]=''
                                    else:
                                        break
                                v.Player_name=v.Player_name_2
                                
                    elif zzz==v.translations['records']:
                        рекорды=get_all_scores()
                        all_scores=''
                        for i in range(0,10):
                            try:
                                all_scores+=f'{i+1}) {рекорды[i][0]} {рекорды[i][1]}\n'
                            except:
                                break
                        if eg.msgbox(all_scores,title=v.translations['records'])!=None:
                            v.click_sound.play()

                    elif zzz==v.translations['settings']:
                        zzzz=eg.buttonbox(v.translations['settings'],choices=[
                            v.translations['windowName'],
                            v.translations['backgroungColor'],
                            v.translations['music'],
                            v.translations['volume'],
                            v.translations['windowSize'],
                            v.translations['fps'],
                            v.translations['windowTitle'],
                            v.translations['crashes'],
                            '…'])

                        if zzzz!=None:
                            v.click_sound.play()

                        if zzzz==v.translations['crashes']:
                            if len(os.listdir('data/crash-reports'))>=2:
                                os.startfile(os.path.normpath(
                                    'data/crash-reports/'+eg.choicebox('Репорты о сбоях',
                                    title=v.translations['crashes'],
                                    choices=os.listdir('data/crash-reports'))))
                            else:
                                eg.msgbox('Слишком мало репортов',title=v.translations['crashes'])
                        elif zzzz==v.translations['windowTitle']:
                            qwe=eg.buttonbox(v.translations['windowTitle'],choices=['Включить','Выключить'])
                            if qwe=='Включить':
                                update_value('windowTitleBar','True')
                                v.win=pg.display.set_mode(v.size)
                            elif qwe=='Выключить':
                                update_value('windowTitleBar','False')
                                v.win=pg.display.set_mode(v.size,pg.NOFRAME)


                        elif zzzz==v.translations['windowName']:
                            usler=eg.enterbox(v.translations['windowName'],default=get_value('windowName'))
                            if usler=='random()':
                                update_value('windowName','random.stop()')
                                v.click_sound.play()
                                v.random_name_ndicator=True
                            elif usler=='random.stop()':
                                update_value('windowName','random.stop()')
                                v.click_sound.play()
                                v.random_name_ndicator=False
                            else:
                                if usler!=None:
                                    update_value('windowName',usler)
                                    v.click_sound.play()
                                    pg.display.set_caption(usler)

                        if zzzz==v.translations['windowSize']:
                            z=int(eg.enterbox(v.translations['windowLength']))
                            if z!=None:
                                v.click_sound.play()
                            v.size[0]=z
                            z=int(eg.enterbox(v.translations['windowWidth']))
                            if z!=None:
                                v.click_sound.play()
                            v.size[1]=z
                            v.win=pg.display.set_mode(v.size)

                        elif zzzz==v.translations['music']:
                            zz=eg.buttonbox(v.translations['music'],choices=v.music_names,title=v.translations['musicAdd'])

                            if zz!=None:
                                v.click_sound.play()
                            try:
                                v.game_sound=pg.mixer.Sound('music/'+zz+'.wav')
                                v.game_sound.set_volume(float(get_value('musicValume')))
                                update_value('selectedMusic',zz+'.wav')
                            except:
                                pass

                        elif zzzz==v.translations['volumeSettings']:
                            v.root=tk.Tk()
                            v.root.title(v.translations['volumeSettings'])

                            label=tk.Label(v.root,text=v.translations['volumeSettings'])
                            label.pack()

                            v.volume=tk.IntVar(value=int(float(get_value('musicValume'))*10))

                            up_button=tk.Button(v.root,text='↑',command=increase_volume)
                            up_button.pack()

                            volume_label=tk.Label(v.root,textvariable=v.volume)
                            volume_label.pack()

                            down_button = tk.Button(v.root,text='↓',command=decrease_volume)
                            down_button.pack()

                            v.root.protocol('WM_DELETE_WINDOW',on_closing)
                            v.root.mainloop()

                        elif zzzz=='FPS':
                            update_value('fps',eg.enterbox('FPS',default=get_value('fps'),
                                                           title=v.translations['fpsChange']))
                            v.fps=int(get_value('fps'))

                        elif zzzz==v.translations['backgroungColor']:
                            zz=eg.buttonbox(v.translations['colors'],choices=[
                                v.translations['photo'],
                                v.translations['red'],
                                v.translations['yellow'],
                                v.translations['green'],
                                v.translations['marrsGreen'],
                                v.translations['blue'],
                                v.translations['purpule'],
                                v.translations['otherColor']])
                            if zz!=None:
                                v.click_sound.play()

                            if zz==v.translations['photo']:
                                v.background_photo_indicator=True

                            elif zz==v.translations['red']:
                                v.dolax_screen_color=(255,0,0)
                                v.background_photo_indicator=False

                            elif zz==v.translations['yellow']:
                                v.dolax_screen_color=(255,255,0)
                                v.background_photo_indicator=False

                            elif zz==v.translations['green']:
                                v.dolax_screen_color=(0,255,0)
                                v.background_photo_indicator=False

                            elif zz==v.translations['marrsGreen']:
                                v.dolax_screen_color=(0,255,170)
                                v.background_photo_indicator=False

                            elif zz==v.translations['blue']:
                                v.dolax_screen_color=(0,0,255)
                                v.background_photo_indicator=False

                            elif zz==v.translations['purpule']:
                                v.dolax_screen_color=(139,0,255)
                                v.background_photo_indicator=False

                            else:
                                do=eg.enterbox(v.translations['colorCode'],default=0)
                                if do!=None:
                                    v.click_sound.play()
                                if not do=='':
                                    try:
                                        dd=int(do)
                                        if dd>255:
                                            dd=255
                                        elif dd<0:
                                            dd=0
                                    except ValueError:
                                        dd=0
                                else:
                                    dd=0
                                do=eg.enterbox(v.translations['colorCode'],default=0)
                                if do!=None:
                                    v.click_sound.play()
                                if not do=='':
                                    try:
                                        ddd=int(do)
                                        if ddd>255:
                                            ddd=255
                                        elif ddd<0:
                                            ddd=0
                                    except ValueError:
                                        ddd=0
                                else:
                                    ddd=0
                                do=eg.enterbox(v.translations['colorCode'],default=0)
                                if do!=None:
                                    v.click_sound.play()
                                if not do=='':
                                    try:
                                        dddd=int(do)
                                        if dddd>255:
                                            dddd=255
                                        elif dddd<0:
                                            dddd=0
                                    except ValueError:
                                        dddd=0
                                else:
                                    dddd=0
                                v.dolax_screen_color=(dd,ddd,dddd)
                                v.background_photo_indicator=False

                        elif zzzz=='…':
                            lock=eg.buttonbox(v.translations['cheats'],choices=[
                                v.translations['on'],
                                v.translations['off'],
                                '…'])
                            if lock!=None:
                                v.click_sound.play()
                            if lock==v.translations['on']:     v.qwertyuiop==1
                            if lock==v.translations['off']:    v.qwertyuiop==0
                            if lock=='…':
                                lock=eg.buttonbox('Ещё игры',
                                    choices=['Пин-понг',
                                             'Лучник',
                                             '…'])
                                if lock!=None:
                                    v.click_sound.play()
                                if lock=='Пин-понг':    print('потом доделаю')
                                if lock=='Лучник':      print('потом доделаю')
                                if lock=='…':           print('потом доделаю')


                if e.type==pg.MOUSEBUTTONDOWN and e.button==4:
                    v.click_sound.play()
                    v.psihodel_indicator=True
                if e.type==pg.MOUSEBUTTONDOWN and e.button==5:
                    v.click_sound.play()
                    v.psihodel_indicator=False
        if v.psihodel_indicator:
            p1=r(0,255)
            p2=r(0,255)
            p3=r(0,255)

        pointer=pg.mouse.get_pos()

        for i in items:
            if pointer[0]>i[0] and pointer[0]<i[0]+150 and pointer[1]>i[1] and pointer[1]<i[1]+150:
                item=i[5]
        for i in items:
            if item==i[5]:
                v.screen.blit(v.font.render(i[2],1,i[4]),[i[0],i[1]-40])
            else:
                v.screen.blit(v.font.render(i[2],1,i[3]),[i[0],i[1]-40])

        v.win.blit(v.screen,[0,40])
        pg.display.flip()
    v.menu_music.stop()
    v.game_sound.play()






def gamov():
    if v.qwertyuiop==0:
        for seg in v.snake[1:]:
            if v.head_rect.colliderect(seg):
                return True
        return False




def move(head,snake):
    
    if v.KEYS[v.MenuOpen]:
        v.game_sound.stop()
        v.win.fill((0,0,0))
        load_menu()

    if v.KEYS[v.Exit]:
        fullend(False)

    if v.qwertyuiop==1:
        if v.KEYS[pg.K_SPACE]:
            game_point+=10
            snake.append(snake[-1].copy())
        if v.KEYS[pg.K_BACKSPACE]:
            game_point-=10
            if game_point<0:
                game_point=0
            if len(snake)>=2:
                snake.pop()


        if v.KEYS[pg.K_DOWN]:    v.apple_rect.y+=10
        if v.KEYS[pg.K_LEFT]:    v.apple_rect.x-=10
        if v.KEYS[pg.K_RIGHT]:   v.apple_rect.x+=10
        if v.KEYS[pg.K_UP]:      v.apple_rect.y-=10


    if v.KEYS[pg.K_RSHIFT] and v.qwertyuiop==0:
        v.qwertyuiop=1

    if v.KEYS[v.Up] and v.DIR[1]==0:        v.DIR=[0,-v.SPEED]
    elif v.KEYS[v.Down] and v.DIR[1]==0:    v.DIR=[0, v.SPEED]
    elif v.KEYS[v.Right] and v.DIR[0]==0:   v.DIR=[v.SPEED, 0]
    elif v.KEYS[v.Left] and v.DIR[0]==0:    v.DIR=[-v.SPEED,0]

    if head.right>v.size[0]:    head.left=0
    elif head.left<0:           head.right=v.size[0]
    elif head.top<0:            head.bottom=v.size[1]
    elif head.bottom>v.size[1]: head.top=0

    for ind in range(len(snake)-1,0,-1):
        snake[ind].x=snake[ind-1].x
        snake[ind].y=snake[ind-1].y

    head.move_ip(v.DIR)





def load_image(src,x,y,xr,yr):
    image=pg.image.load(src).convert()
    image=pg.transform.scale(image,(xr,yr))
    rect=image.get_rect(center=(x,y))
    trans=image.get_at((0,0))
    image.set_colorkey(trans)
    return image,rect




def load_image_with_no_file(color,x,y,xr,yr):
    image=pg.Surface((xr,yr))
    image.fill(color)
    rect=image.get_rect(center=(x,y))
    return image,rect





def pikup():
    if v.head_rect.colliderect(v.apple_rect):
        v.apple_rect.x=r(0,v.size[0]-50)
        v.apple_rect.y=r(0,v.size[1]-50)
        v.nym_sound.play()
        '''
        v.head_rect.x=r(0,v.size[0]-30)
        v.head_rect.y=r(0,v.size[1]-30)
        '''
        v.game_point+=10
        if v.timer<=100:
            v.timer=100
        v.snake.append(v.snake[-1].copy())





def score():
    textfont=pg.font.Font('fonts/minecraft.ttf',30)
    text=textfont.render(f'Рекорд: {int(v.score_max)}                      Счёт:  {int(v.game_point)}                        {v.timer//15}',True,(0,140,140))
    text_rect=text.get_rect(center=(450,80))
    v.win.blit(text,text_rect)





def timerer(tu):
    texter=pg.font.Font('fonts/minecraft.ttf',30)
    textir=texter.render(f'{tu/15}',True,(0,140,140))
    textir_rect=textir.get_rect(center=(450,80))
    v.win.blit(textir,textir_rect)
