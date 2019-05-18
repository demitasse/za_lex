#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the Zulu rule-based syllabification algorithm.
"""

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys

from syl_xho import NguniSyllabifier, main

if __name__ == "__main__":
    main(NguniSyllabifier)

