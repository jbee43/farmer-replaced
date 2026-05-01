# Companion planting — fulfill plant preferences for yield bonus
import nav
import sow
import water

def once():
    ws = get_world_size()
    # Plant carrots (high-value companion target)
    nav.home()
    for _ in range(ws):
        for _ in range(ws):
            sow.tile(Entities.Carrot)
            nav.advance()
    # Wait for all to grow
    ready = False
    while not ready:
        ready = True
        nav.home()
        for _ in range(ws):
            for _ in range(ws):
                if get_entity_type() != Entities.Carrot:
                    sow.tile(Entities.Carrot)
                    ready = False
                elif not can_harvest():
                    ready = False
                    water.ensure()
                    if num_items(Items.Fertilizer) > 0:
                        use_item(Items.Fertilizer)
                nav.advance()
    # Collect companion preferences
    companions = []
    nav.home()
    for _ in range(ws):
        for _ in range(ws):
            comp = get_companion()
            if comp != None:
                c_type = comp[0]
                c_pos = comp[1]
                companions = companions + [[c_type, c_pos[0], c_pos[1]]]
            nav.advance()
    # Fulfill each companion request
    for c in companions:
        nav.to(c[1], c[2])
        e = get_entity_type()
        if e != None:
            harvest()
        if sow.needs_soil(c[0]) and get_ground_type() != Grounds.Soil:
            till()
        elif not sow.needs_soil(c[0]) and get_ground_type() != Grounds.Grassland:
            till()
        plant(c[0])
        water.ensure()
    # Wait for companions to mature
    for c in companions:
        nav.to(c[1], c[2])
        while get_entity_type() == None or not can_harvest():
            water.ensure()
            if num_items(Items.Fertilizer) > 0:
                use_item(Items.Fertilizer)
    # Harvest all
    nav.home()
    for _ in range(ws):
        for _ in range(ws):
            if can_harvest():
                harvest()
            nav.advance()

def loop():
    while True:
        once()
