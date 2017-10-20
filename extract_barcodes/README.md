# Usage
```
chmod +x extract_barcodes/extract_barcodes.awk
zcat interleaved_paired_end.fastq.gz | extract_barcodes/extract_barcodes.awk | less
```

The commandline flags are:
```
c: Oppress writing the barcode to the comment field after the readname
n: Oppress prepending the barcode the readname
```

For example:
```
zcat interleaved_paired_end.fastq.gz | extract_barcodes/extract_barcodes.awk -- -c | less
```
or:
```
zcat interleaved_paired_end.fastq.gz | extract_barcodes/extract_barcodes.awk -- -n | less
```
