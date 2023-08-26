class Attribute:
    def __init__(self, initial_value, min_value=0, max_value=100):
        self.value = initial_value
        self.min_value = min_value
        self.max_value = max_value

    def increase(self, amount):
        self.value += amount
        self.value = min(self.value, self.max_value)

    def decrease(self, amount):
        self.value -= amount
        self.value = max(self.value, self.min_value)

    def is_maxed(self):
        return self.value == self.max_value

    def is_depleted(self):
        return self.value == self.min_value


class Strength(Attribute):
    def can_lift(self, weight):
        return self.value >= weight

    def exert(self, effort):
        self.decrease(effort)


class Speed(Attribute):
    def can_reach(self, distance, time):
        return distance / time <= self.value


class Intelligence(Attribute):
    def can_solve(self, difficulty):
        return self.value >= difficulty

    def learn(self, amount):
        self.increase(amount)


class Agility(Attribute):
    def can_dodge(self, difficulty):
        return self.value >= difficulty

    def perform_acrobatics(self, effort):
        self.decrease(effort)


class Health(Attribute):
    def is_healthy(self):
        return self.value > self.max_value / 2

    def recover(self, amount):
        self.increase(amount)

    def get_hurt(self, damage):
        self.decrease(damage)

class Hunger(Attribute):
    def is_hungry(self):
        return self.value > self.max_value / 2

    def eat(self, amount):
        self.decrease(amount)

class Thirst(Attribute):
    def is_thirsty(self):
        return self.value > self.max_value / 2

    def drink(self, amount):
        self.decrease(amount)


class Memory(Attribute):
    def __init__(self, initial_value, max_events=100):
        super().__init__(initial_value)
        self.log = []
        self.max_events = max_events

    def remember(self, event):
        self.log.append(event)
        if len(self.log) > self.max_events:
            self.log.pop(0)

    def forget(self, event):
        self.log.remove(event)

    def remember_recent(self, num_events):
        return self.log[-num_events:]