# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin

class Counter:
    """Sert a compter (du temps, des tours, etc...).Compte à reboure ou en avançant."""

    def __init__(self, default_value: float, ascending: bool = False):
        self.default_value = default_value  # Indique le temps par defaut ( temps a ateindre ou temps de depart)
        self.ascending = ascending  # Indique si le timer augmente ou diminue
        self.is_counting = False  # Indique si le timer est actif (s'il compte)
        self.value = None  # Indique la valeur actuel du counter
        self.reset()

    # ================
    # === METHODES ===
    # ================

    def start(self):
        """Demare le counter avec ses valeurs par defaut"""
        self.is_counting = True
        if self.ascending:
            self.value = 0
        else:
            self.value = self.default_value

    def reset(self):
        """Stop le counter et met ses valeurs par defaut"""
        self.is_counting = False  # Indique si le timer est actif (s'il compte)
        # Initialise l'atribut value
        if self.ascending:
            self.value = 0
        else:
            self.value = self.default_value

    def stop(self):
        """Met le counter en pause"""
        self.is_counting = False

    def resume(self):
        """Reprend le counter la ou il s'est arrete"""
        self.is_counting = True

    # === GETTERS ===
    def get_time(self):
        """Renvoie le temps actuel"""
        return self.value

    def get_is_counting(self):
        """Indique si le counter est arrive au bout"""
        return self.is_counting

    def get_time_left(self) -> float:
        """Renvoie le temps restant avant la fin"""
        if self.ascending:
            return self.default_value - self.value
        return self.value

    # === UPDATE ===
    def update(self, value_to_add: float) -> bool:
        """Update le counter et renvoie True si le counter est finie.
        Renvoie False sinon"""
        if self.is_counting:
            if self.ascending:
                if self.value < self.default_value:
                    self.value += value_to_add
                    return False
                else:
                    self.value = 0
                    self.is_counting = False

            else:
                if self.value > 0:
                    self.value -= value_to_add
                    return False
                else:
                    self.value = self.default_value
                    self.is_counting = False

        return True
