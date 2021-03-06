# -*- coding: utf-8 -*-
from src import image, helper

def init_organisms(source_image, amount, verbose):
    organisms = []
    for i in range(amount):
        organisms.append( image.Organism(source_image) )
    if verbose: helper.log('initiated {} organisms', len(organisms))
    return organisms

def evaluate(organisms, verbose, current_generations):
    """Returns a list of (organism, score) tuples sorted by score, highest first"""
    evaluated = [ ( org, org.compare() ) for org in organisms ]
    evaluated = sorted(evaluated, key=lambda x: x[1], reverse=True)
    if verbose: helper.log('evaluated organisms, gen {}', current_generations)
    return evaluated

def create_new_candiditates(candidates, total):
    best = candidates[0][0]
    new = [best]
    new.extend( [best.mutate() for x in range(total)] )
    return new
