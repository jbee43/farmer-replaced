# Full fastest-reset automation — self-contained (no imports, starts with 0 unlocks)

ws = get_world_size()

# --- Helpers (inlined because Import is not unlocked at start) ---

def go_to(x, y):
    while get_pos_x() > x:
        move(West)
    while get_pos_x() < x:
        move(East)
    while get_pos_y() > y:
        move(South)
    while get_pos_y() < y:
        move(North)

def go_home():
    go_to(0, 0)

def advance():
    move(East)
    if get_pos_x() == 0:
        move(North)

def ensure_water():
    if num_unlocked(Unlocks.Watering) > 0:
        while get_water() < 0.75 and num_items(Items.Water) > 0:
            use_item(Items.Water)

def prepare_tile(entity, do_water):
    current = get_entity_type()
    if current != None and (current != entity or can_harvest()):
        harvest()
    soil = (entity == Entities.Cactus or entity == Entities.Carrot
            or entity == Entities.Pumpkin or entity == Entities.Sunflower
            or entity == Entities.Tree)
    ground = get_ground_type()
    if soil and ground != Grounds.Soil:
        till()
    elif not soil and ground != Grounds.Grassland:
        till()
    if get_entity_type() == None:
        plant(entity)
    if do_water and soil and num_unlocked(Unlocks.Watering) > 0:
        ensure_water()

def pad(n):
    s = str(n // 1)
    if len(s) <= 1:
        s = "0" + s
    return s

# --- Farming passes ---

def hay_pass():
    go_home()
    for _ in range(ws):
        for _ in range(ws):
            prepare_tile(Entities.Grass, False)
            advance()

def wood_pass():
    go_home()
    for _ in range(ws):
        for _ in range(ws):
            if num_unlocked(Unlocks.Trees) > 0 and (get_pos_x() + get_pos_y()) % 2 == 0:
                prepare_tile(Entities.Tree, True)
            else:
                prepare_tile(Entities.Bush, False)
            advance()

def carrot_pass():
    go_home()
    for _ in range(ws):
        for _ in range(ws):
            prepare_tile(Entities.Carrot, True)
            advance()

def pumpkin_pass():
    ready = False
    while not ready:
        ready = True
        go_home()
        for _ in range(ws):
            for _ in range(ws):
                e = get_entity_type()
                if e == Entities.Dead_Pumpkin:
                    harvest()
                    e = None
                if e == None:
                    prepare_tile(Entities.Pumpkin, True)
                    ready = False
                elif e == Entities.Pumpkin and not can_harvest():
                    ready = False
                    ensure_water()
                if num_items(Items.Fertilizer) > 0:
                    use_item(Items.Fertilizer)
                advance()
    # Harvest all — mega-pumpkin cascade gives count^3 yield
    go_home()
    for _ in range(ws):
        for _ in range(ws):
            if can_harvest():
                harvest()
            advance()

def cactus_pass():
    # Plant
    go_home()
    for _ in range(ws):
        for _ in range(ws):
            prepare_tile(Entities.Cactus, True)
            advance()
    # Wait for all mature
    ready = False
    while not ready:
        ready = True
        go_home()
        for _ in range(ws):
            for _ in range(ws):
                if get_entity_type() != Entities.Cactus:
                    prepare_tile(Entities.Cactus, True)
                    ready = False
                elif not can_harvest():
                    ready = False
                    ensure_water()
                advance()
    # Sort (shearsort: alternating row/col bubble passes)
    while True:
        s1 = False
        for row in range(ws):
            go_to(0, row)
            for _ in range(ws - 1):
                if measure() > measure(East):
                    swap(East)
                    s1 = True
                move(East)
        s2 = False
        for col in range(ws):
            go_to(col, 0)
            for _ in range(ws - 1):
                if measure() > measure(North):
                    swap(North)
                    s2 = True
                move(North)
        if not s1 and not s2:
            break
    # Cascade harvest from smallest
    go_home()
    harvest()

def dino_pass():
    clear()
    change_hat(Hats.Dinosaur_Hat)
    going_east = True
    while True:
        side = East if going_east else West
        while move(side):
            pass
        if not move(North):
            break
        going_east = not going_east
    change_hat(Hats.Straw_Hat)

def maze_pass():
    left_of = {North: West, East: North, South: East, West: South}
    right_of = {North: East, East: South, South: West, West: North}
    opposite = {North: South, East: West, South: North, West: East}
    substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
    clear()
    plant(Entities.Bush)
    use_item(Items.Weird_Substance, substance)
    d = North
    while get_entity_type() == Entities.Hedge:
        if move(right_of[d]):
            d = right_of[d]
        elif move(d):
            pass
        elif move(left_of[d]):
            d = left_of[d]
        else:
            d = opposite[d]
            move(d)
    if get_entity_type() == Entities.Treasure:
        harvest()
    clear()

# --- Resource orchestration ---

def ensure_cost(entity):
    count = ws * ws
    cost = get_cost(entity)
    for item in cost:
        needed = cost[item] * count
        if num_items(item) < needed:
            farm_to(item, needed)

def farm_to(item, amount):
    while num_items(item) < amount:
        if item == Items.Hay:
            hay_pass()
        elif item == Items.Wood:
            wood_pass()
        elif item == Items.Carrot:
            ensure_cost(Entities.Carrot)
            carrot_pass()
        elif item == Items.Pumpkin or item == Items.Weird_Substance:
            ensure_cost(Entities.Pumpkin)
            pumpkin_pass()
        elif item == Items.Cactus:
            ensure_cost(Entities.Cactus)
            cactus_pass()
        elif item == Items.Power:
            ensure_cost(Entities.Sunflower)
            # Plant
            go_home()
            for _ in range(ws):
                for _ in range(ws):
                    prepare_tile(Entities.Sunflower, True)
                    advance()
            # Wait for all to grow
            sun_ready = False
            while not sun_ready:
                sun_ready = True
                go_home()
                for _ in range(ws):
                    for _ in range(ws):
                        e = get_entity_type()
                        if e != Entities.Sunflower:
                            prepare_tile(Entities.Sunflower, True)
                            sun_ready = False
                        elif not can_harvest():
                            sun_ready = False
                            ensure_water()
                            if num_items(Items.Fertilizer) > 0:
                                use_item(Items.Fertilizer)
                        advance()
            # 5x bonus: harvest max-petal sunflower first
            if ws * ws >= 10:
                go_home()
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
                        advance()
                go_to(bx, by)
                harvest()
            # Harvest remaining
            go_home()
            for _ in range(ws):
                for _ in range(ws):
                    if can_harvest():
                        harvest()
                    advance()
        elif item == Items.Bone:
            dino_pass()
        elif item == Items.Gold:
            maze_pass()

def unlock_tech(tech):
    global ws
    cost = get_cost(tech)
    for item in cost:
        farm_to(item, cost[item])
    if not unlock(tech):
        unlock_tech(tech)
    if tech == Unlocks.Expand:
        ws = get_world_size()

# --- Main: optimal unlock order for fastest reset ---

def run():
    s = get_time()
    quick_print("Fastest Reset - Start")

    unlock_tech(Unlocks.Speed)
    unlock_tech(Unlocks.Plant)
    unlock_tech(Unlocks.Carrots)
    unlock_tech(Unlocks.Speed)
    unlock_tech(Unlocks.Watering)
    unlock_tech(Unlocks.Trees)
    unlock_tech(Unlocks.Speed)
    unlock_tech(Unlocks.Expand)
    unlock_tech(Unlocks.Expand)
    unlock_tech(Unlocks.Speed)
    unlock_tech(Unlocks.Fertilizer)
    unlock_tech(Unlocks.Pumpkins)
    unlock_tech(Unlocks.Expand)
    unlock_tech(Unlocks.Fertilizer)
    unlock_tech(Unlocks.Fertilizer)
    unlock_tech(Unlocks.Grass)
    unlock_tech(Unlocks.Trees)
    unlock_tech(Unlocks.Carrots)
    unlock_tech(Unlocks.Speed)
    unlock_tech(Unlocks.Watering)
    unlock_tech(Unlocks.Fertilizer)
    unlock_tech(Unlocks.Grass)
    unlock_tech(Unlocks.Trees)
    unlock_tech(Unlocks.Carrots)
    unlock_tech(Unlocks.Pumpkins)
    unlock_tech(Unlocks.Watering)
    unlock_tech(Unlocks.Cactus)
    unlock_tech(Unlocks.Cactus)
    unlock_tech(Unlocks.Dinosaurs)
    unlock_tech(Unlocks.Dinosaurs)
    unlock_tech(Unlocks.Mazes)
    unlock_tech(Unlocks.Leaderboard)

    elapsed = get_time() - s
    d = elapsed // 86400
    elapsed = elapsed - d * 86400
    h = elapsed // 3600
    elapsed = elapsed - h * 3600
    m = elapsed // 60
    elapsed = elapsed - m * 60
    quick_print("Done: " + pad(d) + "d " + pad(h) + "h " + pad(m) + "m " + pad(elapsed) + "s")

# Entry guard: only auto-run from a fresh leaderboard_run / simulate
if num_unlocked(Unlocks.Speed) == 0 and num_unlocked(Unlocks.Plant) == 0:
    run()
else:
    quick_print("Use via: leaderboard_run(Leaderboards.Fastest_Reset, \"quest_reset\", 256)")
