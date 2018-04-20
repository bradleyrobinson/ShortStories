"""
(c) 2018 Bradley Robinson

For now, this is where the "levels" will be.
"""
import pygame.font
from collections import deque


class Level(object):
    def __init__(self):
        pass


class Text(object):
    def __init__(self, size, messages, screen_size, repeat=False):
        """
        
        Parameters
        ----------
        size
        messages : list
        """
        self.font = pygame.font.SysFont("monospace", size)
        self.size = size
        self.repeat = repeat
        self.messages = messages
        self.queue = None
        self.reset_queue()
        self.screen_size = screen_size
        self.current_message = None

    def render(self, color, screen, new_message=False,
               centered=True, location=None):
        if len(self.queue) == 0:
            if self.repeat:
                self.reset_queue()
            else:
                return
        if self.current_message is None or new_message:
            self.font = pygame.font.SysFont("monospace", self.size)
            self.current_message = self.queue.popleft()
        if centered:
            location = self.get_center(self.current_message)
        else:
            # TODO: finish this
            pass
        if location is None or len(location) != 2:
            # Fail here if there is no location and it's
            # not centered
            return
        label = self.font.render(self.current_message, 1, color, screen)
        screen.blit(label, location)

    def get_center(self, message):
        size = self.font.size(message)
        center_x, center_y = self.screen_size[0]/2, self.screen_size[1]/2
        half_width, half_height =  size[0]/2, size[1]/2
        position_x = center_x - half_width
        position_y = center_y - half_height
        return position_x, position_y

    def reset_queue(self):
        self.queue = deque(self.messages)


def opposite_color(colors):
    colors = [wrap_around(c) for c in colors]
    return colors


def wrap_around(x):
    result = 45 - x
    if result < 0:
        remainder = result
        result = 254 + remainder
    return result
