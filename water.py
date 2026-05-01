# Watering helper

def ensure(threshold = 0.75):
    while get_water() < threshold and num_items(Items.Water) > 0:
        use_item(Items.Water)
