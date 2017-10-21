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
    def __init__(self, rname, start, end, newMolecID, barcode, interArrivals, totalBases, alignScore, count):
        self.rname = rname
        self.start = start
        self.end = end
        self.barcode = barcode
        self.newMolecID = newMolecID
        self.interArrivals = interArrivals
        self.totalBases = totalBases
        self.alignScore = alignScore
        self.count = count

    def asTSV(self):
        return self.rname + "\t" + str(self.start) + "\t" + str(self.end) \
            + "\t" + self.barcode + "\t" + str(self.count) + "\t" + str(self.newMolecID)

    def getLength(self):
        return self.end-self.start
        
class MolecIdentifier:
    
    def setDist(self, dist):
        self._maxDist = dist
        
    def setMin(self, min):
        self._min = min
    
    def setMAPQ(self, mapq):
        self._mapq = mapq
    
    def setNewBam(self, filename):
        self._newBamFilename = filename
    
    def setOutput(self, filename):
        self._tsvFilename = filename
        
    def setMAPQ(self, mapq):
        self._mapq = mapq
        
    def printTSV(self, molec):
        if self._tsvFilename:
            self._newMolecFH.write(molec.asTSV() + "\n")
        else:
            print(molec.asTSV())
    
    def __init__(self, filename):
        """
        Constructor, identifies molecules based on inter-arrival time threshold
        """
        self._min = 4
        self._maxDist = 50000
        self._mapq = 1
        self._filename = filename;
        self._newBamFilename = ""
        self._tsvFilename = ""
        
    def run(self):
        samfile = pysam.AlignmentFile(self._filename, "rb")
        if self._newBamFilename:
            self._outfilebam = pysam.AlignmentFile(self._newBamFilename, "wb", template=samfile)
        else:
            self._outfilebam = None
        
        header = "Rname\tStart\tEnd\tBX\tReads\tMI"
        if self._tsvFilename:
            self._newMolecFH = open(self._tsvFilename, "w");
            self._newMolecFH.write(header + "\n")
        else:
            self._newMolecFH = None
            print(header)
            
        prevBarcode = ""
        prevChr = ""
        curReads = []
        trueMolecs = {}
        
        newMolecID = 0
        for read in samfile:
            barcode = ""
            if read.is_unmapped:
                continue
            # extract barcode
            barcodeList = [bc for bc in read.tags if "BX" in bc]
            if len(barcodeList) != 0:
                barcode = barcodeList[0][1]
            else:
                if self._newBamFilename:
                    self._outfilebam.write(read)
                continue
            if prevChr == "" or prevBarcode == "":
                prevBarcode = barcode
                prevChr = read.reference_id
            if prevBarcode != barcode or read.reference_id != prevChr:
                prevVal = 0
                prevRead = curReads[0]
                prevVal1 = 0
                prevVal2 = 0
                start = curReads[0].pos
                rname = curReads[0].reference_name
                interArrivals = []
                count = 0
                totalBases = 0
                totalAS = 0
                
                #mapq values for calculating median
                mapqs = []
                #alignment score values for calculating median
                aScores = []
                
                for curRead in curReads:
#                     print(str(curRead.is_reverse) + " " + curRead.reference_name + " " + str(curRead.pos))                    
                    value = curRead.pos
                    absDist = value - prevVal
                    totalBases += curRead.rlen
                    totalAS += curRead.get_tag("AS")
                    
                    #check if molecules should be terminated
                    if absDist > self._maxDist and prevVal > 0:
                        end = prevRead.reference_end
                        
                        #find distance from nearest read
                        molec = Molecule(rname, start, end, \
                                         newMolecID, barcode, \
                                         interArrivals, \
                                         totalBases, totalAS, count)
                        if prevRead.is_reverse:
                            prevVal2 = value
                            prevVal1 = 0
                        else:
                            prevVal1 = value
                            prevVal2 = 0
                        start = value;
                        if count >= self._min:
                            self.printTSV(molec)
                            newMolecID += 1
                        if self._newBamFilename:
                            curRead.tags += [("MI", newMolecID)]
                            self._outfilebam.write(curRead)
                        interArrivals = []
                        prevVal = value
                        totalBases = 0;
                        totalAS = 0;
                        count = 0
                        continue
                    else:
                        if self._newBamFilename:
                            curRead.tags += [("MI", newMolecID)]
                            self._outfilebam.write(curRead)
                    
                    #inter arrival time is distance between read of the same direction
                    interArrival = 0
                    if curRead.is_reverse:
                        if prevVal2 == 0:
                            prevVal2 = value
                            prevVal = value
                            count += 1
                            continue
                        else:
                            interArrival = value - prevVal2
                            prevVal2 = value
                    else:
                        if prevVal1 == 0:
                            prevVal1 = value
                            prevVal = value
                            count += 1
                            continue
                        else:
                            interArrival = value - prevVal1
                            prevVal1 = value
                    if interArrival > 0:
                        count += 1
                        interArrivals.append(interArrival)
                    prevVal = value
                    prevRead = curRead
                end = prevRead.reference_end
                molec = Molecule(rname, start, end, newMolecID, barcode, interArrivals, totalBases, totalAS, count)
                if count >= self._min:
                    self.printTSV(molec)
                    newMolecID += 1
                curReads = []
            curReads.append(read)
            prevBarcode = barcode;
            prevChr = read.reference_id
        
        #clean up
        samfile.close()
        if self._newMolecFH != None:
            self._newMolecFH.close()
        if self._outfilebam != None:
            self._outfilebam.close()
    
if __name__ == '__main__':
    
    # specify parser options
    parser = OptionParser()
    parser.add_option("-b", "--bam", dest="bam",
                  help="Reference to genome BAM file", metavar="BAM")
    parser.add_option("-d", "--dist", dest="dist",
                  help="Minimum distance when considering interarrival times [50000]", metavar="DIST")
    parser.add_option("-o", "--output", dest="output",
                  help="file name of tsv file (optional)", metavar="OUTPUT")
    parser.add_option("-n", "--new_bam", dest="newBam",
                  help="new bam file (optional)", metavar="NEWBAM")
    parser.add_option("-m", "--min", dest="min",
                  help="minimum number of reads in alignment to consider [4]", metavar="MIN")
    parser.add_option("-q", "--mapq", dest="mapq",
                  help="minimum mapq threshold to consider [1]", metavar="MAPQ")
    
    (options, args) = parser.parse_args()  
  
    if options.bam:
        molecID = MolecIdentifier(options.bam)
        if options.dist:
            molecID.setDist(options.dist)
        if options.min:
            molecID.setMin(options.min)
        if options.mapq:
            molecID.setMAPQ(options.mapq)
        if options.newBam:
            molecID.setNewBam(options.newBam)
        if options.output:
            molecID.setOutput(options.output)
        molecID.run()
    else:
        print("Missing required options -b")
