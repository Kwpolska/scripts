#!/usr/bin/env python3
# Compare multiple files.
# Copyright © 2017, Chris Warrick.
# All rights reserved.
# Licensed under the 3-clause BSD license.

"""Compare multiple files."""

from sys import argv
from itertools import combinations

if len(argv) < 3:
    print("Usage: crossdiff.py FILENAME FILENAME [FILENAME [FILENAME...]]")
    exit(2)
else:
    f = argv[1:]

comb = set()
any_diff = False
for left, right in combinations(f, 2):
    if left == right:
        continue
    comb.add(frozenset([left, right]))
for left, right in comb:
    lt = open(left, "rb").read()
    rt = open(right, "rb").read()
    if lt.strip() != rt.strip():
        print("Files", left, "and", right, "differ")
        any_diff = True

exit(any_diff)
