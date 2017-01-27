#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This code split a VCF file into files of smaller size.  It can be used to run HapCUT2 in parallel.
Usage:
python VCFsplit4HapCUT2.py  vcf_input  line_number_per_file
Author : lxue@uga.edu
"""

import re
from sys import argv
import os.path


#################
### FUNCTIONS ###
#################

class batch_vcf:
    def __init__(self,file_in, batch_tracking):
        self.head = []
        self.content = []
        self.file_out = file_in[0:-4]+'_P'+str(batch_tracking)+'.vcf'

    def write(self):
        VCFOUT = open(self.file_out, "w")
        VCFOUT.write("".join(self.head))  # write head lines
        VCFOUT.write("".join(self.content))  # write head lines
        VCFOUT.close()


class VariantTable:
    """Hold the VCF records in memory"""

    def __init__(self, file_in):
        self.file_full = file_in
        dir, self.file_short = os.path.split(file_in)
        self.head = []

    def split(self, batch_line_num):
        check_begin = re.compile("^#")
        batch_num = 1
        b_vcf = batch_vcf(self.file_short,batch_num)
        line_num = 0
        with open(self.file_full, "r") as INPUT:
            for line in INPUT:
                if check_begin.match(line):
                    self.head.append(line)
                else:
                    line_num += 1
                    b_vcf.content.append(line)
                    if(line_num >= batch_line_num):
                        # write and initiate
                        b_vcf.head =  self.head
                        b_vcf.write()
                        # init
                        batch_num += 1
                        line_num = 0
                        b_vcf = batch_vcf(self.file_short,batch_num)
                    # just append as it is
            # end of for
            b_vcf.head = self.head
            b_vcf.write()  # last batch in memory


#################
###   MAIN    ###
#################

if __name__ == "__main__":
    script, input_file, batch_line_num = argv
    batch_line_num = int(batch_line_num)
    VarTab = VariantTable(input_file)
    VarTab.split(batch_line_num)
