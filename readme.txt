### getCoverage ###

get_coverageRun.py and get_coverageProc.py are 2 scripts that form a mini pipe for passing your fastq files through to run SPAdes, BWA & Samtools, and then to run Qualimap to obtain information about the coverage of your sequences.

## Installation:
Download and store getCoverage somewhere reasonable i.e. in /home/

## Dependencies:
SPAdes - https://github.com/ablab/spades
https://www.ncbi.nlm.nih.gov/pubmed/22506599

Samtools - http://samtools.sourceforge.net/
https://www.ncbi.nlm.nih.gov/pubmed/19505943

BWA - http://bio-bwa.sourceforge.net/
https://www.ncbi.nlm.nih.gov/pubmed/19451168

Qualimap - http://qualimap.bioinfo.cipf.es/
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4708105/

GNU Parallel -https://www.gnu.org/software/parallel/
@book{tange_ole_2018_1146014,
      author       = {Tange, Ole},
      title        = {GNU Parallel 2018},
      publisher    = {Ole Tange},
      month        = Mar,
      year         = 2018,
      ISBN         = {9781387509881},
      doi          = {10.5281/zenodo.1146014},
      url          = {https://doi.org/10.5281/zenodo.1146014}
}

python2.7 - https://www.python.org/downloads/release/python-2714/

Python modules - Numpy


## Your data:
Your data folder should contain both R1 and R2 fastq(.gz) files per sample.


## How to run it:
python /path/to/get_coverageRun.py </path/to/data_name>


## Your results:
Your results (as per sample) will be kept in the results folder of the main (getCoverage) directory
i.e. - ~/getCoverage/results/data_name/sample_1/spades/contigs.fasta
     - ~/getCoverage/results/data_name/sample_1/qualimap/sample_1_qualimapResult/qualimapReport.html


# Dolapo Ajayi, August 2018 - Contact: dolaajayi@hotmail.com