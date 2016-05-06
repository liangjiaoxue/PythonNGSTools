#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv

code, fasta_file, output_file, size_limit0 = argv


#fasta_file  = "Potra01-genome.fa"
#output_file = "Potra01"
#size_limit0 = 10000000


size_limit = int(size_limit0)

num = 0
len_test = 0
# read fasta
fasta = open(fasta_file, "rU")
for line in "".join(fasta.readlines()).split(">")[1:]:
    line=line.split("\n")
    seqid = line[0].split()[0].replace("|","")
    seqstr = "".join(line[1:]).upper()
    seqlen = len(seqstr)
    len_test += seqlen


    if len_test > size_limit or num == 0 : # initial
        if num > 0:
            handleOUT.close()

        len_test = 0
        num += 1
        print ("Open file "+str(num)+"\n")
        file_out = output_file + "_p_" + str(num) + ".fasta"
        handleOUT = open(file_out, "w")

    # write out all the time
    handleOUT.write(">" + seqid + "\n")
    handleOUT.write(seqstr + "\n")

handleOUT.close()
