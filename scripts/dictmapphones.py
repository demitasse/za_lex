#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Map phones in simple dictionary using simple mapping
   file. Dictionaries via STDIO, with mapping file and options as
   arguments.
"""
import sys, os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('mapfile', metavar='MAPFILE', type=str, help="File containing phone mapping.")
    parser.add_argument('--mapreverse', action='store_true', help="Apply mapping file in reverse.")
    args = parser.parse_args()

    phmap = {}
    with open(args.mapfile, encoding="utf-8") as infh:
        for line in infh:
            a, b = line.split()
            if args.mapreverse:
                a, b = (b, a)
            phmap[a] = b

    warnings = set()
    for line in sys.stdin:
        fields = line.split()
        word = fields[0]
        phones = fields[1:]
        newphones = []
        for ph in phones:
            try:
                newphones.append(phmap[ph])
            except KeyError:
                if not ph in warnings:
                    print("WARNING: Did not map /{}/".format(ph), file=sys.stderr)
                    #print("\t{}".format(line.strip()), file=sys.stderr)
                    warnings.add(ph)
                newphones.append(ph)
            if "\t" in line:
                sep = "\t"
            else:
                sep = " "
        print("{}{}{}".format(word, sep, " ".join(newphones)))
