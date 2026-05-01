# Crop mandala — concentric rings of different crops from center
import nav
import sow

def once():
    ws = get_world_size()
    crops = [Entities.Sunflower, Entities.Carrot, Entities.Pumpkin,
             Entities.Bush, Entities.Grass]
    center = ws // 2
    set_execution_speed(1)
    nav.home()
    for y in range(ws):
        for x in range(ws):
            nav.to(x, y)
            ring = max(abs(x - center), abs(y - center))
            crop = crops[ring % len(crops)]
            sow.tile(crop, False)
    set_execution_speed(0)

def loop():
    while True:
        once()
