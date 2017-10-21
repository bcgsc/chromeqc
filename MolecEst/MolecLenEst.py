#!/usr/bin/env python3
'''
Created on Monday, May 15 2017
Last Updated Friday, Oct 20 2017

Computes molecule size and stdev (for error bounds of molecule size)

Columns: BX, MI, RefName, Start, End, Length_stdev, Reads
Optional Columns: Mapq_median, AS_median, NM_median

Version 0.0.1

@author: cjustin
'''

from optparse import OptionParser
import pysam

class Molecule:
    def __init__(self, contig, start, end, newMolecID, barcode, interArrivals, totalBases, alignScore):
        self.contig = contig
        self.start = start
        self.end = end
        self.barcode = barcode
        self.newMolecID = newMolecID
        self.interArrivals = interArrivals
        self.totalBases = totalBases
        self.alignScore = alignScore
    
    def printAsTsv(self, fh, molec, count):
        fh.write(self.barcode + "\t" + str(self.newMolecID) + "\t" \
                 + str(self.contig) + "\t" + str(self.start) + "\t" + str(self.end) \
                 + "\t" + str(len(self.interArrivals) + 2) + "\n")
        
    def getLength(self):
        return self.end-self.start
        
class MolecIdentifier:
    
    def setDist(self, dist):
        self._maxDist = dist
        
    def setMin(self, min):
        self._min = min
    
    def setMAPQ(self, mapq):
        self._mapq = mapq
    
    def __init__(self, filename):
        """
        Constructor, identifies molecules based on inter-arrival time threshold
        @todo: Possible to thread per contig
        """
        self._min = 4
        self._maxDist = 50000
        self._mapq = 1
        samfile = pysam.AlignmentFile(filename, "rb")
        self._molec = {}
        
    def run(self, outPrefix):
        
        newMolecFH = open(outPrefix + ".tsv", "w"); 
        outfilebam = pysam.Samfile(outPrefix + ".bam", "wb", template=samfile)
        
        prevBarcode = "";
        prevChr = ""
        curReads = ();
        
        newMolecID = 0;        
        for read in samfile:
            barcode = ""
            # extract barcode
            barcodeList = [bc for bc in read.tags if "BX" in bc]
            if len(barcodeList) != 0:
                barcode = barcodeList[0][1]
                curReads.append(read)
            else:
                outfilebam.write(read)
                continue
            
            chr = read.reference_id
            if prevBarcode != barcode and read.reference_id:
                prevVal = 0
                prevVal1 = 0
                prevVal2 = 0
                start = curReads[0].pos
                interArrivals = []
                count = 0
                totalBases = 0
                totalAS = 0
                for read in curReads:
                    count += 1
                    
                    value = read.pos
                    absDist = value - prevVal
                    totalBases += read.rlen
                    totalAS += read.get_tag("AS")
                    
                    #check if molecules should be terminated
                    if absDist > self._maxDist and prevVal > 0:
                        end = prevVal + read.query_alignment_length
                        
                        #adjust find distance from nearest read
                        molec = Molecule(chr, start, end, \
                                         newMolecID, barcode, \
                                         interArrivals, \
                                         totalBases, totalAS)
                        
                        if  len(interArrivals) >= self._min:
                            molec.printAsTsv(newMolecFH, self._molec[maxMolec], maxMolec, count)
                        else:
                            molec.printAsTsv(newMolecFH, BedMolec("NA", 0, 0, 0), maxMolec, count)
                        if read.is_reverse:
                            prevVal2 = value
                            prevVal1 = 0
                        else:
                            prevVal1 = value
                            prevVal2 = 0
                        start = value;
                        newMolecID += 1
                        read.tags += [("MI", newMolecID)]
                        outfilebam.write(read)
                        interArrivals = []
                        trueMolecs = {}
                        prevVal = value
                        totalBases = 0;
                        totalAS = 0;
                        count = 0
                        continue
                    else:
                        read.tags += [("MI", newMolecID)]
                        outfilebam.write(read)
                    
                    interArrival = 0
                    if read.is_reverse:
                        if prevVal2 == 0:
                            prevVal2 = value
                            prevVal = value
                            continue
                        else:
                            interArrival = value - prevVal2
                            prevVal2 = value
                    else:
                        if prevVal1 == 0:
                            prevVal1 = value
                            prevVal = value
                            continue
                        else:
                            interArrival = value - prevVal1
                            prevVal1 = value
                    if interArrival > 0:
                        interArrivals.append(interArrival)
                    prevVal = value
                end = prevVal + read.query_alignment_length
                molec = Molecule(chr, start, end, newMolecID, barcode, trueMolecs, interArrivals, totalBases, totalAS)
                maxMolec = "NA";
                max = 0;
                for molecID in trueMolecs:
                    if max < trueMolecs[molecID]:
                        maxMolec = molecID
                        max = trueMolecs[molecID]
                if  len(interArrivals) >= self._threshold and maxMolec in self._molec:
                    molec.printAsTsv(newMolecFH, self._molec[maxMolec], maxMolec, count)
                else:
                    molec.printAsTsv(newMolecFH, BedMolec("NA", 0, 0, 0), maxMolec, count)
                newMolecID += 1
                curReads = ()
            prevBarcode = barcode;            
        outfilebam.close()
        samfile.close()
        newMolecFH.close()
    
if __name__ == '__main__':
    
    # specify parser options
    parser = OptionParser()
    parser.add_option("-b", "--bam", dest="bam",
                  help="Contig to genome BAM file", metavar="BAM")
    parser.add_option("-d", "--dist", dest="dist",
                  help="Minimum distance for contigs when considering interarrival times [50000]", metavar="DIST")
    parser.add_option("-o", "--output", dest="output",
                  help="Output location of result, will add a suffix to indicate what type of file it is", metavar="OUTPUT")
    parser.add_option("-m", "--min", dest="min",
                  help="minimum number of reads in alignment to consider [4]", metavar="MIN")
    parser.add_option("-q", "--mapq", dest="mapq",
                  help="minimum mapq threshold to consider [1]", metavar="MAPQ")
    
    (options, args) = parser.parse_args()  
  
    if options.bam and options.output:
        molecID = MolecIdentifier(options.bam)
        if options.dist:
            molecID.setDist(options.dist)
        if options.min:
            molecID.setMin(options.min)
        if options.mapq:
            molecID.setMAPQ(options.mapq)
        molecID.run(options.output)
    else:
        print("Missing required options -b -o")
