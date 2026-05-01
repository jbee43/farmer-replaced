# Pumpkin mega-farming — waits for all to grow, uses fertilizer, clears dead
import nav
import sow
import water

def once():
    ws = get_world_size()
    ready = False
    while not ready:
        ready = True
        nav.home()
        for _ in range(ws):
            for _ in range(ws):
                e = get_entity_type()
                if e == Entities.Dead_Pumpkin:
                    harvest()
                    e = None
                if e == None:
                    sow.tile(Entities.Pumpkin)
                    ready = False
                elif e == Entities.Pumpkin and not can_harvest():
                    ready = False
                    water.ensure()
                if num_items(Items.Fertilizer) > 0:
                    use_item(Items.Fertilizer)
                nav.advance()
    # Harvest all — mega-pumpkin cascade gives count^3 yield
    nav.home()
    for _ in range(ws):
        for _ in range(ws):
            if can_harvest():
                harvest()
            nav.advance()

def loop():
    while True:
        once()
