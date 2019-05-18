#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Apply a diacritic restoration model
"""

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

class Diacritiser(object):
    def diacritise(self, line):
        raise NotImplementedError

    def __call__(self, line):
        return self.diacritise(line)

if __name__ == "__main__":
    import sys, argparse, pickle
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('modelfn', metavar='MODELFN', type=str, default=None, help="Load from model file (pickle format)")
    args = parser.parse_args()

    with open(args.modelfn, "rb") as infh:
        d = pickle.load(infh)
    
    for line in sys.stdin:
        line = line.strip()
#        try:
        print(d.diacritise(line))
        # except Exception as e:
        #     print("CONVERSION FAILED: '{}'".format(line), file=sys.stderr)
        #     print(str(e), file=sys.stderr)
