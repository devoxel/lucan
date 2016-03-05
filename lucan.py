"""python lucan.py path-to-source"""

import sys
from src import genetic, image

source = image.open(sys.argv[1])
organisms = genetic.init_organisms(source, 5)

for i in range(0, int(sys.argv[2])):
    for org in organisms:
        org.simulate()
    evaluated = genetic.evaluate(organisms, source)
    organisms = genetic.create_new_candiditates(evaluated, 4)

organisms[0].im.show()
