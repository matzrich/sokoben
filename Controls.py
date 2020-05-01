import const
import pygame
from pygame.locals import *

controls = {}

def add(name, tile, x, y, enabled):
    controls[name] = Control(name, tile, x, y, enabled)

class Control:
    def __init__(self, name, tile, x, y, enabled):
        self.name = name
        self.tile = tile
        self.x = x
        self.y = y
        self.width = self.tile.get_width()
        self.height = self.tile.get_height()

        self.enabled = enabled

    def draw(self):
        if not self.enabled:
            return None

        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()
        surface.blit(self.tile, (0, 0))
        return surface

    def toggle(self):
        self.enabled = not self.enabled

    def isClicked(self, mousePos):
        if self.enabled:
            x, y = mousePos
            if x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height:
                return True
        
        return False
    