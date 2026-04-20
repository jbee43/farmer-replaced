# Tile preparation: ground type, plant, water
import water

def needs_soil(entity):
    return (entity == Entities.Cactus or entity == Entities.Carrot
            or entity == Entities.Pumpkin or entity == Entities.Sunflower
            or entity == Entities.Tree)

def tile(entity, do_water = True):
    current = get_entity_type()
    if current != None and (current != entity or can_harvest()):
        harvest()
    soil = needs_soil(entity)
    ground = get_ground_type()
    if soil and ground != Grounds.Soil:
        till()
    elif not soil and ground != Grounds.Grassland:
        till()
    if get_entity_type() == None:
        plant(entity)
    if do_water and soil and num_unlocked(Unlocks.Watering) > 0:
        water.ensure()
