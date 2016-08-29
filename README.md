# PythonNGSTools
Scripts for NGS processing

#MUMmerSNPs2VCF.py  
This code convert output file from show-snps of MUMmer into VCF format.
"-x 1" option should be turned on so that reference fasta is not needed.  

Usage:  

show-snps -Clr -x 1  -T mum.delta.filter  >mum.delta.filterX.snps  
python3.4 MUMmerSNPs2VCF.py mum.delta.filterX.snps  mum_filterX.snps.vcf  


#Download_FTP_ENA.py


Download fastq files from ENA.

Usage:  
1. Search the project in ENA to get the information page of one study.  
2. Click "Read Files" tag next to "Navigation".  
3. Download the TEXT file (save as ENA_description.txt).  
4. Write the shell scripts to download fastq files (The master shell submit downloading jobs to one queue on clusters).  
python2.7 Download_FTP_ENA.py  ./  ENA_description.txt  

./ : is the current directory and can be changed into the directory to store the fastq files.  

#MUMmer helper
Some tools to split large query file, submit jobs to clusters and merge the delta output from MUMmer


