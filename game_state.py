"""
(c) Bradley Robinson

Stuff for the game 
"""


class ColorChanger(object):
    def __init__(self, r=0, g=0, b=0, increase=1):
        self.colors = [r, g, b]
        self.add_color = [True, False, False]
        self.increase = increase

    def change_color(self, change_by=0):
        for i, color in enumerate(self.colors[:]):
            if self.add_color[i]:
                self.colors[i] = color + self.increase + change_by
                if self.colors[i] >= 254 and self.increase > 0 \
                        or self.colors[i] <= 1 and self.increase < 0:
                    if self.colors[i] > 254:
                        self.colors[i] = 254
                    if self.colors[i] < 0:
                        self.colors[i] = 0
                    if i < 2:
                        self.add_color[i] = False
                        self.add_color[i + 1] = True
                    elif i == 2:
                        self.add_color[0] = True
                        self.add_color[i] = False
                        self.increase *= -1

    def get_colors(self):
        return self.colors


