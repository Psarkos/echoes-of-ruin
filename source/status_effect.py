# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
# ======================
# === INITIALISATION ===
# ======================

# === IMPORTATIONS ===
# Iportation de toutes les bibliotheques


class StatusEffect:
    """Un effet de status dont les effets sont permanent (soin, poison, etc...)

    le parametre 'is_continuous' indique si les effets ont lieu chaque tour"""

    def __init__(
        self, name: str, duration: int, is_continuous: bool = True, kwargs={}
    ):
        self.name = name
        self.duration = duration
        self.is_continuous = is_continuous
        self.stats = kwargs
        if not self.is_continuous:
            self.first_update = True

    def change_duration(self, value: int):
        self.duration += value

    def copy(self):
        var = StatusEffect(self.name, self.duration, self.is_continuous)
        var.stats = self.stats.copy()
        return var

    def update(self):
        if self.duration > 0:
            self.duration -= 1
            if not self.is_continuous:
                if self.first_update:
                    self.first_update = False
                    return self.stats
            else:
                return self.stats

    def __eq__(self, other):
        return self.name == other.name and self.stats == other.stats

    def __repr__(self):
        return str((self.name, self.duration, self.stats))


class StatusEffectsHandler:

    def __init__(self):
        self.status_effects = []

    def add_status_effect(self, status_effect: StatusEffect):
        is_status_effect_exist = False
        for effect in self.status_effects:
            if effect == status_effect:
                effect.change_duration(status_effect.duration)
                is_status_effect_exist = True
                break
        if not is_status_effect_exist:

            self.status_effects.append(status_effect.copy())

    def remove_status_effect(self, i):
        self.status_effects.pop(i)

    def clear(self):
        self.status_effects.clear()

    def update(self):
        effect_stats_dict = {}

        for i in range(len(self.status_effects) - 1, -1, -1):
            effect = self.status_effects[i]
            var = effect.update()

            if var is not None:
                for key, value in var.items():
                    effect_stats_dict[key] = effect_stats_dict.get(key, 0) + value

            if effect.duration <= 0:

                if not effect.is_continuous:
                    for key, value in effect.stats.items():
                        effect_stats_dict[key] = effect_stats_dict.get(key, 0) - value

                self.remove_status_effect(i)

        return effect_stats_dict


if __name__ == "__main__":
    heal = StatusEffect("Heal", 1, True, health=10)
    speed_boost = StatusEffect("Boost de vitesse", 1, False, movement_time=20)

    stat_handler = StatusEffectsHandler()
    stat_handler.add_status_effect(heal)
    print(heal, stat_handler.status_effects)
    stat_handler.update()
