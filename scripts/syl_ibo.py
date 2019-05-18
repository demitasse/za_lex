#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the Igbo rule-based syllabification algorithm.
"""

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys

from syllabifier import Syllabifier, main


class IgboSyllabifier(Syllabifier):
    def syllabify(self, phones):
        def breakcluster(cluster):
            if not cluster:
                bounds.append(ci) #Always V.V
            elif len(cluster) == 1:
                bounds.append(ci) #Always V.CV (open syllables)
            elif len(cluster) == 2:
                if self.is_syllabic(cluster[0]):
                    #V.sC.CV
                    bounds.append(ci)
                    bounds.append(ci + 1)
                    return
                #DEFAULT: V.CCV
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster),"".join(phones)), file=sys.stderr)
                bounds.append(ci)
            else:
                print("syllabify(): WARNING: unexpectedly long consonant cluster found: '{}' in '{}'"\
                      .format("".join(cluster), "".join(phones)), file=sys.stderr)            
                if self.is_syllabic(cluster[0]):
                    #V.sC.*V
                    bounds.append(ci) 
                    bounds.append(ci + 1)
                else:
                    #V.*V (generally: prefer open syllables)
                    bounds.append(ci)                

        v_inds = self._vowelindices(phones)
        bounds = []
        if v_inds:
            #Onset cluster (syllabic consonant?)
            if not 0 in v_inds:
                span = phones[0:v_inds[0]+1]
                cluster = phones[0:v_inds[0]]
                ci = 0
                breakcluster(cluster)
                bounds.pop(0)
            #Other clusters
            for i, j in zip(v_inds, v_inds[1:]):
                span = phones[i:j+1]
                cluster = span[1:-1]
                ci = i+1
                breakcluster(cluster)
            #Word-final cluster?
            cluster = phones[v_inds[-1]+1:]
            if cluster:
                ci = v_inds[-1]+1
                if len(cluster) == 1 and self.is_syllabic(cluster[0]):
                    bounds.append(ci)
                else:
                    print("syllabify(): WARNING: word-final cluster not considered valid: '{}' in '{}'".format("".join(cluster), "".join(phones)), file=sys.stderr)
        else:
            print("syllabify(): WARNING: no vowels found in word '{}'".format("".join(phones)), file=sys.stderr)
                
        #Convert sylbounds to syllable lists
        sylls = []
        startbound = 0
        for bound in bounds:
            sylls.append(phones[startbound:bound])
            startbound = bound
        sylls.append(phones[startbound:])
        return sylls

if __name__ == "__main__":
    main(IgboSyllabifier)
