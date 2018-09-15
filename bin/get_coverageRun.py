#!/usr/bin/env python2.7

import os
import sys
import getpass
import shutil
from shutil import copy
import glob
import subprocess
import multiprocessing
import re
import numpy
from numpy import median

#DEFAULT SETTINGS#
ncpus=1
optionBWA='y'
optionQUALIMAP='y'


# Get n.o of Cores
all_cores = multiprocessing.cpu_count()
ncpus = raw_input("\nThis PC has " + str(all_cores) + " cores.\nDon't use too many cores because for every core you give, SPAdes needs 4.\nPlease enter the number of cores you wish to use: \n")

## Run courtesy ##
def run_Courtesy():
## Ask the user what programs they'd like to use ##
	print("By default this script runs SPAdes, but enter 'y' to run BWA or 'n' not to:")
	optionBWA=raw_input()
	if optionBWA != 'y' and optionBWA != 'n':
		print("Please enter either 'y' or 'n'")
		optionBWA=raw_input()

	if optionBWA == 'y':
	    print("By default this script runs SPades but enter 'y' to also run Qualimap or 'n' not to")
	    optionQUALIMAP=raw_input()
	    if optionQUALIMAP != 'y' and optionQUALIMAP != 'n':
		    print("Please enter either 'y' or 'n'")
		    optionQUALIMAP=raw_input()
	else:
		optionQUALIMAP='n'


## Get Run Name ##
try:
    dataPath=sys.argv[1]
    runName=os.path.basename(dataPath)
except:
	print("Run as so: python get_coverageRun.py <foldername>")

# Added in case user appends path to data with '/'
if runName=="":
	dataPath=dataPath[:-1]
	runName=os.path.basename(dataPath)

scriptPath=os.path.dirname(os.path.realpath(__file__))
resultsPath=os.path.join(scriptPath.replace("bin", "WGS_Results"), runName)


## Make hub directory in home ##
try:
    os.makedirs(resultsPath, 0o777)
except:
	pass

## Run get_coverageProc.py ##
def run_Pipe():
	print("\nRunning coverage pipe for samples in directory: " + dataPath)
	print("\n")
	os.chdir(dataPath)
	pipe_command=" ".join(["ls *R1.fastq.gz | parallel -r -j", str(ncpus), "python", os.path.join(scriptPath, "get_coverageProc.py"), \
	                       runName, resultsPath, dataPath, "{}", optionBWA, optionQUALIMAP ])
	subprocess.check_call(pipe_command, shell=True)


## Extracting data and calculating coverage average ##
def run_Averages():
	all_values=[]
	for fldr1 in glob.glob(os.path.join(resultsPath, '*')):
		strainName=os.path.basename(fldr1)
		qualiDir=os.path.join(resultsPath, strainName, 'qualimap', strainName+'_qualimapResult')
		try:
			with open(os.path.join(qualiDir, 'genome_results.txt'), 'r') as file:
			    file=file.readlines()
			    pattern=('\s\s\s\s\snumber\sof\sreads\s=\s(\d?,?\d\d\d,?\d\d\d)')
			    value=re.search(pattern, str(file)).group(1)
			    value=value.replace(",","")
			    value=int(value)
			    all_values.append(value)
		except:
			pass

	total=0
	average=0
	for x in all_values:
		total=total+int(x)

	the_mean=total/len(all_values)
	the_median=median(all_values)


	with open(os.path.join(resultsPath, 'coverage_average.txt'), 'a') as file2:
		file2.write(" ".join(["###", runName, "Coverage Statistics ###"]))
		file2.write("\n\n")
		file2.write("Number of reads:")
		file2.write("\n\n")		
		print >>file2, "Mean: "+str(the_mean)
		file2.write("\n")
		print >>file2, "Median: "+str(the_median)


run_Courtesy()
run_Pipe()
run_Averages()


print("\n Done! ^_^ \n")