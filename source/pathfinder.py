# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques

from queue import PriorityQueue


# =================
# === FONCTIONS ===
# =================


def h(cell1, cell2):
    """Heuristique : distance de Manhattan."""
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)


def aStar(
    map: list, start: tuple[int, int], end: tuple[int, int], mob_coordinates: list = []
) -> list[tuple[int, int]]:
    """Retourne une liste contenant les cellules sur le chemin vers la cellule finale.
    Le debut et la fin apparraissent dans cette liste"""
    # --- Verif des infos transmises ---
    if (
        not type(map) == list
        and type(map[0]) == list
        and not len(map[0]) >= start[0] >= 0
        and len(map) >= start[1] >= 0
        and not len(map[0]) >= end[0] >= 0
        and len(map) >= end[1] >= 0
        and not end in mob_coordinates
    ):
        return None

    # Initialisation des scores
    g_score = {
        (x, y): float("inf") for x in range(len(map[0])) for y in range(len(map))
    }
    g_score[start] = 0
    f_score = {
        (x, y): float("inf") for x in range(len(map[0])) for y in range(len(map))
    }
    f_score[start] = h(start, end)

    # File des priorités
    open_set = PriorityQueue()
    open_set.put((f_score[start], start))

    # Stockage des chemins
    came_from = {}
    # Direction des voisins
    neighbor_direction = {"N": "S", "S": "N", "E": "O", "O": "E"}

    while not open_set.empty():
        current: tuple[int, int] = open_set.get()[1]

        # Si la destination est atteinte
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        # Vérification des voisins
        x, y = current
        for direction, (dx, dy) in {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "O": (-1, 0),
        }.items():
            neighbor = (x + dx, y + dy)

            # Vérification des limites et des murs
            if (
                0 <= neighbor[0] < len(map[0])
                and 0 <= neighbor[1] < len(map)
                and type(map[neighbor[1]][neighbor[0]]) is not int
                and not map[y][x].get_wall(direction)
                and not map[neighbor[1]][neighbor[0]].get_wall(
                    neighbor_direction[direction]
                )
                and neighbor not in mob_coordinates
            ):

                temp_g_score = g_score[current] + 1

                # Si un meilleur chemin est trouvé
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h(neighbor, end)
                    open_set.put((f_score[neighbor], neighbor))

    # Aucun chemin trouvé
    return None
