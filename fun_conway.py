# Conway's Game of Life — grass is alive, empty is dead
import nav

def step():
    ws = get_world_size()
    # Read current state into flat list
    state = []
    nav.home()
    for _ in range(ws * ws):
        if get_entity_type() != None:
            state = state + [1]
        else:
            state = state + [0]
        nav.advance()
    # Compute next generation in-memory
    nxt = []
    for y in range(ws):
        for x in range(ws):
            alive = state[y * ws + x]
            neighbors = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx != 0 or dy != 0:
                        ni = ((y + dy + ws) % ws) * ws + ((x + dx + ws) % ws)
                        neighbors = neighbors + state[ni]
            if alive == 1 and (neighbors == 2 or neighbors == 3):
                nxt = nxt + [1]
            elif alive == 0 and neighbors == 3:
                nxt = nxt + [1]
            else:
                nxt = nxt + [0]
    # Apply changes
    nav.home()
    for i in range(ws * ws):
        e = get_entity_type()
        if nxt[i] == 1 and e == None:
            if get_ground_type() != Grounds.Grassland:
                till()
            plant(Entities.Grass)
        elif nxt[i] == 0 and e != None:
            harvest()
        nav.advance()

def seed():
    ws = get_world_size()
    clear()
    nav.home()
    for _ in range(ws * ws):
        if random() > 0.5:
            plant(Entities.Grass)
        nav.advance()

def once(generations = 50):
    set_execution_speed(2)
    seed()
    for _ in range(generations):
        step()
    set_execution_speed(0)

def loop():
    while True:
        once()
