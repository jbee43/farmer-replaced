# Movement helpers
# Named 'nav' to avoid shadowing the builtin move() function.

def to(x, y):
    while get_pos_x() > x:
        move(West)
    while get_pos_x() < x:
        move(East)
    while get_pos_y() > y:
        move(South)
    while get_pos_y() < y:
        move(North)

def home():
    to(0, 0)

def advance():
    move(East)
    if get_pos_x() == 0:
        move(North)
