#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv
import glob
import os

script,  data_dir, reference, query, method, output_file= argv

#master hash


file_out = open(output_file, 'w')
file_out.write(reference+" "+ query+ "\n")
method_in = method.upper()
file_out.write(method_in+"\n")

fq_num  = 0
#data_dir = "/escratch4/lxue/lxue_Aug_23/SNP_717v2/12Comparative/02MUMeach"
for filename in sorted(glob.glob(os.path.join(data_dir, '*.delta'))):
    #dir,file=os.path.split(filename)
    print(filename)
    fq_num += 1
    with open(filename, "rU") as f:
        lines = f.readlines()[2:]
        for line in lines:
            line_n = line.rstrip()
            file_out.write(line_n+"\n")

print ("total file"+str(fq_num))
file_out.close()
## Author : lxue@uga.edu

#/usr/local/mummer/latest/delta-filter -1  Potra01_p_9.delta  >Potra01_p_9.delta.1filter
#/usr/local/mummer/latest/show-coords -rclT Potra01_p_9.delta.1filter  > Potra01_p_9.1delta.coords
