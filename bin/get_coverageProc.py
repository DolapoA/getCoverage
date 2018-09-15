#!/usr/bin/env python2.7


import os
import sys
import shutil
from shutil import copy, move
import glob
import subprocess

## Arguments recieved ##
runName=sys.argv[1]
resultsPath=sys.argv[2]
dataPath=sys.argv[3]
fastqR1=sys.argv[4]
optionBWA=sys.argv[5]
optionQUALIMAP=sys.argv[6]


## Extract the strain name create R2 version of fastq ##
# Change name #
a=list(fastqR1)
a[-10]='2'
# Convert list() to str() #
a=''.join(a)
# Use string #
fastqR2=a
# Get basename of path, then split for strain name #
b=os.path.basename(a)
strainName, filetype = b.split('_R')
strainDir=os.path.join(resultsPath, strainName)



## Run SPAdes ##
def run_Spades():
	os.chdir(resultsPath)
	spadesDir=os.path.join(strainDir, "spades")
	file_list=[]
	for file in glob.glob(os.path.join(spadesDir,'*')):
	    file=os.path.basename(file)
	    file_list.append(file)

	if 'contigs.fasta' in file_list:
	    print(" ".join(["SPAdes results for", strainName, "already obtained."]))
	else:
	    spades_command=" ".join(["spades -t 8 -k 21,33 --careful -1", os.path.join(dataPath, fastqR1), "-2", os.path.join(dataPath, fastqR2), "-o", spadesDir])
	    try:
	        subprocess.check_call(spades_command, shell=True)
	    except:
	    	pass

## Run BWA ##
def run_Bwa():
	bwaDir=os.path.join(strainDir, "bwa")
	spadesDir=os.path.join(strainDir, "spades")
	try:
	    os.makedirs(bwaDir, 0o777)
	except:
		pass
	shutil.copy(os.path.join(spadesDir, "contigs.fasta"), bwaDir)
	os.chdir(dataPath)

	for file in glob.glob("".join([strainName, '*fastq.gz'])):
		try:
		    shutil.copy(file, bwaDir)
		except:
			pass

	os.chdir(bwaDir)

	file_list=[]
	for file in glob.glob(os.path.join(bwaDir,'*')):
	    file=os.path.basename(file)
	    file_list.append(file)

	if 'test_bwa_out_sorted.bam' in file_list:
	    print(" ".join(["BWA results for", strainName, "already obtained."]))
	else:
		bwa_command="bwa index -a bwtsw contigs.fasta; \
		bwa aln contigs.fasta *R1.fastq.gz > R1_bwa_out.sai ; \
		bwa aln contigs.fasta *R2.fastq.gz > R2_bwa_out.sai ;\
		bwa sampe contigs.fasta R1_bwa_out.sai R2_bwa_out.sai *R1.fastq.gz  *R2.fastq.gz > test_bwa_out.sam ; \
		samtools view -ubS test_bwa_out.sam > test_bwa_out.bam ; \
		samtools sort -o test_bwa_out_sorted.bam test_bwa_out.bam ;"
		subprocess.check_call(bwa_command, shell=True)

	bwa_othersDir=os.path.join(bwaDir, "bwa_others")
	qualimapDir=os.path.join(strainDir, "qualimap")

	try:
		os.makedirs(bwa_othersDir, 0o777)
	except:
		pass

	try:
		os.makedirs(qualimapDir, 0o777)
	except:
		pass

## Cleanup - move files around ##
	os.chdir(bwaDir)
# 2>/dev/null - silences the error message if there's no file to be moved #
	copy_and_move_command=" ".join(["cp *bwa_out_sorted.bam", qualimapDir, \
		                           "; mv *.amb", bwa_othersDir, "2>/dev/null", \
		                           "; mv *.ann", bwa_othersDir, "2>/dev/null", \
		                           "; mv *.bwt", bwa_othersDir, "2>/dev/null", \
		                           "; mv *.pac", bwa_othersDir, "2>/dev/null", \
		                           "; mv *.sai", bwa_othersDir, "2>/dev/null", \
		                           "; mv *.sa", bwa_othersDir, "2>/dev/null"])
	try:
		subprocess.check_call(copy_and_move_command, shell=True)
	except:
		pass

## Run Qualimap ##
def run_Qualimap():
	qualimapDir=os.path.join(strainDir, "qualimap")
	os.chdir(qualimapDir)
	qualiResultPath=strainName+"_qualimapResult"
	
	file_list=[]
	for file in glob.glob(os.path.join(qualiResultPath,'*')):
	    file=os.path.basename(file)
	    file_list.append(file)

	if 'css' in file_list:
	    print(" ".join(["Qualimap results for", strainName, "already obtained."]))
	else:
	    qualimap_command=" ".join(["qualimap bamqc -bam test_bwa_out_sorted.bam -outdir", qualiResultPath, "-outformat html" ])
	    try:
		    subprocess.check_call(qualimap_command, shell=True)
	    except:	
		    pass
	
#############################################################
######################Run Functions##########################
#############################################################


run_Spades()

if optionBWA=='y':
	run_Bwa()
else:
    pass	

if optionQUALIMAP=='y':
	run_Qualimap()
else:
	pass
