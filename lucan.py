#!/bin/env python`
"""./lucan.py [OPTIONS] SOURCE OUTPUT

Arguments:
 SOURCE:            Path to the source image file
 OUTPUT:            Path to the output image file

Options:
 -v, --verbose          Output everything to stdout
 -V, --version          Output version number
 -g, --generations <n>  Amount of generations. Defaults to 5
 -c, --candidates <n>   Amount of candidates per generation. Defaults to 5
 -h, --help             Print this help
"""

import sys
from src import genetic, image

def arg_parse():
    """Modifies src's initialization state to match the sys arguments"""
    # short_form --> long_form, type, default
    CLI = {
        'v': ['verbose',        FLAG,       False],
        'V': ['version',        FLAG,       False],
        'h': ['help',           FLAG,       False],
        'g': ['generations',    PROPERTY,   5],
        'c': ['candidates',     PROPERTY,   5]
    }
    for arg in sys.argv:
        if CLI.get(arg[0]):
            # TODO check type
            # TODO modify state
    # TODO map arguments to src's global state

def cli():
    source = image.open(sys.argv[1])
    organisms = genetic.init_organisms(source, 5)

    for i in range(0, int(sys.argv[2])):
        for org in organisms:
            org.simulate()
        evaluated = genetic.evaluate(organisms, source)
        organisms = genetic.create_new_candiditates(evaluated, 4)

    organisms[0].im.show()

if __name__ == "__main__":
    cli()
