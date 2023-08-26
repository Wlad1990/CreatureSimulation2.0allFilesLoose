import pygame
import noise
import numpy as np
import random

class DayNightCycle:
    def __init__(self, day_length, night_length, dawn_length, dusk_length):
        self.current_time = 0
        self.day_length = day_length
        self.night_length = night_length
        self.dawn_length = dawn_length
        self.dusk_length = dusk_length
        self.total_length = day_length + night_length + dawn_length + dusk_length

    def update(self):
        self.current_time = (self.current_time + 1) % self.total_length

    def get_time_of_day(self):
        if self.current_time < self.dawn_length:
            return "dawn"
        elif self.current_time < self.dawn_length + self.day_length:
            return "day"
        elif self.current_time < self.dawn_length + self.day_length + self.dusk_length:
            return "dusk"
        else:
            return "night"

    def get_light_level(self):
        time_of_day = self.get_time_of_day()
        if time_of_day == "day":
            return 1.0
        elif time_of_day == "night":
            return 0.0
        elif time_of_day == "dawn":
            return 0.5 + 0.5 * (self.current_time - self.dawn_length) / self.day_length
        else:  # dusk
            return 0.5 + 0.5 * (self.current_time - self.dawn_length - self.day_length) / self.dusk_length