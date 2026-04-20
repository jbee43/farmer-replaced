# Dinosaur bone farming — fill field with tail segments via serpentine traversal

def once():
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

def loop():
    while True:
        once()
