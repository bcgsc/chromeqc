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
    parser.add_argument("-w", "--whitelist", action="store", default='whitelist_barcodes', type=str, dest="whitelist_path")
    parser.add_argument("-s", "--subsample_size", action="store", default=4000, type=int, dest="subsample_size")
    parser.add_argument("-i", "--in", action="store", default='-', type=str, dest="in_fastq", nargs='+')
    parser.add_argument("-o", "--out", action="store", default='stdout', type=str, dest="out_fastq")
    parser.add_argument("-r", "--random_seed", action="store", default=1334, type=int, dest="seed")
    parser.add_argument("-m", "--max_read_pairs", action="store", default=MAX_READ_PAIR_DEFAULT, type=int, dest="max_read_pair")    
    parser.add_argument("-p", "--stats_out_path", action="store", default='.', type=str, dest="stats_out_path")
    parser.add_argument("-v", "--verbose", action='store_true', dest="verbose")   


    args = parser.parse_args()
    
    if args.verbose:
        print(args, file=sys.stderr)
    
    # Open whitelist
    whitelist_file = ''
    if args.whitelist_path[-2:] == 'gz':
        whitelist_file = gzip.open(args.whitelist_path, 'rb')
    else:
        whitelist_file = open(args.whitelist_path, 'rb')

    my_process_fastq = process_fastq.ProcessFastQBarCodes(
                            barcode_whitelist_file=whitelist_file,
                            stats_path=args.stats_out_path,
                            subset_size=args.subsample_size,
                            random_seed=args.seed,
                            max_read_pairs=args.max_read_pair,
                            verbose=args.verbose)

    # Open output fastq
    if args.out_fastq in {'stdout', '-'}:
        my_output = sys.stdout
    else:
        my_output = gzip.open(args.out_fastq+'.gz', 'wb+')
    
    # Open input fastq
    if args.in_fastq[0] == '-':
        my_process_fastq.process_fastq(file_in=sys.stdin, file_out=my_output)
    else:
        for input_path in args.in_fastq:
            if input_path[-2:] == 'gz':
                input_file = gzip.open(input_path, 'rb')
            else:
                input_file = open(input_path, 'rb')
            my_process_fastq.process_fastq(file_in=input_file, file_out=my_output)
            input_file.close()
    my_output.close()
