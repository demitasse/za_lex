#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the Sotho rule-based syllabification algorithm.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys

from syllabifier import Syllabifier, main

class SothoSyllabifier(Syllabifier):

    def is_affricate(self, phonename):
        return "mn_affricate" in self.phones[phonename]

    def is_fricative(self, phonename):
        return "mn_fricative" in self.phones[phonename]

    def is_plosive(self, phonename):
        return "mn_plosive" in self.phones[phonename]

    def is_click(self, phonename):
        return "mn_click" in self.phones[phonename]

    def is_plosivelike(self, phonename):
        return self.is_plosive(phonename) or self.is_affricate(phonename) or self.is_click(phonename)

    def is_nasal(self, phonename):
        return "mn_nasal" in self.phones[phonename]

    def is_approximant(self, phonename):
        return "mn_approximant" in self.phones[phonename]

    def is_trill(self, phonename):
        return "mn_trill" in self.phones[phonename]

    def _vowelindices(self, phones):
        return [i for i, ph in enumerate(phones) if self.is_vowel(ph)]

    def is_valid_CC(self, cluster, consider_foreign=True):
        """ We only explicitly check for Cw and Ch
        """
        if (cluster[1] == self.phone_w or cluster[1] == self.phone_hv) and any(isf(cluster[0]) for isf in [self.is_plosivelike, self.is_fricative, self.is_nasal, self.is_approximant, self.is_trill]):
            #print("CC1:", "/".join(cluster).encode("utf-8"), sep="\t", file=sys.stderr)
            return True
        elif consider_foreign and cluster in self.clusters_foreign_CC_onsets:
            #print("CC5:", "/".join(cluster).encode("utf-8"), sep="\t", file=sys.stderr)
            print("syllabify(): WARNING: foreign onset cluster: '{}'".format("".join(cluster)).encode("utf-8"), file=sys.stderr)
            return True
        return False

    def syllabify(self, phones):
        """ Basic Sotho syllabification...
        """
        def breakcluster(cluster):
            if not cluster:
                bounds.append(ci) #Always V.V
            elif len(cluster) == 1:
                bounds.append(ci) #Always V.CV (open syllables)
            elif len(cluster) == 2:
                if self.is_valid_CC(cluster):
                    bounds.append(ci) #V.CCV
                    return
                if self.is_syllabic(cluster[0]):
                    #V.sC.CV
                    bounds.append(ci)
                    bounds.append(ci + 1)
                    return
                if cluster in self.clusters_foreign_CC_not_onsets:
                    print("syllabify(): WARNING: foreign cluster was split: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)
                    bounds.append(ci + 1) #VC.CV
                    return
                #DEFAULT: V.CCV
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster),"".join(phones)).encode("utf-8"), file=sys.stderr)
                bounds.append(ci)
            elif len(cluster) == 3:
                if self.is_syllabic(cluster[0]):
                    if self.is_valid_CC(cluster[1:]): #V.sC.CWV
                        pass
                    else:
                        print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster[1:]), "".join(phones)).encode("utf-8"), file=sys.stderr)
                    bounds.append(ci) 
                    bounds.append(ci + 1)
                    return
                if cluster in self.clusters_foreign_CCC_onsets:
                    print("syllabify(): WARNING: foreign syllable cluster: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)
                    bounds.append(ci) #V.CCCV
                if cluster[1:] in self.clusters_foreign_CC_onsets:
                    print("syllabify(): WARNING: foreign syllable cluster: '{}' in '{}'".format("".join(cluster[1:]), "".join(phones)).encode("utf-8"), file=sys.stderr)
                    bounds.append(ci + 1) #VC.CCV  (foreign)
                    return
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)
                bounds.append(ci) #V.CCCV
            else:
                print("syllabify(): WARNING: unexpectedly long consonant cluster found: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)                
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
                    print("syllabify(): WARNING: word-final cluster not considered valid: '{}' in '{}'".format("".join(cluster), "".join(phones)).encode("utf-8"), file=sys.stderr)

        else:
            print("syllabify(): WARNING: no vowels found in word '{}'".format("".join(phones)).encode("utf-8"), file=sys.stderr)
                
        #Convert sylbounds to syllable lists
        sylls = []
        startbound = 0
        for bound in bounds:
            sylls.append(phones[startbound:bound])
            startbound = bound
        sylls.append(phones[startbound:])
        return sylls

if __name__ == "__main__":
    main(SothoSyllabifier)
