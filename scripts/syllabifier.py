#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys

class Syllabifier(object):
    def __init__(self, phonemeset):
        self.__dict__.update(phonemeset)

    def is_vowel(self, phonename):
        return "vowel" in self.phones[phonename]

    def is_syllabic(self, phonename):
        return "syllabic" in self.phones[phonename]

    def _vowelindices(self, phones):
        return [i for i, ph in enumerate(phones) if self.is_vowel(ph)]

    def syllabify(self, phones):
        raise NotImplementedError

def main(SylCls):
    import json
    import argparse

    import dictconv
    
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('phonesetfile', metavar='PHONESETFILE', type=str, help="File containing the phoneme set (json utf-8).")
    parser.add_argument('--oformat', metavar='OUTPUTFORMAT', default=dictconv.DEF_OUTFORMAT, help="output format (flat|nested)")
    parser.add_argument('--defstresstone', metavar='DEFSTRESSTONE', default=dictconv.DEFSTRESSTONE, help="default stress/tone")
    args = parser.parse_args()

    #load phoneset
    with open(args.phonesetfile, encoding="utf-8") as infh:
        phoneset = json.load(infh)
    syllabifier = SylCls(phoneset)

    for line in sys.stdin:
        fields = line.strip().split()
        word = fields[0]
        pronun = fields[1:]
        
        syls = syllabifier.syllabify(pronun)
        sylspec = [str(len(syl)) for syl in syls]
        stresspat = args.defstresstone * len(sylspec)

        if args.oformat == "flat":
            print(dictconv.print_flat(word, "None", stresspat, sylspec, pronun, None))
        elif args.oformat == "nested":
            print(dictconv.print_nested(word, "None", stresspat, sylspec, pronun, phoneset, args.defstresstone, None))
        else:
            raise Exception("Invalid output format specified")
