from collections import defaultdict
from .attributes import Strength, Health, Intelligence, Agility, Memory

class BaseLivingEntity:
    def __init__(self, name, tribe, lifespan, components=None):
        self.name = name
        self.tribe = tribe
        self.components = components if components is not None else {}
        self.memory = Memory(100)  # initialize Memory with a capacity of 100 events
        self.inventory = defaultdict(int)
        self.strength = Strength(10)  # initialize Strength with a value of 10
        self.health = Health(100)  # initialize Health with a value of 100
        self.intelligence = Intelligence(10)  # initialize Intelligence with a value of 10
        self.agility = Agility(10)  # initialize Agility with a value of 10
        self.age = 0
        self.lifespan = lifespan
        self.hunger = Hunger(0)
        self.thirst = Thirst(0)

    def add_component(self, component):
        self.components[component.name] = component

    def get_component(self, name):
        return self.components.get(name)

    def update(self):
        for component in self.components.values():
            component.update()
        self.age += 1
        self.hunger.increase(1)
        self.thirst.increase(1)

    def is_alive(self):
        return self.age < self.lifespan and not self.hunger.is_maxed() and not self.thirst.is_maxed()