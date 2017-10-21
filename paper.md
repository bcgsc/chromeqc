---
title: 'Linked-Reads QC: Summarize sequencing library quality of 10x Genomics Chromium linked reads'
author: [Shaun D Jackman, Justin Chu, Emre Erhan, Nikka Keivanfar, Sean La, Swapna Menon, Tatyana Mozgacheva, Baraa Orabi, Chen Yang, Hamid Younesy]
bibliography: paper.bib
csl: paper.csl
rangeDelim: "&ndash;"
figPrefix: "Fig."
tblPrefix: ["Table", "Tables"]
---

# Abstract

# Introduction
10x Genomics Chromium sequencing is long range information sequencing library preparation toolkit. Every few DNA molecules (~100K bp) will have a unique 16 nucleotides long barcode mixed with them. These molecules are then sequenced with Illumina short paired-end sequencing. A molecule is expected to have a uniform distribution of locations of the reads covering it. 

Quality control (QC) for sequencing data is done to assess whether the sequencing experiment has been perfomed successfully or not. One popular QC tool for Illumina reads is FastQC which gathers basic information such as base qualities, sequence distribution, or GC content and reports that in quick manner. However, FastQC does not provide QC of aspects that are specific to the long range reads of Chromium. 

For that, 10x Genomics provide their own analysis tool, Loupe. Loupe provides QC summary of the sequencing data alongside phasing information, SNP calling, and structural variants discovered. When analyzing [some number]x coverage fastq file, Loupe takes about [some time number] at memory usage peak of [some memory number]. The aim of ChromeQC analysis of Chromium sequencing data that is focused on QC of sizes of the molecules, the number of reads per molecule, the number of molecules per barcode, and the amount of DNA per barcode at substantially less time and memory costs than Loupe's performance. On top of that, ChromeQC is compatable with MultiQC [@Ewels_2016], a tool that combines relevent QC reports from multiple samples into a single integrated report.

# Methods
## Extract Barcodes

## Random Sampling of Barcodes

## Read Alignment

## Grouping Reads To Molecules

## Computing Molecule Statistisc

## Report Generation

## Multiple Report Aggregation
# Results

# Discussion

# References
