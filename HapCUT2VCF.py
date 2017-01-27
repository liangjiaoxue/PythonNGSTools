#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This code convert a output file from HapCUT2(https://github.com/pjedge/hapcut2) into VCF format.
Usage:
HapCUT2VCF.py   hapcut2_table  output_VCF   original_VCF(optional)

If the original input VCF file for HapCUT2 is provided, it will be combined into the same output file.
Each block in HapCUT2 table is stored as haplotype block in VCF file, and marked using PS tag.
The numbering of PS starts from 1 for each run. The output tables can be concatenated before converting
to generate unique PS IDs in the whole genome.

Author : lxue@uga.edu
"""

import re
import gzip
import sys
from sys import argv



#################
### FUNCTIONS ###
#################


class  VarTable:
    """Read variant table from HapCUT2 output """
    def __init__(self):
        self.hap_vcf = {}
        self.delete_list = {}
        self.vcf_head = []
        self.vcf_content = []

    def load_haptable(self,input_filel):
        ps_tracking = 0
        with open(input_file,"r") as hap_table :
            for line in hap_table:
                if line.startswith('*****') or line.startswith('BLOCK'):
                    if line.startswith('BLOCK'):
                        ps_tracking += 1
                    continue
                records = line.rstrip().split("\t")
                idx, hap1,hap2, chrom, position, ref, alt = records[0:7]
                idx = int(idx)
                if hap1 == '-' or hap2 == '-':
                    self.delete_list[idx] = 1
                else :
                    gt_out = hap1+'|'+hap2+':'+str(ps_tracking) # add PS number
                    out_line = [chrom, position,'.',ref,alt,'30','PASS','.','GT:PS',gt_out]
                    self.hap_vcf[idx] = out_line
                    #  0     1   2   3   4   5       6       7        8       9
                    # CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	sample1

    def write_VCF_haponly(self,vcf_out):
        OUT = open(vcf_out, "w")
        OUT.write('##fileformat=VCFv4.1' + "\n")
        OUT.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">' + "\n")
        out_line = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'sample1']
        OUT.write("\t".join(out_line) + "\n")
        keys_order = sorted( self.hap_vcf.keys())
        for idx_order in keys_order :
            out_line = self.hap_vcf[idx_order]
            OUT.write("\t".join(out_line) + "\n")

    def replace_gt(self,format, data, hap_data):
        format_records = format.split(':')
        gt_pos = format_records.index('GT')
        hap_list = hap_data.split(':')
        newdata_list = data.split(':')
        newdata_list[gt_pos] = hap_list[0]  # change GT
        newdata_list.append(hap_list[1])          # append PS record
        return format+':PS',  ':'.join(newdata_list)

    def check_ori_vcf(self, vcf_original, output_file):
        check_begin = re.compile("^#")
        tracking = 0
        OUT = open(output_file, "w")
        with open(vcf_original, "r") as INPUT:
            for line in INPUT:
                if check_begin.match(line):
                    OUT.write(line) # report head lines
                else :
                    tracking += 1
                    if tracking in self.delete_list.keys():
                        continue
                    # filter deleted records
                    record = line.rstrip().split("\t")
                    record[7] = '.'
                    # if phased replace the genotype
                    if tracking in self.hap_vcf.keys():
                        hap_out = self.hap_vcf[tracking]
                        if record[0] != hap_out[0] or   record[1] != hap_out[1]:
                            sys.exit("Order in original VCF doesn't match with HapCUT2 output")
                        else :
                            # change the genotype of
                            new_format, new_data = self.replace_gt(record[8],record[9],hap_out[9])
                            record[8] = new_format
                            record[9] = new_data
                    # write the vcf line
                    OUT.write("\t".join(record)+"\n")  # report content lines
        OUT.close()
# End of class


#################
###   MAIN    ###
#################

if __name__ == "__main__":
    if len(argv) == 4 :
        script, input_file, output_file, vcf_original = argv
    elif  len(argv) == 3 :
        script, input_file, output_file = argv
        vcf_original = ''
    else :
        sys.exit("Usage: HapCUT2VCF  hapcut2_table  output_VCF   original_VCF(optional)")
    # read HapCUT2 output
    VarTab = VarTable ()
    VarTab.load_haptable(input_file)
    if vcf_original == '':
        VarTab.write_VCF_haponly(output_file)
    else :
        VarTab.check_ori_vcf(vcf_original,output_file)
