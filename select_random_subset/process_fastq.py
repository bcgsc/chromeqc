# parameters:
# how many reads to burn-in
# how many reads-pairs to process from fastq

import gzip
# from Bio import SeqIO

# read the white listed barcodes (
# barcodes are extracted from longranger tool:
# longranger-2.1.6/longranger-cs/2.1.6/tenkit/lib/python/tenkit/barcodes/4M-with-alts-february-2016.txt
barcodes = {}
print("Reading barcodes ...")
with open("data/barcode.txt", "r") as f:
    for line in f.readlines():
        barcode = line[:-1]
        if barcode in barcodes:
            print("duplicate barcode: {}", barcode)
        barcodes[barcode] = 0
print("[Done]. {} records".format(len(barcodes)))

# process the fastq file
unmatched_barcodes = {}
num_unmatched_barcodes = 0
print("Reading fastq file ...")
read_index = 0
prev_read_name = None
with gzip.open('data/read-RA_si-GAGTTAGT_lane-001-chunk-0002.fastq.gz') as fq:
    while True:
        try:
            read_name = fq.readline().decode("utf-8")[:-1].split(' ')[0]
            read_seq = fq.readline().decode("utf-8")[:-1]
            _ = fq.readline()
            read_qual = fq.readline().decode("utf-8")[:-1]
            is_read1 = read_index % 2 == 0
            if is_read1:
                read_barcode = str(read_seq[:16])
                read_barcode_count = barcodes.get(read_barcode, -1)
                if read_barcode_count == -1:
                    unmatched_barcodes[read_barcode] = unmatched_barcodes.get(read_barcode, 0) + 1
                    num_unmatched_barcodes += 1
                else:
                    barcodes[read_barcode_count] = read_barcode_count + 1
            else: # read2
                if read_name != prev_read_name:
                    print("Mismatched reads at read index {}".format(read_index))
            prev_read_name = read_name
            read_index += 1
            if read_index % 100000 == 0:
                print("Processed {} reads. found {} unmatched barcodes ({} unique)".format(
                    read_index, num_unmatched_barcodes, len(unmatched_barcodes)))
                break
        except EOFError:
            pass
print("Total {} reads. found {} unmatched barcodes ({} unique)".format(
    read_index, num_unmatched_barcodes, len(unmatched_barcodes)))


