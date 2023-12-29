from utils.constants import plants


def get_plant_info_by_name(plant_name):
    for plant in plants:
        if plant['name'] == plant_name:
            return plant


def get_plant_info_by_index(plant_index):
    return plants[plant_index]
