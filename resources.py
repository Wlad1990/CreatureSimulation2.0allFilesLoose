import csv
import os

class Resource:
    TYPES = {
        "Wood": {"weight": 5, "quantity": 100},
        "Stone": {"weight": 10, "quantity": 200},
        "Water": {"weight": 1, "quantity": 500},
        "Iron": {"weight": 20, "quantity": 50},
        "Meat": {"weight": 2, "quantity": 150},
        "Crop": {"weight": 1, "quantity": 300},
        "Vegetable": {"weight": 1, "quantity": 250},
        "Fruit": {"weight": 1, "quantity": 250},
        "Alcohol": {"weight": 1, "quantity": 100},
        "DrinkingWater": {"weight": 1, "quantity": 500}
    }

    def __init__(self, name, distribution, quantity, location, regrowth_rate=0):
        self.name = name
        self.distribution = distribution
        self.quantity = quantity
        self.location = location
        self.regrowth_rate = regrowth_rate

    def use(self, amount):
        if self.quantity >= amount:
            self.quantity -= amount
        else:
            raise ValueError(f"Not enough {self.name} available")

    def replenish(self, amount=None):
        if amount is None:
            self.quantity += self.regrowth_rate
        else:
            self.quantity += amount


def load_resources_from_csv(file_path):
    resources = []
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Assuming CSV contains columns: Name, Distribution, Quantity, Density (as a sample)
                resource = Resource(name=row['Name'], distribution=row['Distribution'],
                                    quantity=int(row['Quantity']), location=None)
                resources.append(resource)
        return resources
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None


# Load resources from CSV if available, else fall back to hardcoded values
csv_resources = load_resources_from_csv("path_to_csv")
if csv_resources:
    RESOURCES = csv_resources
else:
    # Hardcoded resources as fallback
    RESOURCES = [
        # Add hardcoded resources here
    ]

class Stone(Resource):
    def __init__(self, location, quantity=1000):
        super().__init__("Stone", "common", quantity, location)

class Iron(Resource):
    def __init__(self, quantity=500):
        super().__init__("Iron", "common", quantity, location)


class Wood(Resource):
    def __init__(self, location, quantity=1000):
        super().__init__("Wood", "common", quantity, location, required_tool="Axe")


class Soil(Resource):
    def __init__(self, quantity=2000):
        super().__init__("Soil", "common", quantity, location)


class Water(Resource):
    def __init__(self, quantity=1500):
        super().__init__("Water", "common", quantity, location)


class Food(Resource):
    def __init__(self, name, nutrition, quantity=100):
        super().__init__(name, "common", quantity, location)
        self.nutrition = nutrition

    def consume(self, creature, amount):
        super().use(amount)
        creature.hunger -= self.nutrition * amount
        creature.memory.append(f"Consumed {amount} of {self.name}")


class DrinkingWater(Resource):
    def __init__(self, location, quantity=1500):
        super().__init__("Drinking Water", "common", quantity, location)

    def consume(self, creature, amount):
        super().use(amount)
        creature.thirst -= amount
        creature.memory.append(f"Drank {amount} of {self.name}")


class SeaWater(Resource):
    def __init__(self, location, quantity=1500):
        super().__init__("Sea Water", "common", quantity, location)

    def consume(self, creature, amount):
        super().use(amount)
        creature.thirst -= amount / 2  # Sea water is not as hydrating as drinking water
        creature.memory.append(f"Drank {amount} of {self.name}")


class Medicine(Resource):
    def __init__(self, name, health_benefit, quantity=50):
        super().__init__(name, "rare", quantity)
        self.health_benefit = health_benefit

    def use(self, creature, amount):
        super().use(amount)
        creature.health += self.health_benefit * amount
        creature.memory.append(f"Used {amount} of {self.name}")