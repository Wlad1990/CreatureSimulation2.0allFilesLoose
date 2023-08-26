from .base import BaseLivingEntity


class WildAnimal(LivingEntity):
    def __init__(self, name, size, domesticatable=False, components=None):
        super().__init__(name, size, components)
        self.domesticatable = domesticatable


class Predator(WildAnimal):
    def __init__(self, name, size, pack_behavior=False, components=None):
        super().__init__(name, size, domesticatable=False, components=components)
        self.pack_behavior = pack_behavior