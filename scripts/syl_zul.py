#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the Zulu rule-based syllabification algorithm.
"""
from __future__ import unicode_literals, division, print_function #Py2

__author__ = "Daniel van Niekerk"
__email__ = "dvn.demitasse@gmail.com"

import sys

from syl_xho import NguniSyllabifier, main

if __name__ == "__main__":
    main(NguniSyllabifier)

