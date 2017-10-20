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
10x Genomics long range sequencing is a new technology that a gives a wholistic picture of the sequencing. Each few DNA molecules will have a unique 16 nucleotides long barcode mixed with. These molecules are then sequenced with Illumina short paired-end sequencing. A molecule is expected to have a uniform location distribution of the reads covering it. Before relying on these long range reads and the information they imply, it is important to perform quality checks on the sequencing data. These checks include computing distributions of molecule sizes, the number of molecules per barcode, the [list more stuf]. 10x Genomics provides a tool, [NAME], that does most of these quality checks but a typical [some number]x coverage sequencing takes about [some time number] at memory usage peak of [some memory number]. Our aim is to provide a pipeline that perform these quality controls at substantially less time and memory costs.
MultiQC [@Ewels_2016]

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
