"""
(c) Bradley Robinson
"""
from game_state import ColorChanger
import pygame
import random


class Box(pygame.sprite.Sprite):
    """ Guess what it is?

    """
    def __init__(self, x=30, y=30, width=20, height=20, color=(254,254,254)):
        super(Box, self).__init__()
        self.color = ColorChanger(color[0], color[1], color[2])
        self.location = [x, y]
        self.width = width
        self.height = height

        self.image = pygame.Surface([width, height])
        self.image.fill(self.color.get_colors())

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.location
        self.direction = [0, 0]

    def move(self, x, y, size, change_by=0):
        """

        Parameters
        ----------
        x : int
        y : int
        size : tuple or list, len(size) == 2

        """
        if x != 0 or y != 0:
            self.color.change_color(change_by=change_by)
        self.direction = [x, y]
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]
        self.location = [self.rect.x, self.rect.y]
        return self.check_collision(size)

    def draw(self, screen):
        """

        Parameters
        ----------
        screen : screen (I'm not sure what this is yet)
        """
        pygame.draw.rect(screen, self.color.get_colors(), self.rect)

    def check_collision(self, size):
        maxed_out = False
        max_right = size[0] - self.width
        if self.rect.x >= max_right:
            self.rect.x = max_right
            maxed_out = True
        if self.rect.x <= 0:
            self.rect.x = 0
            maxed_out = True
        max_down = size[1] - self.height
        if self.rect.y >= max_down:
            self.rect.y = max_down
            maxed_out = True
        if self.rect.y <= 0:
            self.rect.y = 0
            maxed_out = True
        return maxed_out


class Player(Box):
    """
    A beautiful rectangle that will move and change colors as a player moves
    
    Ideas: add a beautiful fading tail
    """
    def __init__(self, x=30, y=30, width=20, height=20):
        super(Player, self).__init__(x, y, width, height)


class Explosion(object):
    """
    Can we create some pixels that 
    
    """
    def __init__(self, starting_location, screen_size,
                 density=20, color=(112, 112, 112)):
        """
        
        Parameters
        ----------
        starting_location
        density
        color
        """
        self.screen_size = screen_size
        # TODO: Experiment with different shapes? Start in different locations?
        # TODO: Change it to parameter
        self.boxes = [Box(starting_location[0] + 10,
                          starting_location[1] + 10,
                          2, 2, color) for i in range(density)]
        # TODO: fade the boxes

    def draw(self, screen):
        new_boxes = []
        for box in self.boxes:
            move_direction = (random.randint(-2, 2), random.randint(-2, 2))
            max_out = box.move(move_direction[0], move_direction[1],
                               self.screen_size)
            box.draw(screen)
            if not max_out:
                new_boxes.append(box)
        self.boxes = new_boxes


class ShrinkingEmptyBox(pygame.sprite.Sprite):
    def __init__(self, size):
        super(ShrinkingEmptyBox, self).__init__()

