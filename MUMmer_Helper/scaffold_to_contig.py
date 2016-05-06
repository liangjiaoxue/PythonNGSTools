#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv
import re

code, fasta_file, output_file, lim_in  = argv


#fasta_file  = "Potra01-genome.fa"
#output_file = "Potra01"
#size_limit0 = 10000000

file_out = open(output_file, 'w')

lim =  int(lim_in)


pattern_in = 'N{'+ str(lim)+',}'
pattern = re.compile(pattern_in)
total_num = 0
fasta = open(fasta_file, "rU")
for line in "".join(fasta.readlines()).split(">")[1:]:
    line = line.split("\n")
    seqid = line[0].split()[0].replace("|", "")
    seqstr = "".join(line[1:]).upper()
    out_split = pattern.split(seqstr)
    num_part = 0

    if len(out_split)>1 :
        for seq_part in out_split:
            num_part += 1
            seqid_new = seqid + '_'+ str(num_part)
            file_out.write(">" + seqid_new + "\n")
            file_out.write(seq_part + "\n")
    else :
        file_out.write(">" + seqid + "\n")
        file_out.write(seqstr + "\n")

file_out.close()







