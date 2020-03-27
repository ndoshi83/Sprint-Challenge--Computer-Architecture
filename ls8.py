#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) != 2:
    print('Incorrect file name: ls8.py examples/filename')
    sys.exit(1)

fn = sys.argv[1]




cpu = CPU()

cpu.load(fn)
cpu.run()