# -*- coding: utf-8 -*-
from src import image, helper

def init_organisms(source_image, amount, verbose):
    organisms = []
    for i in range(amount):
        organisms.append( image.Organism(source_image) )
    if verbose: helper.log('initiated {} organisms', len(organisms))
    return organisms

def evaluate(organisms, verbose):
    """Returns a list of (organism, score) tuples sorted by score, highest first"""
    evaluated = [ ( org, org.compare() ) for org in organisms ]
    evaluated = sorted(evaluated, key=lambda x: x[1], reverse=True)
    if verbose: helper.log('evaluated organisms: {}', evaluated)
    return evaluated

def create_new_candiditates(candidates, total):
    best = candidates[0][0]
    return [best.mutate() for x in range(total)]
