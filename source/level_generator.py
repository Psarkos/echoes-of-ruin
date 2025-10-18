# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
import pygame as pg
import random as rd

from template import get_random_list_of_templates
from usefull_fonctions import image_loader, csv_to_list
from item import DropedItem, EquipableItem, ConsumableItem, StatusEffect
from map_generator import map_generator
from enemy import Enemy
from entity import Entity
from spawn import get_all_spawn_pos, get_random_spawn_pos
from exit import Exit

dic_img = {}


def generate_items(dropped_item_group, all_spawn_cell_pos):
    nb_item = rd.randint(10, 15)
    PATH = "assets/images/items/"
    item_list = []
    # Ajout des équipements à la liste d'items depuis le fichier csv et
    # création des stats des equipements sous forme de dictionnaire
    item_list.append(csv_to_list("data/items/equipements.csv"))
    str_transform(item_list[0], 4, True)
    
    # Ajout des consommables à la liste d'items depuis le fichier csv 
    # et création d'une liste des effets du consommable
    # et d'un dico des stats des effets
    item_list.append(csv_to_list("data/items/consumables.csv"))
    str_transform(item_list[1], 5)
    str_transform(item_list[1], 6, True)
    
    for _ in range(nb_item):
        item_type = rd.randint(0, 1)

        item_choice = rd.choice(item_list[item_type])
        
        item_img_path = PATH + item_choice[1]
        if item_img_path not in dic_img.keys():
            dic_img[item_img_path] = image_loader(item_img_path)
        match item_type:
            case 0:
                dropped_item_group.add(
                    DropedItem(
                        EquipableItem(
                            item_choice[0],
                            dic_img[item_img_path],
                            item_choice[2],
                            int(item_choice[3]),
                            item_choice[4]
                        ),
                        get_random_spawn_pos(all_spawn_cell_pos),
                    )
                )
            case 1:
                dropped_item_group.add(
                    DropedItem(
                        ConsumableItem(
                            item_choice[0],
                            dic_img[item_img_path],
                            int(item_choice[2]),
                            int(item_choice[3]),
                            int(item_choice[4]),
                            [
                                StatusEffect(effect[0], int(effect[1]), int(effect[2]), {effect[3]:int(item_choice[6][effect[3]])})
                                for effect in item_choice[5]
                            ],
                        ),
                        get_random_spawn_pos(all_spawn_cell_pos),
                    )
                )


def str_transform(item_list, stats_position, is_to_dict=False):
    """ Change les stats des items de str à dict afin de les utilisers dans la 

    Args:
        item_list (list): liste des items dont il faut changer les stats en dictionnaire
        stats_position (int): position des stats dans la liste que constitu chaque item
        is_to_dict (bool, optional): True si on veut transformer le résultat en dictionnaire. Defaults to False
    """
    # Parcours la liste des items
    for item in item_list:
        item[stats_position] = item[stats_position].split("/")
        
        # Parcours les stats de l'item
        for i in range(len(item[stats_position])):
            item[stats_position][i] = item[stats_position][i].split(".")
            item[stats_position][i][1] = int(item[stats_position][i][1])

        # Pour transformer les stats en dictionnaire
        if is_to_dict:
            item[stats_position] = dict(item[stats_position])
            

def generate_map(tile_group):
# Listes des templates

    templates_list = get_random_list_of_templates(rd.randint(5,11))

    # === GENERE LA MAP ET LES COULOIRS ===
    map = map_generator(templates_list, tile_group)  # Map principale
    all_spawn_pos = get_all_spawn_pos(map)

    Entity.MAP = map

    return all_spawn_pos



def generate_enemy(enemy_group, all_spawn_cell_pos, mob_cell_pos):
    nb_enemy = rd.randint(4,15)
    PATH = "assets/images/entity/"
    enemys_list = csv_to_list("data/enemys/enemys.csv")
    
    for _ in range(nb_enemy):
        enemy_info = rd.choice(enemys_list)
        
        enemy_img_path = PATH + enemy_info[0]
        if enemy_img_path not in dic_img.keys():
            dic_img[enemy_img_path] = image_loader(enemy_img_path)
            
        enemy = Enemy(
            dic_img[enemy_img_path], 
            get_random_spawn_pos(all_spawn_cell_pos), 
            (32, 32), 
            int(enemy_info[1]), 
            int(enemy_info[2]), 
            int(enemy_info[3]), 
            int(enemy_info[4]), 
            int(enemy_info[5]), 
            int(enemy_info[6]), 
            int(enemy_info[7]), 
            int(enemy_info[8]), 
            int(enemy_info[9]), 
            int(enemy_info[10]), 
            int(enemy_info[11])
        )
        enemy_group.add(enemy)
        mob_cell_pos.append(enemy.get_current_cell())
    
        
def generate_level():

    # === GENERE LE PLAYER ===
    
    
    tile_group = pg.sprite.Group()
    enemy_group = pg.sprite.Group()
    droped_item_group = pg.sprite.Group()
    text_group = pg.sprite.Group()
    mob_cell_pos = []
    
    all_spawn_cell_pos = generate_map(tile_group)
    generate_enemy(enemy_group, all_spawn_cell_pos, mob_cell_pos)
    
    
    
    return tile_group, enemy_group, droped_item_group, text_group, mob_cell_pos, all_spawn_cell_pos



def level_generator_loop(screen:pg.Surface, text, dropped_item_group, player):
    
    # === AFFICHAGE ===
    screen.fill("black")
    text.rect.x = screen.get_width()//2
    text.draw(screen)
    pg.display.update()
    
    tile_group, enemy_group, dropped_item_group, text_group, mob_cell_pos, all_spawn_cell_pos = generate_level()
    
    generate_items(dropped_item_group, all_spawn_cell_pos)
    
    PLAYER_IMG = image_loader("assets/images/entity/Exit.png")
    exit = Exit(PLAYER_IMG, get_random_spawn_pos(all_spawn_cell_pos))
    

    
    player.previous_cell_pos = get_random_spawn_pos(all_spawn_cell_pos)
    player.current_cell_pos = player.previous_cell_pos
    player.rect.topleft = (
            player.previous_cell_pos[0] * 32 * Entity.zoom,
            player.previous_cell_pos[1] * 32 * Entity.zoom,
        )
    player.end_pos = player.current_cell_pos
    Entity.is_changing_zoom = True
    return ("game",
            tile_group,
            enemy_group,
            dropped_item_group,
            text_group,
            mob_cell_pos,
            exit,
            True)
