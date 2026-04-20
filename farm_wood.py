# Wood farming — tree/bush checkerboard to avoid tree adjacency slowdown
import nav
import sow

def once():
    ws = get_world_size()
    nav.home()
    has_trees = num_unlocked(Unlocks.Trees) > 0
    for _ in range(ws):
        for _ in range(ws):
            if has_trees and (get_pos_x() + get_pos_y()) % 2 == 0:
                sow.tile(Entities.Tree)
            else:
                sow.tile(Entities.Bush, False)
            nav.advance()

def loop():
    while True:
        once()
