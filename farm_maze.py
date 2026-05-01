# Maze gold farming — right-hand wall follower

def solve():
    left_of = {North: West, East: North, South: East, West: South}
    right_of = {North: East, East: South, South: West, West: North}
    opposite = {North: South, East: West, South: North, West: East}
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

def once():
    ws = get_world_size()
    cost = ws * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
    if num_items(Items.Weird_Substance) < cost:
        return False
    clear()
    plant(Entities.Bush)
    use_item(Items.Weird_Substance, cost)
    solve()
    return True

def loop():
    while True:
        if not once():
            break
