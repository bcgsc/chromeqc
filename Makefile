# Summarize sequencing library quality of 10x Genomics Chromium linked reads

# The reference genome.
ref=GRCh38

# The Longranger reference genome.
lrref=GRCh38-2.1.0

# Number of threads.
t=8

# gzip compression program. Use pigz for parallelized compression.
gzip=pigz -p$t

# Options for BCALM.

# k-mer size.
k=63

# Minimum k-mer abundance threshold.
abundance=2

# Report run time and memory usage.
export SHELL=zsh -opipefail
export REPORTTIME=1
export TIMEFMT=time user=%U system=%S elapsed=%E cpu=%P memory=%M job=%J
time=command time -v -o $@.time

.DELETE_ON_ERROR:
.SECONDARY:
.PHONY: all lrbasic lrwgsvc bwa bcalm paper sortbx molecule

# Run the entire analysis.
all: data/SHA256 lrbasic lrwgsvc bwa sortbx molecule

# Extract the barcodes from the reads using Longranger basic.
lrbasic: \
	hg002g1.lrbasic.fq.gz \
	hg003g1.lrbasic.fq.gz \
	hg004g1.lrbasic.fq.gz

# Align reads to the reference genome, call variants, and create a Loupe file.
lrwgsvc: \
	hg002g1.lrwgsvc.bam \
	hg003g1.lrwgsvc.bam \
	hg004g1.lrwgsvc.bam

# Align reads to the reference genome using BWA.
bwa: \
	hg002g1.lrbasic.bwa.sort.bam.bai \
	hg003g1.lrbasic.bwa.sort.bam.bai \
	hg004g1.lrbasic.bwa.sort.bam.bai

# Sort compressed SAM files by barcode.
sortbx: \
	hg002g1.lrbasic.bwa.sortbx.sam.gz \
	hg003g1.lrbasic.bwa.sortbx.sam.gz \
	hg004g1.lrbasic.bwa.sortbx.sam.gz

# Compute molecules coordinates from SAM sorted by barcode then position.
molecule: \
	hg002g1.lrbasic.bwa.sortbx.molecule.tsv \
	hg003g1.lrbasic.bwa.sortbx.molecule.tsv \
	hg004g1.lrbasic.bwa.sortbx.molecule.tsv

# Assemble reads with BCALM.
bcalm: hg004g.lrbasic.bcalm.k$k.a$(abundance).fa

# Render the paper from Markdown to HTML and PDF with pandoc.
paper: paper.html paper.pdf

hg004g.lrbasic.path: \
		hg004g1.lrbasic.fq.gz \
		hg004g2.lrbasic.fq.gz \
		hg004g3.lrbasic.fq.gz \
		hg004g4.lrbasic.fq.gz \
		hg004g5.lrbasic.fq.gz \
		hg004g6.lrbasic.fq.gz \
		hg004g7.lrbasic.fq.gz \
		hg004g8.lrbasic.fq.gz
	ls $^ >$@

# Download the human reference genome.
data/GRCh38.fa.gz:
	mkdir -p $(@D)
	curl -o $@ ftp://ftp.ensembl.org/pub/release-90/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz

# Uncompress data.
data/%.fa: data/%.fa.gz
	mkdir -p $(@D)
	gunzip -c $< | seqtk seq >$@

# Download the Long Ranger-compatible human reference genome.
data/refdata-%.tar.gz:
	curl -o $@ http://cf.10xgenomics.com/supp/genome/$(@F)

# Extract the Long Ranger-compatible human reference genome.
data/refdata-%/genome: data/refdata-%.tar.gz
	tar -x -C data -f $<
	touch $@

# Download the HG002 linked reads data.
data/hg002/%.fastq.gz:
	mkdir -p $(@D)
	curl -o $@ ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/AshkenazimTrio/HG002_NA24385_son/10Xgenomics_ChromiumGenome/NA24385.fastqs/$(@F)

# Download the HG003 linked reads data.
data/hg003/%.fastq.gz:
	mkdir -p $(@D)
	curl -o $@ ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/AshkenazimTrio/HG003_NA24149_father/10Xgenomics_ChromiumGenome/NA24149.fastqs/$(@F)

# Download the HG004 linked reads data.
data/hg004/%.fastq.gz:
	mkdir -p $(@D)
	curl -o $@ ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/AshkenazimTrio/HG004_NA24143_mother/10Xgenomics_ChromiumGenome/NA24143.fastqs/$(@F)

# Symlink the HG002 data.
data/hg002g1.fq.gz: data/hg002/read-RA_si-GCACAATG_lane-001-chunk-0002.fastq.gz
	ln -s hg002/$(<F) $@

# Symlink the HG003 data.
data/hg003g1.fq.gz: data/hg003/read-RA_si-GCTACTGA_lane-001-chunk-0002.fastq.gz
	ln -s hg003/$(<F) $@

# Symlink the HG004 data.
data/hg004g1.fq.gz: data/hg004/read-RA_si-GAGTTAGT_lane-001-chunk-0002.fastq.gz
	ln -s hg004/$(<F) $@
data/hg004g2.fq.gz: data/hg004/read-RA_si-GAGTTAGT_lane-002-chunk-0004.fastq.gz
	ln -s hg004/$(<F) $@
data/hg004g3.fq.gz: data/hg004/read-RA_si-GAGTTAGT_lane-003-chunk-0007.fastq.gz
	ln -s hg004/$(<F) $@
data/hg004g4.fq.gz: data/hg004/read-RA_si-GAGTTAGT_lane-004-chunk-0006.fastq.gz
	ln -s hg004/$(<F) $@
data/hg004g5.fq.gz: data/hg004/read-RA_si-GAGTTAGT_lane-005-chunk-0000.fastq.gz
	ln -s hg004/$(<F) $@
data/hg004g6.fq.gz: data/hg004/read-RA_si-GAGTTAGT_lane-006-chunk-0003.fastq.gz
	ln -s hg004/$(<F) $@
data/hg004g7.fq.gz: data/hg004/read-RA_si-GAGTTAGT_lane-007-chunk-0005.fastq.gz
	ln -s hg004/$(<F) $@
data/hg004g8.fq.gz: data/hg004/read-RA_si-GAGTTAGT_lane-008-chunk-0001.fastq.gz
	ln -s hg004/$(<F) $@

# Download the HG004 aligned linked reads data.
data/hg004/%.bam:
	mkdir -p $(@D)
	curl -o $@ ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/AshkenazimTrio/analysis/10XGenomics_ChromiumGenome_LongRanger2.1_09302016/NA24143_GRCh38/$(@F)

# Symlink the HG004 aligned linked reads data.
data/hg004.lrwgs.bam: data/hg004/NA24143_GRCh38_phased_possorted_bam.bam
	ln -s hg004/$(<F) $@

# Compute the SHA-256 of the data and verify it.
data/SHA256: \
		data/GRCh38.fa.gz \
		data/refdata-GRCh38-2.1.0.tar.gz \
		data/hg002g1.fq.gz \
		data/hg003g1.fq.gz \
		data/hg004g1.fq.gz
	gsha256sum -c SHA256
	gsha256sum $^ >$@

# Extract the barcodes from the reads using Longranger basic.
%_lrbasic/outs/barcoded.fastq.gz: data/%.fq.gz
	mkdir -p data/$*
	ln -sf $$(realpath $<) data/$*/
	command time longranger basic --id=$*_lrbasic --fastqs=data/$*

# Symlink the longranger basic FASTQ file.
%.lrbasic.fq.gz: %_lrbasic/outs/barcoded.fastq.gz
	ln -sf $< $@

# Align reads to the reference genome, call variants, and create a Loupe file.
%_lrwgsvc/outs/phased_possorted_bam.bam: data/%.fq.gz data/refdata-$(lrref)/genome
	mkdir -p data/$*
	ln -sf $$(realpath $<) data/$*/
	command time longranger wgs --vconly --id=$*_lrwgsvc --reference=data/refdata-$(lrref) --fastqs=data/$*

# Symlink the longranger wgs bam file.
%.lrwgsvc.bam: %_lrwgsvc/outs/phased_possorted_bam.bam
	ln -sf $< $@

# BWA

# Index the reference genome.
%.fa.bwt: %.fa
	bwa index $<

# Align paired-end reads to the draft genome using BWA-MEM.
%.bwa.sam.gz: %.fq.gz data/$(ref).fa.bwt
	bwa mem -t$t -pC data/$(ref).fa $< | $(gzip) >$@

# samtools

# Index a FASTA file.
%.fa.fai: %.fa
	samtools faidx $<

# Sort a compressed SAM file by barcode.
%.sortbx.sam.gz: %.sam.gz
	samtools sort -@$t -Osam -tBX $< | $(gzip) >$@

# Sort a compressed SAM file and convert to BAM.
%.sort.bam: %.sam.gz
	samtools sort -@$t -Obam -o $@ $<

# Index a BAM file.
%.bam.bai: %.bam
	samtools index $<

# BCALM

# Index the reads with BCALM.
%.bcalm.k$k.a$(abundance).h5: %.path
	$(time) bcalm -in $< -out $*.bcalm.k$k.a$(abundance) -k $k -abundance $(abundance) -nb-cores $t

# Assemble unitigs with BCALM.
%.fa: %.h5
	$(time) bglue -in $< -out $@ -k $k -nb-cores $t

# ChromeQC

# Compute molecules coordinates from SAM sorted by barcode then position.
%.sortbx.molecule.tsv: %.sortbx.sam.gz
	$(time) MolecEst/MolecLenEst.py -b $< -o $@

# Report

# Render an RMarkdown report to HTML.
%.html: %.rmd
	Rscript -e 'rmarkdown::render("$<", "html_document", "$(@F)")'

# Paper

# Download the Genome Research citation style language (CSL)
paper.csl:
	curl -o $@ https://www.zotero.org/styles/f1000research

# Convert the list of DOIs to Bibtex
%.bib: %.doi
	curl -LH "Accept: text/bibliography; style=bibtex" `<$<` | sed 's/^ *//' >$@

# Render Markdown to HTML using Pandoc
%.html: %.md
	pandoc -s -Fpandoc-crossref -Fpandoc-citeproc -o $@ $<

# Render Markdown to PDF using Pandoc
%.pdf: %.md
	pandoc -Fpandoc-crossref -Fpandoc-citeproc -o $@ $<
