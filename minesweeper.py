from math import *
from random import *
from time import *
from kandinsky import *
from ion import *

grid_dims=(10,10) # Height, Width
nb_mines=10

colors = {
    "background": color(100,0,0),
    "case": color(200,75,75),
    "selection": color(255,0,0),
    "empty": color(150,25,25),
    "marked": color(200,0,0)
}

screen_width=320
screen_height=222

mine_dim = int(round(min((screen_width/grid_dims[0])-0.5,(screen_height/grid_dims[1])-0.5),0)) # Take the lowest possible size as the case dim

# INIT FUNCTIONS

def grids_creation(dims:tuple)->tuple:
    grid, grid_visibility = [], []
    for _ in range(dims[0]):
        grid.append([0 for _ in range(dims[1])])
        grid_visibility.append([0 for _ in range(dims[1])])
    return grid, grid_visibility

def place_mines(grid:list, nb_mines:int)->list:
  for _ in range(nb_mines):
    mine_pos = (randint(0, len(grid[0])-1), randint(0, len(grid)-1))
    while grid[mine_pos[1]][mine_pos[0]]!=0:
      mine_pos = (randint(0, len(grid[0])-1), randint(0, len(grid)-1))
    grid[mine_pos[1]][mine_pos[0]] = -1
  return grid

def calculate_proximity(grid:list)->list:
    for i in range(grid_dims[0]):
        for j in range(grid_dims[1]):
            if grid[i][j]!=-1:
                near_mines = 0
                for a in range((i-1),(i+2)):
                    for b in range((j-1),(j+2)):
                        if a>=0 and b>=0 and a<grid_dims[0] and b<grid_dims[1]:
                            if grid[a][b]==-1:
                                near_mines+=1
                grid[i][j]=near_mines
                    
    return grid


# GAMEPLAY FUNCTIONS

def update(cursor_pos:list, redraw_all:bool=False):
    if redraw_all:
        fill_rect(0,0,320,222,colors["background"])
        for i in range(grid_dims[0]):
            for j in range(grid_dims[1]):
                draw_case((j,i),False)
    draw_case(cursor_pos[1], False) #Unselects the previous case
    draw_case(cursor_pos[0], True) # Selects the new case

def draw_case(case_pos:tuple, selected:bool):
    if selected: color_to_draw = colors["selection"]
    else: color_to_draw = colors["background"]
    fill_rect(case_pos[0]*mine_dim,case_pos[1]*mine_dim,mine_dim,mine_dim,color_to_draw)
    fill_rect(case_pos[0]*mine_dim+1,case_pos[1]*mine_dim+1,mine_dim-2,mine_dim-2,colors["case"])
    if grids[1][case_pos[1]][case_pos[0]] == 1:
        case_state = grids[0][case_pos[0]][case_pos[1]]
        if case_state == 0:
            fill_rect(case_pos[0]*mine_dim+1,case_pos[1]*mine_dim+1,mine_dim-2,mine_dim-2,colors["empty"])
            empty_cases(case_pos)
        elif case_state == -1:
            fill_rect(case_pos[0]*mine_dim+1,case_pos[1]*mine_dim+1,mine_dim-2,mine_dim-2,colors["selection"])
        else:
            draw_string(str(case_state),case_pos[0]*mine_dim+1,case_pos[1]*mine_dim+1, color(255,255,255), colors["case"])
    elif grids[1][case_pos[1]][case_pos[0]] == 2:
        fill_rect(case_pos[0]*mine_dim+1,case_pos[1]*mine_dim+1,mine_dim-2,mine_dim-2,colors["marked"])

def empty_cases(pos:tuple):
    for i in range((pos[0]-1),(pos[0]+2)):
        for j in range((pos[1]-1),(pos[1]+2)):
            if i>=0 and j>=0 and i<grid_dims[0] and j<grid_dims[1] and (i,j)!=(pos[0],pos[1]):
                if grids[1][j][i]==0:
                    grids[1][j][i] = 1
                    draw_case((i,j), False)

def game_over(win:bool):
    game_phase = 2
    if win:
        fill_rect(0,0,320,222,colors["background"])
        draw_string("YOU WIN!", int(round(screen_width/2-45,0)), int(round(screen_height/2-10,0)), color(255,255,255), colors["background"])
    else:
        draw_string("YOU LOSE!", int(round(screen_width/2-50,0)), int(round(screen_height/2-10,0)), color(255,255,255), colors["background"])


# INIT PHASE

game_phase = 0

#Grid creation
grids = grids_creation(grid_dims)
grids = (calculate_proximity(place_mines(grids[0], nb_mines)), grids[1])

nb_markers = 0
cursor_pos = [(0,0) , (0,0)] # (current, previous)

update(cursor_pos, True)

game_phase = 1

#GAMEPLAY
while game_phase == 1:
    need_update = False
    if keydown(KEY_OK):
        if grids[1][cursor_pos[0][1]][cursor_pos[0][0]] == 0:
            grids[1][cursor_pos[0][1]][cursor_pos[0][0]], need_update = 1, True
            if grids[0][cursor_pos[0][0]][cursor_pos[0][1]] == -1 :
                update(cursor_pos)
                sleep(0.5)
                game_over(False)
                break
    elif keydown(KEY_BACKSPACE):
        if grids[0][cursor_pos[0][0]][cursor_pos[0][1]] == -1 and grids[1][cursor_pos[0][1]][cursor_pos[0][0]] == 0:
            grids[1][cursor_pos[0][1]][cursor_pos[0][0]], need_update = 2, True
            nb_markers+=1
            if nb_markers>=nb_mines:
                update(cursor_pos)
                sleep(0.5)
                game_over(True)
                break
        elif grids[1][cursor_pos[0][1]][cursor_pos[0][0]] == 0:
            update(cursor_pos)
            sleep(0.5)
            game_over(False)
            break
        else:
            pass # Case is already visible
    elif keydown(KEY_RIGHT) and cursor_pos[0][0]<grid_dims[1]-1: cursor_pos[0], need_update = (cursor_pos[0][0]+1,cursor_pos[0][1]), True
    elif keydown(KEY_LEFT) and cursor_pos[0][0]>0: cursor_pos[0], need_update = (cursor_pos[0][0]-1,cursor_pos[0][1]), True
    elif keydown(KEY_UP) and cursor_pos[0][1]>0: cursor_pos[0], need_update = (cursor_pos[0][0],cursor_pos[0][1]-1), True
    elif keydown(KEY_DOWN) and cursor_pos[0][1]<grid_dims[0]-1: cursor_pos[0], need_update = (cursor_pos[0][0],cursor_pos[0][1]+1), True

    if need_update:
        update(cursor_pos)
        cursor_pos[1] = cursor_pos[0]
  
    sleep(0.12)
