---
title: 'ChromeQC: Summarize sequencing library quality of 10x Genomics Chromium linked reads'
author: [Shaun D Jackman, Justin Chu, Emre Erhan, Nikka Keivanfar, Sean La, Swapna Menon, Tatyana Mozgacheva, Baraa Orabi, Chen Yang, Hamid Younesy]
affiliation: [University of British Columbia; Simon Fraser University] 
bibliography: paper.bib
csl: paper.csl
rangeDelim: "&ndash;"
figPrefix: "Fig."
tblPrefix: ["Table", "Tables"]
---

# Abstract

# Introduction
10x Genomics Chromium sequencing is long range information sequencing library preparation toolkit. Every few DNA molecules (~100K bp) will have a unique 16 nucleotides long barcode mixed with them. These molecules are then sequenced with Illumina short paired-end sequencing. A molecule is expected to have a uniform distribution of locations of the reads covering it.

Quality control (QC) for sequencing data is done to assess whether the sequencing experiment has been performed successfully or not. One popular QC tool for Illumina reads is FastQC which gathers basic information such as base qualities, sequence distribution, or GC content and reports that in quick manner. However, FastQC does not provide QC of aspects that are specific to the long range reads of Chromium.

For that, 10x Genomics provide their own analysis tool, Loupe. Loupe provides QC summary of the sequencing data alongside phasing information, SNP calling, and structural variants discovered. When analyzing [some number]x coverage fastq file, Loupe takes about [some time number] at memory usage peak of [some memory number]. The aim of ChromeQC analysis of Chromium sequencing data that is focused on QC of sizes of the molecules, the number of reads per molecule, the number of molecules per barcode, and the amount of DNA per barcode at substantially less time and memory costs than Loupe's performance. On top of that, ChromeQC is compatible with MultiQC [@Ewels_2016], a tool that combines relevant QC reports from multiple samples into a single integrated report.

# Methods

## Random Sampling of Barcodes
Raw FASTQ file is fed to ChromeQC. The user chooses a random seed that will deterministically sample without replacement 4000 barcodes out of 10x Chromium whitelist of barcodes. The FASTQ file is then read, the barcodes (first 16 nucleotides of the first read) are extracted and those reads with the sampled whitelisted barcodes are outputted to the next stage. In the same pass, we collect the distribution of sizes of the barcodes of the raw FASTQ file grouped by whether they are whitelisted or not. We report these statistics as two histograms in our report.
## Read Alignment

ChromeQC is agnostic  

- Agnostic to aligner
- Only cares about position (not CIGAR)
- Now supporting BWA MEM and minimap2. We are using minimap2 since it is three times as fast as BWA-MEM.
- The reads subsample that we collected is piped to minimap2 short read module and GRCh38 human reference genome. The mappings are then sorted by barcode then by position using SAMtools.

## Observed Molecules Sizes

The aligned reads are filtered by alignment score \(\<X), mapping quality (\<X), and edit distance (\>X). The reads are then processed to extract the molecule size. We use a a threshold of 60Kbp between each consecutive reads in order for them to be in the same molecule. The observed molecules are reported alongside the barcode they have, and number of reads that constitute it. If more than one read has the same orientation and the same mapping position, we only keep one of those reads as a constituting read of the molecule.

## Expected Molecule Sizes

We start by filtering out any molecules that have less than 6 reads as not having enough reads to be properly estimated. From the observed molecule sizes we inferred the expected molecule sizes based on the German Tank Problem estimation. Our expected estimates for the start, $\hat a$, and end, $\hat b$, of a molecule with observed start $a$, observed end $b$, and number of reads $n$ are:

$\hat a= a - \frac{a-b}{n-1}$

$\hat b= b + \frac{a-b}{n-1}$

After this correction, we report the histogram of the molecule sizes. We also report the mean of the molecule sizes weighted by molecule size, the N50 of molecule sizes, the mean of the number of reads per molecule weighted by the number of reads per molecule, and the N50 of number of reads per molecule.

## Report Generation

The final report of a single sample is generated using Rmarkdown.

## Multiple Report Aggregation
# Results

# Discussion

# References