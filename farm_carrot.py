# Carrot farming — soil + water
import nav
import sow

def once():
    ws = get_world_size()
    nav.home()
    for _ in range(ws):
        for _ in range(ws):
            sow.tile(Entities.Carrot)
            nav.advance()

def loop():
    while True:
        once()
