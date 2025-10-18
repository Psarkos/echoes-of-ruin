# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin

# ================================
# === DEFINITION DES FONCTIONS ===
# ================================

def is_case_lookable(map, pos1, pos2):
    """ Regarde s'il y a un mur sur la droite séparant les deux cases,
        si les cases sont sur la même colonne alors je parcours les cases 
        sur cette même colonne

    Args:
        map (list): map ingame
        pos1 (tuple): position de la première case
        pos2 (tuple): position de la deuxième case

    Returns:
        bool: True s'il n'y a aucun mur entre les deux cases 
              lorsque l'on trace une droite entre elles, False sinon
    """
    if pos1[0] >= len(map[0]) and pos1[1] >= len(map) and pos2[0] >= len(map[0]) and pos2[1] >= len(map):
        return False
    
    if pos1[0] == pos2[0]:
        return vertical_right(map, pos1, pos2)
    a, b = found_a_and_b(pos1, pos2)
    
    if a == 0:
        return x_verifying(map, pos1, pos2, a, b)
    return x_verifying(map, pos1, pos2, a, b) and y_verifying(map, pos1, pos2, a, b)
    

def vertical_right(map, pos1, pos2):
    """ Fonction qui regarde sur la droite passant par les deux cases 
        lorsqu'elles sont sur la même colonne s'il a au moins un mur horizontal 
        (Sud ou Nord), en parcourant les cases de cette colonne

    Args:
        map (list): map ingame
        pos1 (tuple): position de la première case
        pos2 (tuple): position de la deuxième case

    Returns:
        bool: True s'il n'y a aucun mur verticale sur la ligne droite entre les deux entités
              False sinon
    """
    from tile import Wall
    
    x = pos1[0]
    
    for y in range(
        min([pos1[1], pos2[1]]),
        max([pos1[1], pos2[1]])
    ):
        if y >= 0:
            if not (
                type(map[y][x]) is Wall and 
                type(map[y + 1][x]) is Wall
            ):
                return False
            # Si au moins une des cases a un mur sur la droite (fonction affine)
            elif (
                map[y][x].get_wall('S') and 
                map[y + 1][x].get_wall('N')
            ):
                return False
    return True


def x_verifying(map, pos1, pos2, a, b):
    """ Fonction qui regarde sur la droite passant par les deux cases s'il a 
        au moins un mur verticale (Est ou Ouest), en utilisant la formule de 
        la fonction affine passant par ces cases

    Args:
        map (list): map ingame
        pos1 (tuple): position de la première case
        pos2 (tuple): position de la deuxième case
        a (int): coefficient directeur de la droite passant par les deux cases
        b (int): ordonné à l'origine de la droite passant par les deux cases

    Returns:
        bool: True s'il n'y a aucun mur verticale sur la ligne droite entre les deux entités
              False sinon
    """
    from tile import Wall
    
    for x in range(
        min([pos1[0], pos2[0]]),
        max([pos1[0], pos2[0]]),
    ):
        if x >= 0:
            y = round(fonction_affine(a, b, x + 0.5))
            # Si la case regarder et sa voisine de droite ne sont pas toutes les deux des murs
            if not (
                type(map[y][x]) is Wall and 
                type(map[y][x + 1]) is Wall
            ):
                return False
            # Si au moins une des cases a un mur sur la droite (fonction affine)
            elif (
                map[y][x].get_wall('E') and 
                map[y][x + 1].get_wall('O')
            ):
                return False
    return True


def y_verifying(map, pos1, pos2, a, b):
    """ Fonction qui regarde sur la droite passant par les deux cases s'il a 
        au moins un mur horizontal (Sud ou Nord), en utilisant la formule de 
        de l'antécédant de la fonction affine passant par ces cases

    Args:
        map (list): map ingame
        pos1 (tuple): position de la première case
        pos2 (tuple): position de la deuxième case
        a (int): coefficient directeur de la droite passant par les deux cases
        b (int): ordonné à l'origine de la droite passant par les deux cases

    Returns:
        bool: True s'il n'y a aucun mur horizontal sur la ligne droite entre les deux entités
              False sinon
    """
    from tile import Wall
    
    for y in range(
        min([pos1[1], pos2[1]]), 
        max([pos1[1], pos2[1]])
    ):
        if y >= 0:
            x = round(antecedant_fonction_affine(a, b, y + 0.5))
            # Si la case regarder et sa voisine de dessous ne sont pas toutes les deux des murs
            if not (
                type(map[y][x]) is Wall and 
                type(map[y + 1][x]) is Wall
            ):
                return False
            # Si au moins une des cases a un mur sur la droite (fonction affine)
            elif (
                map[y][x].get_wall('S') and 
                map[y + 1][x].get_wall('N')
            ):
                return False
    return True


def found_a_and_b(pos1, pos2):
    """ Trouve les valeurs a et b de la fonction affine qui passe
        par les deux points rentrés en paramètres

    Args:
        pos1 (tuple): première position
        pos2 (tuple): deuxième position

    Returns:
        tuple: les valuers de a et b
    """
    if not pos2[0] - pos1[0] == 0:
        a = (pos2[1] - pos1[1]) / (pos2[0] - pos1[0])
    else:
        a = 0
    b = - (a * pos1[0]) + pos1[1]
    return a, b


def fonction_affine(a, b, x):
    """ Sert de fonction affine mutable """
    return a * x + b


def antecedant_fonction_affine(a, b, y):
    """ Renvoie l'antécédant de la fonction affine """
    return (y - b) / a
