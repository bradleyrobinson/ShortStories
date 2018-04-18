"""
(c) Bradley Robinson
"""
from game_state import ColorChanger
import pygame
import random

class Box(pygame.sprite.Sprite):
    """ Guess what it is?

    """
    def __init__(self, x=30, y=30, width=20, height=20):
        super(Box, self).__init__()
        self.color = ColorChanger(254, 254, 254)
        self.location = [x, y]
        self.width = width
        self.height = height

        self.image = pygame.Surface([width, height])
        self.image.fill(self.color.get_colors())

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.location
        self.direction = [0, 0]

    def move(self, x, y, size, frames):
        """

        Parameters
        ----------
        x : int
        y : int
        size : tuple or list, len(size) == 2

        """
        if x != 0 or y != 0:
            self.color.change_color()
        self.direction = [x, y]
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]
        self.check_collision(size)

    def draw(self, screen):
        """

        Parameters
        ----------
        screen : screen (I'm not sure what this is yet)
        """
        pygame.draw.rect(screen, self.color.get_colors(), self.rect)

    def check_collision(self, size):
        max_right = size[0] - self.width
        if self.rect.x >= max_right:
            self.rect.x = max_right
        if self.rect.x <= 0:
            self.rect.x = 0
        max_down = size[1] - self.height
        if self.rect.y >= max_down:
            self.rect.y = max_down
        if self.rect.y <= 0:
            self.rect.y = 0


class Player(Box):
    """
    A beautiful rectangle that will move and change colors as a player moves
    
    Ideas: add a beautiful fading tail
    """
    def __init__(self, x=30, y=30, width=20, height=20):
        super(Player, self).__init__(x, y, width, height)
