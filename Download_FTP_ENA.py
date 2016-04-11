#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv
import re
import os

script, first, second = argv
working_dir = first
data_file   = second

dir = os.path.dirname(os.path.realpath(__file__))
data_file_full = os.path.join(dir,data_file)

master_file = "run_ENA_download_Py.sh"

file_out = open(master_file, 'w')
file_out.write("#!/bin/sh\n")
file_out.write("cd "+working_dir + "\n")
	
	
	
num = 0
run_position = 0
ftp_position = 0	

with open(data_file_full, 'r') as file_in:	
	for line in file_in.readlines():
	    buffer = re.split(r'\t', line.strip())
	    
	    num += 1
	    
	    if num == 1 :
	    	for x in range(0,len(buffer)):
	    		if buffer[x] == 'run_accession' :
	    			run_position = x
	    		if buffer[x] == 'fastq_ftp' :
	    			ftp_position = x
	    else:
	    	run_id  = buffer[run_position]
	    	ftp_id_string = buffer[ftp_position]
	    	
	    	ftp_ids =  re.split(r'\;', ftp_id_string)
	    	fq_num  = 0 
	    	for ftp_addr in ftp_ids :
	    		fq_num += 1
	    		sh_file = 'runPy_'+ str(num-1)+ '_'+ run_id+'_'+ str(fq_num) +'.sh'
	    		# master shell file
	    		file_out.write('qsub -q copyq '+ sh_file + " \n")
	    		
	    		with open(sh_file, 'w') as file_shell :
	    			file_shell.write("#!/bin/sh\n")
	    			file_shell.write("cd "+ working_dir + "\n")
	    			file_shell.write("wget "+ ftp_addr)

file_out.close()
## Author : lxue@uga.edu
   
   
