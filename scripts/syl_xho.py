#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the Xhosa rule-based syllabification algorithm.
"""

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys

from syllabifier import Syllabifier, main

class NguniSyllabifier(Syllabifier):
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

    def is_homorganic(self, phn1, phn2):
        place1 = set([e for e in self.phones[phn1] if e.startswith("pl_")])
        place2 = set([e for e in self.phones[phn2] if e.startswith("pl_")])
        return bool(place1.intersection(place2))

    def is_valid_CC(self, cluster, consider_foreign=True):
        """Mostly from the book by Philip Hoole (see below)..
        """
        if cluster[1] == self.phone_w and any(isf(cluster[0]) for isf in [self.is_plosivelike, self.is_fricative, self.is_nasal, self.is_approximant]):
            #print("CC1:", "/".join(cluster), sep="\t", file=sys.stderr)
            return True
        if cluster[0] in self.phones_nN and (self.is_plosivelike(cluster[1]) or self.is_fricative(cluster[1])) and self.is_homorganic(cluster[0], cluster[1]):
            #print("CC2:", "/".join(cluster), sep="\t", file=sys.stderr)
            return True
        if cluster[0] == self.phone_J and self.is_homorganic(cluster[0], cluster[1]):
            #print("CC3:", "/".join(cluster), sep="\t", file=sys.stderr)
            return True
        if cluster[0] == self.phone_m and cluster[1] in self.phones_valid_mC_consonants:
            #print("CC4:", "/".join(cluster), sep="\t", file=sys.stderr)
            return True
        elif consider_foreign and cluster in self.clusters_foreign_CC_onsets:
            #print("CC5:", "/".join(cluster), sep="\t", file=sys.stderr)
            print("syllabify(): WARNING: foreign onset cluster: '{}'".format("".join(cluster)), file=sys.stderr)
            return True
        return False

    def _vowelindices(self, phones):
        return [i for i, ph in enumerate(phones) if self.is_vowel(ph)]

    def syllabify(self, phones):
        """Syllabification algorithm for Nguni languages based on notes
           pp. 349 of "Consonant Clusters and Structural Complexity"
           by Philip Hoole
        """
        def breakcluster(cluster):
            if not cluster:
                print("syllabify(): WARNING: VV context found in '{}'".format("".join(phones)), file=sys.stderr)
                bounds.append(ci) #Always V.V
            elif len(cluster) == 1:
                bounds.append(ci) #Always V.CV (open syllables)
            elif len(cluster) == 2:
                if self.is_valid_CC(cluster):
                    bounds.append(ci) #V.CCV
                    return
                if self.is_syllabic(cluster[0]):
                    #V.N.CV
                    bounds.append(ci)
                    bounds.append(ci + 1)
                    return
                if cluster in self.clusters_foreign_CC_not_onsets:
                    print("syllabify(): WARNING: foreign cluster was split: '{}' in '{}'".format("".join(cluster), "".join(phones)), file=sys.stderr)
                    bounds.append(ci + 1) #VC.CV
                    return
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster),"".join(phones)), file=sys.stderr)
                bounds.append(ci) #V.CCV
            elif len(cluster) == 3:
                if cluster[2] == self.phone_w:
                    if self.is_valid_CC(cluster[:2], consider_foreign=False):
                        bounds.append(ci) #V.CCWV
                        return
                if self.is_syllabic(cluster[0]) and self.is_valid_CC(cluster[1:]):
                    #V.N.CWV
                    bounds.append(ci) 
                    bounds.append(ci + 1)
                    return
                if cluster in self.clusters_foreign_CCC_onsets:
                    print("syllabify(): WARNING: foreign syllable cluster: '{}' in '{}'".format("".join(cluster), "".join(phones)), file=sys.stderr)
                    bounds.append(ci) #V.CCCV
                if cluster[1:] in self.clusters_foreign_CC_onsets:
                    print("syllabify(): WARNING: foreign syllable cluster: '{}' in '{}'".format("".join(cluster), "".join(phones)), file=sys.stderr)
                    bounds.append(ci + 1) #VC.CCV  (foreign)
                    return
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster), "".join(phones)), file=sys.stderr)
                bounds.append(ci) #V.CCCV
            elif len(cluster) == 4:
                if cluster[-1] == self.phone_w and self.is_syllabic(cluster[0]) and self.is_valid_CC(cluster[1:3], consider_foreign=False):
                    #V.N.CCWV
                    bounds.append(ci)
                    bounds.append(ci + 1)
                    return
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster), "".join(phones)), file=sys.stderr)                
                bounds.append(ci) #V.CCCCV
            else:
                print("syllabify(): WARNING: onset cluster not considered valid: '{}' in '{}'".format("".join(cluster), "".join(phones)), file=sys.stderr)
                bounds.append(ci) #V.*V (generally: prefer open syllables)

        v_inds = self._vowelindices(phones)
        bounds = []
        if v_inds:
            #Onset cluster (syllabic nasal?)
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
    main(NguniSyllabifier)

