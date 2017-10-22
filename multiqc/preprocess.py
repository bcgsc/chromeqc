#!/usr/bin/env python

import numpy
import getopt
import sys

def main(argv):
    # Parse input and output files
    infile = ''
    outfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["infile=", "outfile="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit(0)
        elif opt == "-i":
            infile = arg
        elif opt == "-o":
            outfile = arg
        else:
            sys.exit(1)

    ls = []
    with open(infile, 'r') as f:
        f.readline()
        for line in f:
            info = line.split()
            size = int(info[2]) - int(info[1])
            ls.append(size)

    counts, bin_edges = numpy.histogram(ls, bins=numpy.logspace(1, 6))
    out = open(outfile, 'w')
    for i in range(len(counts)):
        out.write(str(bin_edges[i]) + "," + str(counts[i]) + '\n')
    
    out.close()

if __name__ == "__main__":
    main(sys.argv[1:])

