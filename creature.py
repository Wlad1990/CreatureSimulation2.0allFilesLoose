from .base import BaseLivingEntity

class Creature(BaseLivingEntity):
    def __init__(self, name, tribe, components=None, parent1=None, parent2=None):
        self.name = name
        self.tribe = tribe
        self.components = components if components is not None else {}
        self.parent1 = parent1
        self.parent2 = parent2
        self.tools = []
        self.memory = Memory(100)  # initialize Memory with a capacity of 100 events
        self.inventory = defaultdict(int)
        self.strength = Strength(10)  # initialize Strength with a value of 10
        self.health = Health(100)  # initialize Health with a value of 100
        self.intelligence = Intelligence(10)  # initialize Intelligence with a value of 10
        self.agility = Agility(10)  # initialize Agility with a value of 10
        self.behavior = Behavior(self)  # Attach behavior instance to the creature

    def add_component(self, component):
        self.components[component.name] = component

    def get_component(self, name):
        return self.components.get(name)

    def update(self):
        for component in self.components.values():
            component.update()

        if self.hunger.is_hungry() and "Food" in self.inventory:
            amount_eaten = min(self.hunger.value, self.inventory["Food"])
            self.hunger.eat(amount_eaten)
            self.inventory["Food"] -= amount_eaten

        if self.thirst.is_thirsty() and "Water" in self.inventory:
            amount_drank = min(self.thirst.value, self.inventory["Water"])
            self.thirst.drink(amount_drank)
            self.inventory["Water"] -= amount_drank

        # Check if the creature has died
        if not self.is_alive():
            self.memory.remember("I have died")

    def make_tool(self, tool):
        if tool.required_resources.items() <= self.inventory.items():  # check if the creature has all the required resources
            for resource, amount in tool.required_resources.items():
                self.inventory[resource] -= amount  # remove the resources used to make the tool
            self.tools.append(tool)  # add the tool to the creature's tools
            self.memory.remember(f"Made a {tool.name}")
        else:
            self.memory.remember(f"Tried to make a {tool.name} but didn't have all the required resources")

    def gather(self, resource):
        if resource.required_tool and resource.required_tool not in self.tools:
            self.memory.remember(f"Tried to gather {resource.name} but didn't have the required tool")
        elif not self.strength.can_lift(resource.weight):
            self.memory.remember(f"Tried to gather {resource.name} but wasn't strong enough")
        else:
            amount_gathered = min(self.strength.value, resource.quantity)
            if resource.required_tool:
                amount_gathered *= 2  # gathering is twice as efficient with the required tool
            resource.use(amount_gathered)
            self.inventory[resource.name] += amount_gathered
            self.memory.remember(f"Gathered {amount_gathered} of {resource.name}")

    def draw(self, screen):
        x, y = self.position
        pygame.draw.circle(screen, self.color, (int(x), int(y)), self.size)

    def visible_creatures(self):
        visible_creatures = []
        for creature in self.world.creatures:
            if creature != self:  # A creature cannot see itself
                distance = self.calculate_distance(self.location, creature.location)
                if distance <= self.visibility_radius:
                    visible_creatures.append(creature)
        return visible_creatures

    def visible_resources(self):
        visible_resources = []
        for resource in self.world.resources:
            distance = self.calculate_distance(self.location, resource.location)
            if distance <= self.visibility_radius:
                visible_resources.append(resource)
        return visible_resources

    @staticmethod
    def calculate_distance(location1, location2):
        x1, y1 = location1
        x2, y2 = location2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def generate_prompt(self, world):
        # Create a list of descriptions of nearby resources
        nearby_resources = [f"There is a {resource.name} nearby." for resource in world.get_nearby_resources(self)]
        
        # Combine all the elements into a single string
        prompt = (
            f"I am a {self.name} of the {self.tribe} tribe. "
            f"My current health is {self.health.value}, hunger is {self.hunger.value}, and thirst is {self.thirst.value}. "
            f"I am located at {self.location}. "
            + ' '.join(nearby_resources) 
            + f" My recent memories are: {' '.join(self.memory.remember_recent(5))}"
        )
        
        return prompt

    def decide_interaction(self):
        if self.health.value < 50:
            # If the creature's health is low, it will try to avoid fights
            return self.cooperate if self.intelligence.value > 50 else self.trade
        elif self.strength.value > 50:
            # If the creature is strong, it is more likely to choose to fight
            return self.fight if self.health.value > 50 else self.cooperate
        elif self.intelligence.value > 50:
            # If the creature is intelligent, it might prefer to trade or cooperate
            return self.trade if self.inventory else self.cooperate
        else:
            # Otherwise, it will choose randomly
            return random.choice([self.fight, self.trade, self.cooperate])

    def update(self, world):
        # Update creature's components
        for component in self.components.values():
            component.update()

        # Decide what interaction to perform based on the creature's current state
        interaction = self.decide_interaction()

        # Choose a target for the interaction
        # This could also take into account the creature's past experiences with other creatures
        target = random.choice(world.creatures)

        # Perform the interaction
        interaction(target)

    def fight(self, target):
        interaction = Fight(self, target)
        interaction.execute()

    def trade(self, target, give, receive):
        interaction = Trade(self, target, give, receive)
        interaction.execute()

    def cooperate(self, target, task):
        interaction = Cooperate(self, target, task)
        interaction.execute()

    def execute_action(self, action):
        action_type, target, details = action
        if action_type == "move":
            direction = details
            self.move(direction)
        elif action_type == "gather":
            resource = self.visible_resources()[details]
            if resource:
                self.gather(resource)
        elif action_type == "fight":
            target = self.visible_creatures()[details]
            if target:
                fight = Fight(self, target)
                fight.execute()
        elif action_type == "trade":
            target = self.visible_creatures()[details]
            if target:
                # for simplification, we are randomly choosing a resource to trade
                resource_to_trade = random.choice(list(self.inventory.keys()))
                trade = Trade(self, target, resource_to_trade, details)
                trade.execute()
        elif action_type == "cooperate":
            target = self.visible_creatures()[details]
            if target:
                cooperate = Cooperate(self, target, details)
                cooperate.execute()
        else:
            print(f"Unknown action: {action_type}")
