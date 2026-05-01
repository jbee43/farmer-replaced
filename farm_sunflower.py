# Sunflower farming — harvest max-petal sunflower first for 5x power bonus
import nav
import sow
import water

def once():
    ws = get_world_size()
    total = ws * ws
    # Plant full field
    nav.home()
    for _ in range(ws):
        for _ in range(ws):
            sow.tile(Entities.Sunflower)
            nav.advance()
    # Wait for all to grow
    ready = False
    while not ready:
        ready = True
        nav.home()
        for _ in range(ws):
            for _ in range(ws):
                e = get_entity_type()
                if e != Entities.Sunflower:
                    sow.tile(Entities.Sunflower)
                    ready = False
                elif not can_harvest():
                    ready = False
                    water.ensure()
                    if num_items(Items.Fertilizer) > 0:
                        use_item(Items.Fertilizer)
                nav.advance()
    # 5x bonus: harvest max-petal sunflower first (requires >= 10 sunflowers)
    if total >= 10:
        nav.home()
        best = -1
        bx = 0
        by = 0
        for _ in range(ws):
            for _ in range(ws):
                p = measure()
                if p != None and p > best:
                    best = p
                    bx = get_pos_x()
                    by = get_pos_y()
                nav.advance()
        nav.to(bx, by)
        harvest()
    # Harvest remaining
    nav.home()
    for _ in range(ws):
        for _ in range(ws):
            if can_harvest():
                harvest()
            nav.advance()

def loop():
    while True:
        once()
