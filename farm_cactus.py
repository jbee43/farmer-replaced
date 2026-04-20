# Cactus farming — shearsort + cascade harvest (yield = count^2)
import nav
import sow
import water

def once():
    ws = get_world_size()
    # Plant
    nav.home()
    for _ in range(ws):
        for _ in range(ws):
            sow.tile(Entities.Cactus)
            nav.advance()
    # Wait for all to mature, water while waiting
    ready = False
    while not ready:
        ready = True
        nav.home()
        for _ in range(ws):
            for _ in range(ws):
                if get_entity_type() != Entities.Cactus:
                    sow.tile(Entities.Cactus)
                    ready = False
                elif not can_harvest():
                    ready = False
                    water.ensure()
                nav.advance()
    # Sort then cascade-harvest from (0,0)
    sort_field()
    nav.home()
    harvest()

def sort_field():
    while True:
        s1 = sort_rows()
        s2 = sort_cols()
        if not s1 and not s2:
            break

def sort_rows():
    ws = get_world_size()
    swapped = False
    for row in range(ws):
        nav.to(0, row)
        for _ in range(ws - 1):
            if measure() > measure(East):
                swap(East)
                swapped = True
            move(East)
    return swapped

def sort_cols():
    ws = get_world_size()
    swapped = False
    for col in range(ws):
        nav.to(col, 0)
        for _ in range(ws - 1):
            if measure() > measure(North):
                swap(North)
                swapped = True
            move(North)
    return swapped

def loop():
    while True:
        once()
