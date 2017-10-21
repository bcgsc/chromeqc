# parameters:
# how many reads to burn-in
# how many reads-pairs to process from fastq

import gzip
import matplotlib.pyplot as plt
import sys
import os
import numpy as np


class ProcessFastQBarCodes:
    """

    """
    STAT_SAVE_FREQUENCY = 1000000  # how often to save stats (number of pair-end reads)
    PROGRESS_PRINT_FREQUENCY = 100000  # how often to print progress (number of pair-end reads)
    BARCODE_SIZE = 16
    TRIM_SIZE = BARCODE_SIZE + 6

    def __init__(self, barcode_whitelist_file, stats_path='.',
                 subset_size=4000, random_seed=1337, max_read_pairs=-1, verbose=True):
        """
        Args:
            barcode_whitelist_file:
            stats_path:
            subset_size:
            random_seed:
            max_read_pairs:
            verbose:
        """
        self.whitelist_barcodes_list = []
        self.whitelist_barcodes_count = {}  # dict of the white listed barcodes mapped to read-pair count
        self.unmatched_barcodes_count = {}
        self.subset_barcodes_count = {}  # barcodes randomly sampled from the whitelist
        self.num_unmatched_barcodes = 0
        self.read_pairs_processed = 0
        self.verbose = verbose
        self.stats_path = stats_path
        self.max_read_pairs=-1
        self.subset_size = subset_size
        self.random_seed = random_seed
        # read the white list
        self._read_whitelist_barcodes(barcode_whitelist_file)
        self._create_barcode_subset()

    def eprint(self, *args, **kwargs):
        if self.verbose:
            print(*args, file=sys.stderr, **kwargs)

    def _read_whitelist_barcodes(self, barcode_file):
        """
        Read the white listed barcodes. and creates a randomly sampled list
        Args:
            barcode_file: whitelist barcodes are extracted from longranger tool:
            longranger-2.1.6/longranger-cs/2.1.6/tenkit/lib/python/tenkit/barcodes/4M-with-alts-february-2016.txt
        """
        self.eprint('Reading white listed barcodes ...')

        do_check_if_bytes = True
        for line in barcode_file.readlines():
            if do_check_if_bytes:
                try:
                    line = line.decode()  # when input is a gzip file
                except AttributeError:
                    do_check_if_bytes = False

            barcode = line[:-1]
            if barcode in self.whitelist_barcodes_count:
                self.eprint('Warning: duplicate barcode found in the whitelist: {}'.format(barcode))
            self.whitelist_barcodes_list.append(barcode) # todo: is this efficient?
            self.whitelist_barcodes_count[barcode] = 0

        self.eprint('[Done]. read {} records'.format(len(self.whitelist_barcodes_count)))

    def _create_barcode_subset(self):
        np.random.seed(self.random_seed)
        if self.subset_size <= 0 or self.subset_size >= len(self.whitelist_barcodes_list):
            random_indices = range(len(self.whitelist_barcodes_list))  # just take the entire list
        else:
            random_indices = np.random.choice(len(self.whitelist_barcodes_list), size=self.subset_size, replace=False)
        self.subset_barcodes_count = {self.whitelist_barcodes_list[i]: 0 for i in random_indices}

    def process_fastq(self, file_in, file_out):
        """
        Processes a fastq file and outputs randomly sampled reads
        Args:
            file_in: input file object (or stream) to get the fastq reads from
            file_out: output file object (or stream) to write the sampled fastq reads to

        Returns: None
        """

        self.eprint('Reading fastq file...')
        read_index = 0
        prev_read_name = None
        do_output_read = False
        do_check_if_bytes = True
        while True:
            try:
                read_name_raw = file_in.readline()
                read_seq_raw = file_in.readline()
                read_line3_raw = file_in.readline()
                read_qual_raw = file_in.readline()

                if do_check_if_bytes:
                    try:
                        read_name_raw = read_name_raw.decode()
                        read_seq_raw = read_seq_raw.decode()
                        read_line3_raw = read_line3_raw.decode()
                        read_qual_raw = read_qual_raw.decode()
                    except AttributeError:
                        do_check_if_bytes = False  # don't check not anymore

                if read_name_raw == '':  # eof
                    raise EOFError

                is_read1 = read_index % 2 == 0
                read_name = read_name_raw.split(' ')[0]
                if is_read1:
                    do_output_read = False
                    read_barcode = read_seq_raw[:self.BARCODE_SIZE]
                    barcode_read_count = self.whitelist_barcodes_count.get(read_barcode, -1)
                    if barcode_read_count != -1:
                        # the read barcode was in the white list
                        self.whitelist_barcodes_count[read_barcode] = barcode_read_count + 1
                        subset_read_count = self.subset_barcodes_count.get(read_barcode, -1)
                        if subset_read_count != -1:
                            # the read barcode was in the white list subset
                            do_output_read = True
                            self.subset_barcodes_count[read_barcode] = subset_read_count + 1
                            # trim the read to remove the barcode and random 6mer
                            read_seq_raw = read_seq_raw[self.TRIM_SIZE:]
                            read_qual_raw = read_qual_raw[self.TRIM_SIZE:]
                    else:
                        # the read barcode didn't match the white list
                        self.unmatched_barcodes_count[read_barcode] = self.unmatched_barcodes_count.get(read_barcode, 0) + 1
                        self.num_unmatched_barcodes += 1
                else:  # read2
                    if read_name != prev_read_name:
                        self.eprint("ERROR: Mismatched reads at read index {:,}".format(read_index))
                        break

                if file_out is not None and do_output_read:
                    read_name_raw = '@{}-1_{} BX:Z:{}-1\n'.format(read_barcode, read_name_raw[1:-1], read_barcode)
                    file_out.write(read_name_raw)
                    file_out.write(read_seq_raw)
                    file_out.write(read_line3_raw)
                    file_out.write(read_qual_raw)

                prev_read_name = read_name
                read_index += 1
                self.read_pairs_processed = read_index // 2

                if read_index % (self.PROGRESS_PRINT_FREQUENCY * 2) == 0:
                    self.print_progress()

                if read_index % (self.STAT_SAVE_FREQUENCY * 2) == 0:
                    self.save_stats()

                if self.max_read_pairs > 0 and self.read_pairs_processed >= self.max_read_pairs:
                    break

            except EOFError:
                self.eprint("[Done]: EOF")
                break

        self.print_progress()
        self.save_stats()

    def print_progress(self):
        self.eprint("Processed {:,} pair of reads. found {:,}({}%) unmatched barcodes ({:,} unique)".format(
            self.read_pairs_processed,
            self.num_unmatched_barcodes,
            round(100.0 * self.num_unmatched_barcodes / self.read_pairs_processed, 1),
            len(self.unmatched_barcodes_count)))

    def save_stats(self):
        self.eprint("Saving stats")
        # create histograms
        self.save_stats_of_counts(self.subset_barcodes_count,
                                  filename_prefix=os.path.join(self.stats_path, 'subset_barcodes'),
                                  title='population count for subset barcodes for {:,} read pairs'.
                                  format(self.read_pairs_processed))
        self.save_stats_of_counts(self.whitelist_barcodes_count,
                                  filename_prefix=os.path.join(self.stats_path, 'whitelist_barcodes'),
                                  title='population count for white-list barcodes for {:,} read pairs'.
                                  format(self.read_pairs_processed))
        self.save_stats_of_counts(self.unmatched_barcodes_count,
                                  filename_prefix=os.path.join(self.stats_path, 'unmatched_barcodes'),
                                  title='population counts for unmatched barcodes for {:,} read pairs'.
                                  format(self.read_pairs_processed))


    @staticmethod
    def save_stats_of_counts(dict_counts, filename_prefix, title ='', remove_zeros=True):
        sorted_list = [x for x in sorted(list(dict_counts.items()), key=lambda x: x[1], reverse=True) if x[1] > 0]
        if remove_zeros:
            sorted_list = [x for x in sorted_list if x[1] > 0]

        max_count = max([x[1] for x in sorted_list])
        min_count = min([x[1] for x in sorted_list])
        count_hist = [0] * (max_count - min_count + 1)
        for x in sorted_list:
            count_hist[x[1] - min_count] += 1

        # output the population count histograms
        with open(filename_prefix + "_population_counts.tsv", "w") as f:
            f.write('reads_in_population\tpopulation_count\n')
            f.write('\n'.join(['{}\t{}'.format(i+min_count, j) for i, j in enumerate(count_hist)]))

        # output top 100 size tags
        with open(filename_prefix + "_top_barcodes.tsv", "w") as f:
            f.write('barcode\tread_count\n')
            f.write('\n'.join(['{}\t{}'.format(x[0], x[1]) for x in sorted_list[:100]]))

        plt.style.use('seaborn-whitegrid')
        plt.plot(range(min_count, max_count + 1), count_hist)
        plt.xlabel('population')
        plt.ylabel('#per population')
        plt.title(title)
        plt.savefig(filename_prefix + ".pdf")
        plt.clf()


if __name__ == '__main__':
    barcode_filename = 'data/barcode.txt'
    fastq_filename = 'data/read-RA_si-GAGTTAGT_lane-001-chunk-0002.fastq.gz'

    with open(barcode_filename, 'r') as f:
        p = ProcessFastQBarCodes(barcode_whitelist_file=f, max_read_pairs=-1, stats_path='select_random_subset/')
        with gzip.open(fastq_filename, 'r') as file_in:
            p.process_fastq(file_in=file_in, file_out=sys.stdout)


"""
@BARCODE-1_...
adapter dimer. p5-template-p7.
"""