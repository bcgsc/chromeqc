#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 14:15:18 2017

@author: nikka.keivanfar
"""
chmod +x select_random_subset/adapter_16mers.py

###fasta as input


def fasta_reader(filename):
    from Bio.SeqIO.FastaIO import FastaIterator
    with open(filename) as handle:
        for record in FastaIterator(handle):
            yield record

sequences = [] #make list out of fasta reads
adapters = [] #make list out of fasta headers

for entry in fasta_reader("adapters.fasta"): #to do: change file path
    heading = str(entry.id) #header of fasta
    adapters.append(heading) 
    reads = str(entry.seq) #sequence of specific fasta entry
    sequences.append(reads)

adapters_dict = {} #make dictionary with fasta headers and corresponding seqs
for i in range (len(adapters)):
    adapters_dict[adapters[i]] = sequences[i]
print(adapters_dict)

k = 16
                                            
all_kmers = set()
for values in adapters_dict.itervalues():
    for i in range(len(values) - k + 1):
        kmer = values[i:i+k]
        all_kmers.add(kmer)
print(all_kmers)
print(len(all_kmers))
