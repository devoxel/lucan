from src import image

def init_organisms(source_image, amount):
    organisms = []
    for i in range(amount):
        organisms.append( image.Im(source_image) )
    return organisms

def evaluate(organisms, source_image):
    """Returns a list of (organism, score) tuples sorted by score, highest first"""
    evaluated = [ ( org, org.compare() ) for org in organisms )
    return sorted(evaluated, key=lambda x: x[1], reverse=True)

def create_new_candiditates(candidates, total):
    best = candidates[0][0]
    print(best)
    return [best.mutate() for x in range(5)]
