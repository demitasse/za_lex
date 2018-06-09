#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the Tswana rule-based syllabification algorithm.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys

from syl_sot import SothoSyllabifier, main

class TswanaSyllabifier(SothoSyllabifier):
    def is_valid_CC(self, cluster, consider_foreign=True):
        """ We only explicitly check for Cw
        """
        if cluster[1] == self.phone_w and any(isf(cluster[0]) for isf in [self.is_plosivelike, self.is_fricative, self.is_nasal, self.is_approximant, self.is_trill]):
            #print("CC1:", "/".join(cluster).encode("utf-8"), sep="\t", file=sys.stderr)
            return True
        elif consider_foreign and cluster in self.clusters_foreign_CC_onsets:
            #print("CC5:", "/".join(cluster).encode("utf-8"), sep="\t", file=sys.stderr)
            print("syllabify(): WARNING: foreign onset cluster: '{}'".format("".join(cluster)).encode("utf-8"), file=sys.stderr)
            return True
        return False


if __name__ == "__main__":
    main(TswanaSyllabifier)
