#!/usr/bin/python

import sys

print 'Then command line arguments are: '
for (i, v) in enumerate(sys.argv):
    print i, "\t", v

