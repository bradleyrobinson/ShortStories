"""
(c) Bradley Robinson

Stuff for the game 
"""


class ColorChanger(object):
    def __init__(self, r=0, g=0, b=0):
        self.colors = [r, g, b]
        self.add_color = [True, False, False]
        self.increase = 1

    def change_color(self):
        for i, color in enumerate(self.colors[:]):
            if self.add_color[i]:
                self.colors[i] = color + self.increase
                if color >= 254 and self.increase == 1 or color <= 1 and self.increase == -1:
                    if i < 2:
                        self.add_color[i] = False
                        self.add_color[i + 1] = True
                    elif i == 2:
                        self.add_color[0] = True
                        self.add_color[i] = False
                        self.increase *= -1

    def get_colors(self):
        return self.colors


