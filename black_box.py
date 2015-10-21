"""
Kai Cheng
CIT 590 Assignment 5
black_box.py
"""

import random

BOARD_SIZE = 8

bomb_list = []
mark_list = []
point_map = {}
flag = ord('a')

def new_game(location1, location2, location3, location4):
    """
    Sets up a new game board with "atoms" in the four locations specified, 
    where each location is a (row, column) tuple. Row and column numbers are 0 to 7. 
    Clears any leftover data from any previous game. 
    Returns None.
    """
    global bomb_list
    global mark_list
    global point_map
    global flag
    bomb_list = [location1, location2, location3, location4]
    mark_list = []
    point_map = {}
    flag = ord('a')

def shoot(entry):
    """
    Shoots a ray into the game, where entry is a string using the same syntax that a user would type in ('1L', etc.). 
    Returns the exit point of the ray in the same syntax, or None in the case of a hit.
    """
    x = 0
    y = 0
    inc_x = 0
    inc_y = 0
    if entry[1] == 'l':
        inc_x = 1
        x = 0
        y = int(entry[0]) - 1
    elif entry[1] == 't':
        inc_y = 1
        x = int(entry[0]) - 1
        y = 0
    elif entry[1] == 'r':
        inc_x = -1
        x = BOARD_SIZE - 1
        y = int(entry[0]) - 1
    elif entry[1] == 'b':
        inc_y = -1
        x = int(entry[0]) - 1
        y = BOARD_SIZE - 1
    next_x = x + inc_x
    next_y = y + inc_y
    while next_x >= 0 and next_x < BOARD_SIZE and next_y >= 0 and next_y < BOARD_SIZE:
        if (next_y, next_x) in bomb_list:
            return None
        if inc_x == 0:
            if (next_y, next_x-1) in bomb_list:
                inc_x = 1
                inc_y = 0
            elif (next_y, next_x+1) in bomb_list:
                inc_x = -1
                inc_y = 0
            else:
                x = next_x
                y = next_y
        elif inc_y == 0:
            if (next_y - 1, next_x) in bomb_list:
                inc_x = 0
                inc_y = 1
            elif (next_y + 1, next_x) in bomb_list:
                inc_x = 0
                inc_y = -1
            else:
                x = next_x
                y = next_y
        next_x = x + inc_x
        next_y = y + inc_y
    
    if inc_x == 0 and inc_y == 1:
        return str(x + 1) + "b"
    elif inc_x == 0 and inc_y == -1:
        return str(x + 1) + "t"
    elif inc_x == 1 and inc_y == 0:
        return str(y + 1) + "r"
    elif inc_x == -1 and inc_y == 0:
        return str(y + 1) + "l"
        

def toggle(row, column):
    """
    Marks or unmarks the specified location in the game. 
    Row and column numbers are 0 to 7. 
    Returns None.
    """
    global mark_list
    if (row, column) in mark_list:
        mark_list.remove((row, column))
    else:
        mark_list.append((row, column))

def score():
    """Returns (as an integer) the current score. Does not end the game."""
    result = len(point_map.keys())
    for bomb in bomb_list:
        if bomb not in mark_list:
            result += 10
    for bomb in mark_list:
        if bomb not in bomb_list:
            result += 10
    return result

def print_board():
    print("     1 2 3 4 5 6 7 8")   
    print("    ", end = "")
    for i in range(BOARD_SIZE):
        if point_map.get(str(i + 1) + "t"):
            print(" " + point_map[str(i + 1) + "t"], end = "")
        else:
            print("  ", end = "")
    print()
    print("    -----------------")
    for i in range(BOARD_SIZE):
        print(str(i + 1) + " ", end = "")
        if point_map.get(str(i + 1) + "l"):
            print(point_map[str(i + 1) + "l"], end = "")
        else:
            print(" ", end = "")
        print("|", end = "")
        for j in range(BOARD_SIZE):
            if (i, j) in mark_list:
                print(" *", end = "")
            else:
                print(" -", end = "")
        print(" |", end = "")
        if point_map.get(str(i + 1) + "r"):
            print(point_map[str(i + 1) + "r"], end = "")
        else:
            print(" ", end = "")
        print(" " + str(i + 1))
    print("    -----------------")
    print("    ", end = "")
    for i in range(BOARD_SIZE):
        if point_map.get(str(i + 1) + "b"):
            print(" " + point_map[str(i + 1) + "b"], end = "")
        else:
            print("  ", end = "")
    print()
    print("     1 2 3 4 5 6 7 8")  

def play():
    answer = ""
    print_board()
    while answer != "f":
        answer = input("input command (f: finish): ").strip().lower()
        if len(answer) == 2:
            if answer[0].isdigit() and answer[1].isdigit():
                toggle(int(answer[0]) - 1,int(answer[1]) - 1)
            elif answer[0].isdigit() and answer[1] in ("l", "t", "r", "b"):
                entry_point = answer
                exit_point = shoot(entry_point)
                if exit_point:
                    global flag
                    point_map[entry_point] = chr(flag)
                    point_map[exit_point] = chr(flag)
                    flag = flag + 1
                else:
                    point_map[entry_point] = "H"  
        if len(answer) == 3:
            if answer[0].isdigit() and answer[2].isdigit():
                toggle(int(answer[0]) - 1, int(answer[2]) - 1)
        print_board()
    print("your score: " + str(score()))

def main():
    answer = "y"
    while answer == "y":
        l = []
        while len(l) != 4:
            t = (random.randint(0,BOARD_SIZE-1), random.randint(0,BOARD_SIZE - 1))
            if t not in l:
                l.append(t)
        new_game(l[0], l[1], l[2], l[3])
        play()
        answer = input("play again? [y|n]: ").lower()
    
if __name__=="__main__":
    main()
