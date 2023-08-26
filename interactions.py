class Interaction:
    def __init__(self, creature):
        self.creature = creature

    def execute(self):
        pass


class Communicate(Interaction):
    def __init__(self, creature, target, message):
        super().__init__(creature)
        self.target = target
        self.message = message

    def execute(self):
        self.target.memory.remember(f"Received message from {self.creature.name}: {self.message}")
        self.creature.memory.remember(f"Sent message to {self.target.name}: {self.message}")


class Fight(Interaction):
    def __init__(self, creature, target):
        super().__init__(creature)
        self.target = target

    def execute(self):
        if self.creature.strength.value > self.target.strength.value:
            self.creature.memory.remember(f"Fought with {self.target.name} and won")
            self.target.health.decrease(self.creature.strength.value)
            self.creature.energy.decrease(10)  # Fighting consumes energy
            self.creature.strength.increase(1)  # The creature becomes stronger from the fight
        else:
            self.creature.memory.remember(f"Fought with {self.target.name} and lost")
            self.creature.health.decrease(self.target.strength.value)
            self.creature.energy.decrease(10)  # Fighting consumes energy


class Trade(Interaction):
    def __init__(self, creature, target, give, receive):
        super().__init__(creature)
        self.target = target
        self.give = give
        self.receive = receive

    def execute(self):
        if self.give in self.creature.inventory and self.receive in self.target.inventory:
            self.creature.inventory[self.give] -= 1
            self.target.inventory[self.receive] -= 1
            self.creature.inventory[self.receive] += 1
            self.target.inventory[self.give] += 1
            self.creature.memory.remember(f"Traded {self.give} for {self.receive} with {self.target.name}")
            self.creature.intelligence.increase(1)  # The creature becomes smarter from the trade
        else:
            self.creature.memory.remember(f"Failed to trade {self.give} for {self.receive} with {self.target.name}")
            self.creature.intelligence.decrease(1)  # The creature becomes less intelligent from the failed trade


class Cooperate(Interaction):
    def __init__(self, creature, target, task):
        super().__init__(creature)
        self.target = target
        self.task = task

    def execute(self):
        if self.creature.agility.value + self.target.agility.value > 10:  # If the combined agility of the creatures is greater than 10, the task is successful
            self.creature.memory.remember(f"Cooperated with {self.target.name} to {self.task} and was successful")
            self.creature.agility.increase(1)  # The creature becomes more agile from the successful cooperation
            self.creature.intelligence.increase(1)  # The creature becomes smarter from the successful cooperation
        else:
            self.creature.memory.remember(f"Cooperated with {self.target.name} to {self.task} and failed")
            self.creature.agility.decrease(1)  # The creature becomes less agile from the failed cooperation
            self.creature.intelligence.decrease(1)  # The creature becomes less intelligent from the failed cooperation
