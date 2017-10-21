#!/usr/bin/env python

from __future__ import division
import sys
import getopt

MATCH = "match"
OFF_BY_ONE = "off by one"
NO_MATCH = "no match"

def get_whitelisted_barcodes(barcode_path):
    '''
    Retrieve the whitelisted barcodes from file
    '''
    whitelisted_barcodes = []
    with open(barcode_path,'r') as barcode_file:
        for line in barcode_file:
            barcode = line.rstrip() # Get rid of any newline characters
            whitelisted_barcodes.append(barcode) 
    return whitelisted_barcodes

def get_barcodes_from_fastq(fastq_path):
    '''
    Retrieves the barcodes from the name line of each read in the FASTQ file
    ''' 
    barcodes = []
    with open(fastq_path,'r') as fastq_file:
        for line in fastq_file:
            if len(line) > 0 and line[0] == "@":
                # Get the indices of colon characters in the line
                colon_indices = [pos for pos, char in enumerate(line) if char == ':']
                # Get the index of the last colon in the string
                colon_index = colon_indices[-1]
                # Get the indices of the dash characters in the line
                dash_indices = [pos for pos, char in enumerate(line) if char == '-']
                # Get the index of the last dash character in the line
                dash_index = dash_indices[-1]
                # Get the barcode from the line
                barcode = line[colon_index+1:dash_index]
                if len(barcode) == 16:
                    barcodes.append(barcode)
    return barcodes

def matched_off_by_one(barcode,whitelisted_barcodes):
    '''
    Determines whether the specified barcode matches any of the whitelisted barcodes when exactly one of the bases
    is permuted to the other three possibilities 
    '''
    # The list of other bases for a given base
    other_bases_dict = {'A': ['C','T','G'], 'C': ['A','T','G'], 'G': ['A','C','T'], 'T': ['A','C','G']}
    # Turn the barcode strng into a list for easy modification
    barcode_list = list(barcode)
    # Check each base of the barcode
    for i in range(len(barcode_list)):
        # Make a copy of the original barcode list
        temp_list = list(barcode_list) 
        original_base = barcode_list[i]
        other_bases = other_bases_dict[original_base]
        # Check whether the barcode exists in the whitelisted barcode list if a single base is permuted
        for other_base in other_bases:
            temp_list[i] = other_base
            mod_barcode = "".join(temp_list)
            if mod_barcode in whitelisted_barcodes:
                return True
    return False

def examine_barcodes(barcodes,whitelisted_barcodes):
    '''
    Determine the number of barcodes that match known whitelisted barcodes, the number that are off by one, and
    the number that don't match at all
    '''
    barcode_stats = {MATCH:0, OFF_BY_ONE:0, NO_MATCH:0}
    for barcode in barcodes:
        if barcode in whitelisted_barcodes:
            barcode_stats[MATCH] += 1
        elif matched_off_by_one(barcode,whitelisted_barcodes):
            barcode_stats[OFF_BY_ONE] += 1
        else:
            barcode_stats[NO_MATCH] += 1
    num_barcodes = len(barcodes)
    print("Number of barcodes: %d" % (num_barcodes))
    for stat in barcode_stats:
        barcode_stats[stat] = barcode_stats[stat]/num_barcodes 
    return barcode_stats

def write_barcode_stats(barcode_stats, output_path):
    '''
    Print the results of the barcode whitelist cross reference and write the output to a file
    '''
    match_line = "Matches: %f" % (barcode_stats[MATCH])
    off_by_one_line = "Off by one: %f" % (barcode_stats[OFF_BY_ONE])
    no_match_line = "No match: %f" % (barcode_stats[NO_MATCH])
    lines = [match_line,off_by_one_line,no_match_line]

    with open(output_path,'w') as output_file:
        for line in lines:
            print(line)
            output_file.write(line)
            output_file.write('\n') 

def test():
    no_match_bc = "A" * 16
    off_by_one_bc = "CGACACGGTATGGGCC" # The A between the two T's is the error; there should be three T's
    matching_barcode = "CGACACGGTTTGGGCC"
    barcodes = [no_match_bc,off_by_one_bc,matching_barcode]
    return barcodes

def main(argv):
    help_message = "Description: Cross references barcodes with known whitelisted barcodes to determine\n" \
                 + "             which match exactly, which are off by one base, and which have no match\n" \
                 + "             otherwise."
    usage_message = "Usage: %s [-h help and usage] [-f input FASTQ file] [-b whitelisted barcodes]\n"% (sys.argv[0]) \
                  + "                                      [-o output path for stats]"

    options = "htf:b:o:"

    try:
        opts, args = getopt.getopt(sys.argv[1:],options)
    except getopt.GetoptError:
        print("Error: unable to read command line arguments.")
        sys.exit(1)

    if len(sys.argv) == 1:
        print(help_message)
        print(usage_message)
        sys.exit()

    fastq_path = None
    barcode_path = None
    output_path = None
    do_test = False

    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            print(usage_message)
            sys.exit(0)
        elif opt == '-f':
            fastq_path = arg
        elif opt == '-b':
            barcode_path = arg
        elif opt == '-o':
            output_path = arg
        elif opt == '-t':
            do_test = True

    opts_incomplete = False

    if fastq_path is None and not do_test:
        print("Error: please provide a FASTQ file.")
        opts_incomplete = True
    if barcode_path is None:
        print("Error: please provide the whitelisted barcode file.")
        opts_incomplete = True
    if output_path is None:
        print("Error: please provide an output path.")
        opts_incomplete = True

    if opts_incomplete:
        print(usage_message)
        sys.exit(1)

    whitelisted_barcodes = get_whitelisted_barcodes(barcode_path)
    if not do_test:
        barcodes = get_barcodes_from_fastq(fastq_path)
    else:
        barcodes = test()    
    barcode_stats = examine_barcodes(barcodes,whitelisted_barcodes)
    write_barcode_stats(barcode_stats, output_path)

if __name__ == "__main__":
    main(sys.argv)
