# parameters:
# how many reads to burn-in
# how many reads-pairs to process from fastq

import gzip
import matplotlib.pyplot as plt
# from Bio import SeqIO


class ProcessFastQBarCodes:
    """

    """
    def __init__(self):
        self.standard_barcodes = {}  # dict of the white listed barcodes mapped to read-pair count
        self.unmatched_barcodes = {}
        self.num_unmatched_barcodes = 0

    def read_standard_barcodes(self, barcode_filename):
        """
        Read the white listed barcodes.
        Args:
            barcode_filename: standard barcodes are extracted from longranger tool:
            longranger-2.1.6/longranger-cs/2.1.6/tenkit/lib/python/tenkit/barcodes/4M-with-alts-february-2016.txt
        """
        print('Reading standard (white listed) barcodes ...')
        with open(barcode_filename, 'r') as f:
            for line in f.readlines():
                barcode = line[:-1]
                if barcode in self.standard_barcodes:
                    print('duplicate barcode: {}', barcode)
                self.standard_barcodes[barcode] = 0

        print('[Done]. read {} records'.format(len(self.standard_barcodes)))

    def process_fastq(self, fastq_filename, max_read_pairs=100000):
        # process the fastq file
        print('Reading fastq file: {} ...'.format(fastq_filename))
        read_index = 0
        prev_read_name = None
        with gzip.open(fastq_filename) as fq:
            while True:
                try:
                    read_name = fq.readline().decode("utf-8")[:-1].split(' ')[0]
                    read_seq = fq.readline().decode("utf-8")[:-1]
                    _ = fq.readline()
                    read_qual = fq.readline().decode("utf-8")[:-1]
                    is_read1 = read_index % 2 == 0
                    if is_read1:
                        read_barcode = str(read_seq[:16])
                        read_barcode_count = self.standard_barcodes.get(read_barcode, -1)
                        if read_barcode_count == -1:
                            self.unmatched_barcodes[read_barcode] = self.unmatched_barcodes.get(read_barcode, 0) + 1
                            self.num_unmatched_barcodes += 1
                        else:
                            self.standard_barcodes[read_barcode] = read_barcode_count + 1
                    else: # read2
                        if read_name != prev_read_name:
                            print("Mismatched reads at read index {}".format(read_index))
                    prev_read_name = read_name
                    read_index += 1
                    if read_index % 100000 == 0:
                        print("Processed {} pair of reads. found {}({}%) unmatched barcodes ({} unique)".format(
                            read_index / 2,
                            self.num_unmatched_barcodes,
                            round(2 * 100.0 * self.num_unmatched_barcodes / read_index, 1),
                            len(self.unmatched_barcodes)))
                    if max_read_pairs > 0 and read_index/2 >= max_read_pairs:
                        break
                except EOFError:
                    pass

        print("Total: {} pair of reads. found {}({}%) unmatched barcodes ({} unique)".format(
            read_index / 2,
            self.num_unmatched_barcodes,
            round(2 * 100.0 * self.num_unmatched_barcodes / read_index, 1),
            len(self.unmatched_barcodes)))
        # create histograms
        self.plot_histogram_of_counts(self.standard_barcodes, filename_prefix='select_random_subset/standard_barcodes',
                                      title='population count for standard barcodes for {} read pairs'.format(max_read_pairs))
        self.plot_histogram_of_counts(self.unmatched_barcodes, filename_prefix='select_random_subset/unmatched_barcodes',
                                      title='population counts for unmatched barcodes for {} read pairs'.format(max_read_pairs))

    @staticmethod
    def plot_histogram_of_counts(dict_counts, filename_prefix, title = '', remove_zeros=True):
        sorted_list = [x for x in sorted(list(dict_counts.items()), key=lambda x: x[1], reverse=True) if x[1] > 0]
        if remove_zeros:
            sorted_list = [x for x in sorted_list if x[1] > 0]

        max_count = max([x[1] for x in sorted_list])
        min_count = min([x[1] for x in sorted_list])
        count_hist = [0] * (max_count - min_count + 1)
        for x in sorted_list:
            count_hist[x[1] - min_count] += 1

        filename_prefix
        with open(filename_prefix + "_population_counts.tsv", "w") as f:
            f.write('reads_in_population\tpopulation_count\n')
            f.write('\n'.join(['{}\t{}'.format(i+min_count, j) for i, j in enumerate(count_hist)]))

        # print("Top 100 size tags")
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
    p = ProcessFastQBarCodes()
    p.read_standard_barcodes(barcode_filename)
    p.process_fastq(fastq_filename, max_read_pairs=1000000)
