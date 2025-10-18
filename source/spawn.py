# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# =======================================================================
# === Créer la liste de toutes les cases où les entités peuvent spawn ===
# =======================================================================

# ==============
# === IMPORT ===
# ==============

from random import randint
from tile import Wall

# ================
# === FONCTION ===
# ================


def get_all_spawn_pos(map):
    """Récupère toutes les positions de spawn sur la map, c'est-à-dire les case de type Wall

    Args:
        map (list): map avec les templates et les couloirs

    Returns:
        list: liste des positions de spawn
    """
    spawn_pos = []
    # On parcours la map
    for y in range(len(map)):
        for x in range(len(map[0])):
            # Si la case est un mur, on l'ajoute à la liste des positions de spawn
            if type(map[y][x]) == Wall:
                # Si le mur ne possède pas tout ses murs
                if not (
                    map[y][x].get_wall('N') and
                    map[y][x].get_wall('E') and
                    map[y][x].get_wall('S') and
                    map[y][x].get_wall('O')
                ):
                    spawn_pos.append((x, y))

    return spawn_pos


def get_random_spawn_pos(all_spawn_pos):
    """Récupère une position de spawn aléatoire

    Args:
        map (list): map avec les templates et les couloirs

    Returns:
        tuple: position de spawn
    """
    return all_spawn_pos.pop(randint(0, len(all_spawn_pos) - 1))
