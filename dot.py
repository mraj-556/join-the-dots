import pygame as pg
from pygame import mixer
from tkinter import messagebox as msgbox
import numpy as np
import os
import time
from threading import Thread

pg.init()

                        #######################  variables  #######################

global dot_obj_list , selected , draw_line, done , dx, dy , player_dict
dot_obj_list = []    # storing button objects (objects)
selected = []    # increasing / decreasing  connected to nearby btns value of respective object
                        # (init : 0 ,  min : 0 , max : 4 or 3 or 2)
connected_nodes = []   # storing the connected nodes
draw_line = []   # for line draw between two points stores two dot obj
gameover = False     # for game looping
dx, dy = 10, 10  # initialising distance between two consecutove points
player_dict = {} # stores player obj for turn decission like { p_i : obj }
blue , pink , red , yellow , violet , brown =  (68, 14, 204) , (224, 9, 131) , (232, 9, 13) , (240, 220, 7) , (191, 9, 227) , (235, 92, 9)
clrs = [blue , pink , red , yellow , violet , brown]

                        #######################  player class  #######################

class player:
    def __init__(self,player_name,player_clr,player_turn):
        self.player_name = player_name
        self.player_clr = player_clr
        self.player_turn = player_turn
    def set_turn(self,v):
        self.player_turn = v


                        #######################  player object create  #######################

def create_player():
    plyr = []
    for i in range(num_of_players):
        # print(plyr)
        r = True
        while r:
            p = f'p_{i}'
            p_name = input(f'Enter name of player_{i} : ')
            p_clr = clrs[i]
            if p_name not in plyr:
                plyr.append(p_name)
                player_dict[p] = player(p_name,p_clr,0)
                r = False
            else:
                print('player already exists...')
                time.sleep(3)
        print()
        print("************  -------  ************")
        print()

    os.system('clear')

                        #######################  players turn decission  #######################

k ,v = list(player_dict.keys()) , list(player_dict.values())

def player_turn():
    while not gameover:
        for i,j in zip(k,v):
            print('turn for :',i)


                        #######################  map create  #######################

def create_map():
    global dot_obj_list , selected , draw_line , dx, dy
    init_x , init_y = 50, 50
    for i in range(grid_x):
        init_x = 50
        for j in range(grid_y):
            obj = pg.draw.circle(screen, (0, 255, 0), (init_x,init_y), 5)
            selected.append(0)
            dot_obj_list.append(obj)
            init_x+=50
        init_y+=50

                        #######################  home build logic  #######################

def draw_home(lu,ld,ru,rd):
    print('home : ',lu,ld,ru,rd)
    home = pg.image.load('img/home.png')
    home = pg.transform.scale(home,(45,45))
    x = [ dot_obj_list[lu].center[0] , dot_obj_list[ld].center[0] , dot_obj_list[ru].center[0] , dot_obj_list[rd].center[0] ]
    y = [ dot_obj_list[lu].center[1] , dot_obj_list[ld].center[1] , dot_obj_list[ru].center[1] , dot_obj_list[rd].center[1] ]
    x , y = min(x) , min(y)
    home_sound()
    screen.blit(home, (x+3,y+3))

def check_box(direction,dots):
    # print(direction,dots)
    if direction=='h':
        top_1 = [dots[0] , dots[0]-grid_y ] # for 1st dot  top
        top_2 = [dots[1] , dots[1]-grid_y ] # for 2nd dot  top
        down_1 = [dots[0] , dots[0]+grid_y ] # for 1st dot  down
        down_2 = [dots[1] , dots[1]+grid_y ] # for 2nd dot  down
        print()
        print('connected list : ',connected_nodes)
        print('top_1 : ',top_1 , 'top_2 : ',top_2)
        print()
        if ( top_1 in connected_nodes or top_1[::-1] in connected_nodes) and ( top_2 in connected_nodes or top_2[::-1] in connected_nodes) and ( [ top_1[1],top_2[1] ] in connected_nodes or [ top_2[1],top_1[1] ] in  connected_nodes):
            draw_home(top_1[1] , top_1[0] , top_2[1] , top_2[0] )
        if ( down_1 in connected_nodes or down_1[::-1] in connected_nodes ) and ( down_2 in connected_nodes or down_2[::-1] in connected_nodes ) and ( [ down_1[1],down_2[1] ] in connected_nodes or [ down_2[1],down_1[1] ] in connected_nodes):
            draw_home(down_1[0] , down_1[1] , down_2[0] , down_2[1] )
    if direction=='v':
        left_1 = [dots[0] , dots[0]-1 ] # for top dot  left
        left_2 = [dots[1] , dots[1]-1 ] # for bottom dot  left
        right_1 = [dots[0] , dots[0]+1 ] # for top dot  right
        right_2 = [dots[1] , dots[1]+1 ] # for bottom dot  right
        print()
        print(connected_nodes)
        print()
        print('left_1 : ',left_1 , 'left_2 : ',left_2)
        if ( left_1 in connected_nodes or left_1[::-1] in connected_nodes) and ( left_2 in connected_nodes or left_2[::-1] in connected_nodes) and ( [ left_1[1],left_2[1] ] in connected_nodes or [ left_2[1],left_1[1] ] in connected_nodes):
            draw_home(left_1[1] , left_2[1] , left_1[0] , left_2[0] )
        if ( right_1 in connected_nodes or right_1[::-1] in connected_nodes ) and ( right_2 in connected_nodes or right_2[::-1] in connected_nodes ) and ( [ right_1[1],right_2[1] ] in connected_nodes or [ right_2[1],right_1[1] ] in connected_nodes):
            draw_home(right_1[0] , right_1[1] , right_2[0] , right_2[1] )

def home():
    global draw_line , connected_nodes
    dots = [dot_obj_list.index(draw_line[0]) , dot_obj_list.index(draw_line[1])]
    dot_1 , dot_2 = dots[0] , dots[1]
    print('~~~~~~~~checking~~~~~~~~',dot_1,dot_2)

    direction = dot_1-dot_2
    if direction==1:
        # print('left')
        check_box('h',dots)
    elif direction==-1:
        # print('right')
        check_box('h',dots)
    elif direction==grid_y:
        # print('top')
        check_box('v',dots)
    elif direction==-grid_y:
        # print('down')
        check_box('v',dots)


                        #######################  game logic  #######################

def start():
    global dot_obj_list , selected , draw_line, done , dx, dy , gameover
    corner = [0 , grid_y-1 , (grid_x*grid_y)-(grid_y-1) , (grid_x*grid_y)-1]
    while not gameover:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                for id , btn_obj in enumerate(dot_obj_list): # if mouse clicked then loop all dot obj
                    if btn_obj.collidepoint(event.pos):  # if dot is clicked
                        click()
                        # max connection of a node decission
                        limit = 4

                        #   left vertical           right vertical                  up horizontal                                down horizontal
                        if (id%grid_y==0)  or ( (id-(grid_y-1)) % grid_y==0 ) or (id>=0 and id<grid_y) or ( id>=(grid_x*grid_y)-(grid_y-1) and id<(grid_x*grid_y) ) :
                            print('edge')
                            limit = 3
                        if id in corner:
                            limit=2

                        if selected[id]<limit:

                            # if nothing is selected and max connection condition obeys
                            if ( selected[id]>=0 and selected[id]<limit ) and ( len(draw_line)==0 ) :
                                print('1st dot : ',dot_obj_list.index(btn_obj))
                                if selected[id]==0:
                                    dot_obj_list[id] = pg.draw.circle(screen, (255, 0, 0), btn_obj.center, 5)
                                draw_line.append(dot_obj_list[id])
                                selected[id]+=1
                                # print(f'selected0 : id {id}  with connections {selected[id]}')
                            
                            elif ( selected[id]>=0 and selected[id]<limit ) and ( len(draw_line)==1 ) :
                                dx, dy = abs(draw_line[0].center[0] - btn_obj.center[0]), abs(draw_line[0].center[1] - btn_obj.center[1])
                                if (dx<=50 and dy==0) or (dx==0 and dy<=50) :
                                    # print('2nd dot : ',dot_obj_list.index(btn_obj))
                                    connecting = [dot_obj_list.index(draw_line[0]) , dot_obj_list.index(btn_obj)]
                                    # print(btn_obj.center , draw_line[0].center)
                                    if (connecting not in connected_nodes and connecting[::-1] not in connected_nodes):
                                        print('len : ',len(draw_line),btn_obj.center == draw_line[0].center)
                                        if ( btn_obj.center != draw_line[0].center ) and (dx==50 and dy==0) or (dx==0 and dy==50) :
                                            if selected[id]==0:
                                                dot_obj_list[id] = pg.draw.circle(screen, (255, 0, 0), btn_obj.center, 5)
                                            draw_line.append(dot_obj_list[id])
                                            selected[id]+=1
                                            # print(f'selected1 : id {id}  with connections {selected[id]}')
                                            pg.draw.line(screen, (0, 255, 255),draw_line[0].center, draw_line[1].center, 3)
                                            line_sound()
                                            connected_nodes.append( [ dot_obj_list.index(draw_line[0]) , dot_obj_list.index(draw_line[1]) ])

                                            # checking home
                                            home()

                                        elif ( btn_obj.center == draw_line[0].center ) :
                                            if selected[id]<4:
                                                dot_obj_list[id] = pg.draw.circle(screen, (0, 255, 0), btn_obj.center, 5)
                                            selected[id]-=1
                                            # print('deselected',id,selected[id])
                                        draw_line = []
                                    else:
                                        warn_sound()
                                        print('Dots are already connected')
                                        connecting = []
                                else:
                                    warn_sound()
                                    print('Invalid connection')
                        
                        elif selected[id]==limit and ( len(draw_line)==1 ) and ( btn_obj.center == draw_line[0].center ):
                            dot_obj_list[id] = pg.draw.circle(screen, (0, 255, 0), btn_obj.center, 5)
                            selected[id]-=1
                            print('deselected:',id,selected[id])
                            draw_line = []

                        else:
                            warn_sound()
                            print('Fully connected dot')
                            break
                            
            if event.type == pg.QUIT:
                gameover = True
        pg.display.flip()

                    #######################  input and screen create  #######################

def screen_create():
    screen = pg.display.set_mode((x, y))
    screen.set_alpha(None)
    bg = pg.image.load('img/bg.png')
    screen.blit(bg, (0, 0))
    pg.display.set_caption('.-.-.Bindu Bindu.-.-.')
    return screen


grid_x , grid_y = 20,20
while True:
    # grid_x, grid_y = list(map(int,input("Screen size : ").split()))
    grid_x, grid_y = 12 , 12
    # p_max = max(grid_x,grid_y)//3
    p_max = 4
    num_of_players = 4
    # num_of_players = int(input(f'Enter number of players below {p_max} : '))

    if (grid_x<=12 and grid_y<=12) and num_of_players<=p_max:
        x , y = (grid_x*50)+50 , (grid_y*50)+50
        break
    elif num_of_players > p_max:
        print('Player number exceeding limit')
    else:
        print('enter size below 15 X 15')


                    #######################  music setting  #######################

pg.mixer.init()

def click():
    click_sound = pg.mixer.Sound('sounds/btnclick.wav')
    pg.mixer.Sound.set_volume(click_sound,0.2)
    pg.mixer.Sound.play(click_sound)

def bgm():
    pg.mixer.music.load('sounds/bgm.mp3')
    pg.mixer.music.set_volume(0.2)
    pg.mixer.music.play(-1)

def home_sound():
    click_sound = pg.mixer.Sound('sounds/home_created.wav')
    pg.mixer.Sound.set_volume(click_sound,0.2)
    pg.mixer.Sound.play(click_sound)

def line_sound():
    click_sound = pg.mixer.Sound('sounds/draw_line.wav')
    pg.mixer.Sound.set_volume(click_sound,0.2)
    pg.mixer.Sound.play(click_sound)

def warn_sound():
    click_sound = pg.mixer.Sound('sounds/click_error.wav')
    pg.mixer.Sound.set_volume(click_sound,0.2)
    pg.mixer.Sound.play(click_sound)

                    #######################  function calling  #######################

create_player()
bgm()
screen = screen_create()
create_map()
start()

pg.quit()
exit()
