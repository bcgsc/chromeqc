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


#P5-read1

P5_set = set()
for i in range(len(P5_Read1) - k + 1):
   P5_kmer = P5_Read1[i:i+k]
   #P5 16mers in a set
   P5_set.add(P5_kmer)

 
#P7

P7_set = set()
for i in range(len(P7) - k + 1):
   P7_kmer = P7[i:i+k]
   #P7 16mers in a list
   P7_set.add(P7_kmer)

   
#read2

Read2_set = set()
for i in range(len(Read2) - k + 1):
   Read2_kmer = Read2[i:i+k]
   #Read2 16mers in a list
   Read2_set.add(Read2_kmer)


#combine all of above 16mers into a single set
   
import itertools
from itertools import chain 
  
all_kmers = set(chain(P5_set, P7_set, Read2_set))
print(all_kmers)
