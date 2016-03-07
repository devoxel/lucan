# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageSequence
from src import helper
import random
from math import floor

def open(path):
    return Image.open(path)

def point_on_edge(size, edge):
    # the edge signifies the edge. 0,1 = top, bottom
    #                              2,3 = left, right
    x, y = 0, 0
    if edge <= 1:
        x = random.random() * size[0]
        if edge == 1:
            y = size[1]
    else:
        y = random.random() * size[1]
        if edge == 3:
            x = size[0]
    return (x,y)

def edge_tuple(size):
    edge = random.randint(0, 3)
    edges = [0,1,2,3]
    edges.remove(edge)
    edge2 = random.choice(edges)
    return point_on_edge(size, edge), point_on_edge(size, edge2)

def similar(point, source, candidate):
    source_pixel = source.getpixel(point)
    candidate_pixel = candidate.getpixel(point)
    if source_pixel == candidate_pixel:
        return 1
    else:
        return -10000

"""
def get_line_equation(p1, p2):
     m = (p1[1] - p2[1]) / (p1[0] - p2[1])
     return (lambda x,y
     : ((m*x) - (m*p1[0]) - y - p1[1]) == 0)
"""

class Organism(object):
    MODE = "RGB"
    BG_FILL = (255,255,255)
    LINE_FILL = (0,0,0)

    GROW_ITERATIONS     = 20
    PROB_NEWLINE        = .3
    PROB_CHANGEDLINE    = .1

    def __init__(self, source_image, lines=[]):
        self.source = source_image
        self.size = self.source.size
        self.im = Image.new(self.MODE, self.size, color=self.BG_FILL)
        self.draw = ImageDraw.Draw(self.im)
        self.points = set()
        self.lines = lines
        if lines:
            self.generate_from_lines()

    """
    def _generate_points(self):
        self.points = set()
        for p1, p2 in self.lines:
            f = get_line_equation(p1, p2)
            for x in range(min(p1[0], p2[0]), max(p1[0], p2[0])):
                for y in range(min(p1[1], p2[1]), max(p1[1], p2[1])):
                    self.points.union( set( [(x, f(x))  ) )
    """

    def generate_from_lines(self):
        for p1, p2 in self.lines:
            self.draw.line( (p1, p2), self.LINE_FILL, 2)

    def make_line(self):
        return edge_tuple(self.size)

    def mutate(self):
        new_lines = []
        for i in range(self.GROW_ITERATIONS):
            if random.random() < self.PROB_NEWLINE:
                new_lines.append(self.make_line())
        for p1, p2 in self.lines:
            for x,y in (p1, p2):
                if random.random() < self.PROB_CHANGEDLINE:
                    magnitude = random.random() * self.size[0]
                    direction = random.choice([-1, 1])
                    x = x*magnitude*direction
                if random.random() < self.PROB_CHANGEDLINE:
                    magnitude = random.random() * self.size[1]
                    direction = random.choice([-1, 1])
                    y = y*magnitude*direction
            new_lines.append( (p1, p2) )
        return Organism(self.source, new_lines)

    def compare(self):
        total_score = 0
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                total_score += similar((x,y), self.source, self.im)
        return total_score

    def __repr__(self):
        return u"生活"
