# ChromeQC: Summarize sequencing library quality of 10x Genomics Chromium linked reads

This tool provides a quick report on the quality of a 10x Genomics Chromium linked reads library. The report summarizes the sizes of the molecules, the number of reads per molecule, the number of molecules per barcode, and the amount of DNA per barcode. The idea is to providea a FastQC-like tool in terms of speed but to contain information provided by the Summary page of the [Loupe software of 10x Genomics](https://support.10xgenomics.com/genome-exome/software/visualization/latest/what-is-loupe).

## Usage

The tool will have two modes of operation: fast and complete. The fast mode will produce a report as quickly as possible by subsampling the data in an intelligent fashion. The complete mode will analyze all of the data and produce a comprehensive report. The analysis will use reads aligned to the reference genome using BWA-MEM, Lariat, or Longranger. A stretch goal is to generate this report de novo without using a reference genome by assembling a small region of the genome and using that assembly as the reference. The report will be compatible with the report aggregating tool MultiQC.
### Commandline arguments

### Examples
```
python3 chromeQC
```
## How chromeQC work

## Prerequisites
```
```

The analysis and report will be created using R, the Tidyverse, RMarkdown, and Flexdashboard. Familiarity with some of these tools is useful, but not necessary to participate in this project. Non-technical participants are welcome to design the aesthetics of the report, prepare and deliver the presentation, and coordinate writing a brief paper about the tool.

Team Lead : Shaun Jackman | sjackman@gmail.com | @sjackman | Grad Student | BC Cancer Agency Genome Sciences Centre
