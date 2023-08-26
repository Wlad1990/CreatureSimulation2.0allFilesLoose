import pygame
import noise
import numpy as np
import random

class Terrain:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.scale = scale
        self.terrain = self.generate_terrain()
    
    def generate_terrain(self):
        world = np.zeros((self.width, self.height))
        for i in range(self.width):
            for j in range(self.height):
                world[i][j] = noise.pnoise2(i/self.scale, 
                                             j/self.scale, 
                                             octaves=6, 
                                             persistence=0.5, 
                                             lacunarity=2.0, 
                                             repeatx=1024, 
                                             repeaty=1024, 
                                             base=0)
        return world

    def draw(self, screen):
        terrain_surface = pygame.Surface((self.width, self.height))

        for i in range(self.terrain.shape[0]):
            for j in range(self.terrain.shape[1]):
                if self.terrain[i][j] < 0:
                    color = (0, 0, 255)  # water
                elif self.terrain[i][j] < 0.1:
                    color = (194, 178, 128)  # sand
                elif self.terrain[i][j] < 0.2:
                    color = (50, 220, 20)  # grass
                elif self.terrain[i][j] < 0.3:
                    color = (16, 122, 0)  # forest
                else:
                    color = (120, 120, 120)  # mountain
                pygame.draw.rect(terrain_surface, color, pygame.Rect(i, j, 1, 1))

        screen.blit(terrain_surface, (0, 0))

    def get_nearby_resources(self, location, radius):
        nearby_resources = []
        for resource in self.resources:
            distance = ((resource.location[0] - location[0])**2 + (resource.location[1] - location[1])**2)**0.5
            if distance <= radius:
                nearby_resources.append(resource)
        return nearby_resources
