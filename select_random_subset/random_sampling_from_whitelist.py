import argparse
import process_fastq
import sys
import gzip

MAX_READ_PAIR_DEFAULT = -1
#MAX_READ_PAIR_DEFAULT = 50000000

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()  

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-w", "--whitelist", action="store", default='whitelist_barcodes', type=str, dest="whitelist_file")
    parser.add_argument("-k", "--subsample_size", action="store", default=4000, type=int, dest="subsample_size")
    parser.add_argument("-i", "--in", action="store", default='-', type=str, dest="in_fastq")
    parser.add_argument("-o", "--out", action="store", default='stdout', type=str, dest="out_fastq")
    parser.add_argument("-s", "--seed", action="store", default=1334, type=int, dest="seed")
    parser.add_argument("-m", "--max_read_pairs", action="store", default=MAX_READ_PAIR_DEFAULT, type=int, dest="max_read_pair")    
    parser.add_argument("-p", "--stats_out_path", action="store", default='.', type=str, dest="stats_out_path")
    parser.add_argument("-v", "--verbose", action="store", default=True, type=bool, dest="verbose")   


    args = parser.parse_args()
    
    print(args)
    
    my_input = my_output = ''
    
    # Open in fastq
    if args.in_fastq == '-':
        my_input == sys.stdin
    elif args.in_fastq[-2:] == 'gz':
        my_input = gzip.open(args.in_fastq, 'rb')
    else:
        my_input = open(in_fastq, 'rb')
    
    # Open out fastq
    if args.out_fastq == '-':
        my_output == sys.stdout
    else:
        my_output == gzip.open(args.out_fastq, 'wb')
    
    # Open whitelist
    if args.out_fastq == '-':
        my_output == sys.stdout
    else:
        my_output == gzip.open(args.out_fastq, 'wb')
    
    whitelist_file = open(args.whitelist_file, 'rb')
    
    my_process_fastq = process_fastq.ProcessFastQBarCodes(
                            barcode_whitelist_file=whitelist_file,
                            stats_path=args.stats_out_path,
                            subset_size=args.subsample_size,
                            random_seed=args.seed,
                            max_read_pairs=-1,
                            verbose=True)
