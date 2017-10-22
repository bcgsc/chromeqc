#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 14:15:18 2017

@author: nikka.keivanfar
"""
chmod +x select_random_subset/adapter_16mers.py

#to do: fasta as input
#to do: scrap dictionaries, make sets

P5_read1 = 'AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT'
P7 = 'CAAGCAGAAGACGGCATACGAGAT'
read2 = 'GTGACTGGAGTTCAGACGTGT' ##P7 and read 2 not concatenated due to Nmer between (sample index)

adapters = [P5_read1, P7, read2] #to do: streamline loops for all adapters combined


P5_kmers = {}
P7_kmers = {}
read1_kmers = {}
read2_kmers = {}
k = 16

#P5_Read1 16mers

for i in range(len(P5_read1) - k + 1):
   kmer = P5_read1[i:i+k]
   if P5_kmers.has_key(kmer):
      P5_kmers[kmer] += 1
   else:
      P5_kmers[kmer] = 1

for kmer, count in P5_kmers.items():
   print(kmer + "\t" + str(count))
   P5mers = set(kmer)
   
#P7 16mers
   
for i in range(len(P7) - k + 1):
   kmer = P7[i:i+k]
   if P7_kmers.has_key(kmer):
      P7_kmers[kmer] += 1
   else:
      P7_kmers[kmer] = 1

for kmer, count in P7_kmers.items():
   print(kmer + "\t" + str(count))
   P7mers = set(kmer)
   
#read2 16mers

for i in range(len(read2) - k + 1):
   kmer = read2[i:i+k]
   if read2_kmers.has_key(kmer):
      read2_kmers[kmer] += 1
   else:
      read2_kmers[kmer] = 1

for kmer, count in read2_kmers.items():
   print(kmer + "\t" + str(count))
   read2mers = set(kmer)
