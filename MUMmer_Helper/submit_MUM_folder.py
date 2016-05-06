#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv
import glob
import os

script, working_dir , data_dir, reference = argv

#master hash
master_file = "sub_MUM_Py.sh"

file_out = open(master_file, 'w')
file_out.write("#!/bin/sh\n")
file_out.write("cd "+working_dir + "\n")

fq_num  = 0
#data_dir = "/escratch4/lxue/lxue_Aug_23/SNP_717v2/12Comparative/02MUMeach"
for filename in sorted(glob.glob(os.path.join(data_dir, '*.fasta'))):
    dir,file=os.path.split(filename)
    fq_num += 1
    sh_file = 'run' + str(fq_num) + '_' +file[0:-6] +'.sh'
    print(sh_file)

    file_out.write('qsub -q rcc-m128-30d ' + sh_file + " \n")
    with open(sh_file, 'w') as file_shell:
        file_shell.write("#!/bin/sh\n")
        file_shell.write("cd " + working_dir + "\n")
        file_shell.write("/usr/local/mummer/latest/nucmer    -prefix="+file[0:-6]+" \\\n")
        file_shell.write( reference + " \\\n")
        file_shell.write(filename+"\n")



file_out.close()
## Author : lxue@uga.edu


