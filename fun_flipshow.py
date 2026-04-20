# Drone acrobatics — traces shapes with flips and hat changes
import nav

def border():
    ws = get_world_size()
    nav.to(0, 0)
    do_a_flip()
    for _ in range(ws - 1):
        move(East)
    do_a_flip()
    for _ in range(ws - 1):
        move(North)
    do_a_flip()
    for _ in range(ws - 1):
        move(West)
    do_a_flip()
    for _ in range(ws - 1):
        move(South)
    do_a_flip()

def diamond():
    ws = get_world_size()
    mid = ws // 2
    nav.to(mid, 0)
    do_a_flip()
    for _ in range(mid):
        move(East)
        move(North)
    do_a_flip()
    for _ in range(mid):
        move(West)
        move(North)
    do_a_flip()
    for _ in range(mid):
        move(West)
        move(South)
    do_a_flip()
    for _ in range(mid):
        move(East)
        move(South)
    do_a_flip()

def zigzag():
    ws = get_world_size()
    nav.to(0, 0)
    for row in range(ws):
        side = East if row % 2 == 0 else West
        for _ in range(ws - 1):
            move(side)
        if row < ws - 1:
            move(North)
        if row % 3 == 0:
            do_a_flip()

def once():
    set_execution_speed(1)
    clear()
    # Act 1: Border trace
    change_hat(Hats.Wizard_Hat)
    border()
    # Act 2: Diamond
    change_hat(Hats.Gold_Hat)
    diamond()
    # Act 3: Zigzag
    change_hat(Hats.Top_Hat)
    zigzag()
    # Finale
    nav.to(get_world_size() // 2, get_world_size() // 2)
    change_hat(Hats.Straw_Hat)
    do_a_flip()
    set_execution_speed(0)

def loop():
    while True:
        once()
