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
        return -100000

def get_line_equation(p1, p2):
    try:
        m = (p1[1] - p2[1]) / (p1[0] - p2[1])
    except ZeroDivisionError:
        m = 0
    return (lambda x: ((m*x) - (m*p1[0]) - p1[1]) == 0)

class Organism(object):
    MODE = "RGB"
    BG_FILL = (255,255,255)
    LINE_FILL = (0,0,0)

    def __init__(self, source_image, lines=[], traits = {}):
        self.source = source_image
        self.size = self.source.size
        self.im = Image.new(self.MODE, self.size, color=self.BG_FILL)
        self.draw = ImageDraw.Draw(self.im)
        self.points = set()
        self.lines = lines
        if lines:
            self.generate_from_lines()
        self.traits = self.traits_mutate(traits)

    def generate_from_lines(self):
        for p1, p2 in self.lines:
            self.draw.line( (p1, p2), self.LINE_FILL, 2)

    def make_line(self):
        return edge_tuple(self.size)

    def mutate(self):
        new_lines = []
        for i in range(int(self.traits['grow_iterations'])):
            if random.random() < self.traits['newline_influence']:
                new_lines.append(self.make_line())
        for p1, p2 in self.lines:
            for x,y in (p1, p2):
                if random.random() < self.traits['mutate_influence']:
                    magnitude = random.random() * self.size[0]
                    direction = random.choice([-1, 1])
                    x = x*magnitude*direction
                if random.random() < self.traits['mutate_influence']:
                    magnitude = random.random() * self.size[1]
                    direction = random.choice([-1, 1])
                    y = y*magnitude*direction
            if random.random() > self.traits['delete_line_influence']:
                new_lines.append( (p1, p2) )
        return Organism(self.source, new_lines, self.traits)

    def traits_mutate(self, traits):
        random_traits = {
            'grow_iterations'     : random.random()*1000,
            'newline_influence'        : random.random(),
            'mutate_influence'    : random.random(),
            'diversity'           : random.random(),
            'delete_line_influence': random.random()
        }
        if 'diversity' in traits:
            random_traits['diversity'] = traits['diversity']
        for trait in traits.keys():
            if random.random() > random_traits['diversity']:
                random_traits[trait] = traits[trait] # TODO implement leaning
        return random_traits

    def compare(self):
        total_score = 0
        compared = set()
        for p1, p2 in self.lines:
            eq = get_line_equation(p1, p2)
            for x in range(min( int(p1[0]) , int(p2[0])), max(int(p1[0]), int(p1[0])) ):
                y = eq(x)
                if (x,y) not in compared:
                    total_score += similar((x,y), self.source, self.im)
                    compared.add((x,y))
        return (total_score)

    def __repr__(self):
        return "|org|"
