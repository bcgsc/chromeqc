#!/usr/bin/env python3
import sys
# Author: Emre Erhan
# Take a sam file in stdin with the barcode in the read name and the barcode length as an input parameter,
# and output a sam file to stdout with the barcodes removed from the read name, and in the BX tag at the end of any line.
# Example usage:
# cat sam_file.sam | python3 minimap2_format.py 18


def format_sam(barcode_length):
    for read in sys.stdin.readlines():
        # Skip header
        if read[0] == "@":
            continue
        parsed_line = read.rstrip().split('\t')
        read_name = parsed_line[0]
        barcode = read_name[:barcode_length]
        new_name = read_name[barcode_length + 1:]
        new_line = new_name + "\t".join(parsed_line[1:]) + "\t BX:Z:{}".format(barcode)
        print(new_line)


def main():
    barcode_length = int(sys.argv[1])
    format_sam(barcode_length)


if __name__ == "__main__":
    main()
