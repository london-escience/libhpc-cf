# Copyright (c) 2015, Imperial College London
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
# this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# 
# 3. Neither the names of the copyright holders nor the names of their 
# contributors may be used to endorse or promote products derived from this 
# software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
# -----------------------------------------------------------------------------
#
# This file is part of the libhpc-cf Coordination Forms library that has been 
# developed as part of the libhpc projects 
# (http://www.imperial.ac.uk/lesc/projects/libhpc).
#
# We gratefully acknowledge the Engineering and Physical Sciences Research
# Council (EPSRC) for their support of the projects:
#   - libhpc: Intelligent Component-based Development of HPC Applications
#     (EP/I030239/1).
#   - libhpc Stage II: A Long-term Solution for the Usability, Maintainability
#     and Sustainability of HPC Software (EP/K038788/1).
'''
File created on Jan 9, 2014

@author: jhc02
'''
# Wrapper module that provides Picard tools as functions

from subprocess import call
import os
import shutil

picard_exec = '/usr/local/bio/picard-tools-1.107'

def set_picard_exec(picard_location):
    global picard_exec
    picard_exec = picard_location

def get_picard_exec():
    return picard_exec

def add_read_groups(input_file, rgid, rglb, rgpl, rgpu, rgsm, output_file=None):
    # AddOrReplaceReadGroups.jar INPUT=ERR018562_pe_sorted.bam OUTPUT=ERR018562_pe_sorted_tagged.bam RGID=1 RGLB=ZAP430 RGPL=ILLUMINA RGPU='Lane 1' RGSM='ZAP430'
    if output_file == None:
        if type(input_file) == type(tuple()):
            input_file = input_file[0]
        output_file = input_file.rsplit('.',1)[0] + '_TAGGED.bam'
    if rglb == None:
        rglb = ''
    if rgsm == None:
        rgsm = ''
    print '\tPICARD - AddOrReplaceReadGroups...\n'
    status = call(['java', '-jar', os.path.join(picard_exec,'AddOrReplaceReadGroups.jar'), 'INPUT='+input_file, 'OUTPUT='+output_file, 'RGID='+str(rgid), 'RGLB='+rglb, 'RGPL='+rgpl, 'RGPU='+rgpu, 'RGSM='+rgsm])
    print '\tPICARD - AddOrReplaceReadGroups...DONE...Status code: ' + str(status) + '\n\n'
    return output_file
    
def merge_sam(input_list, output_file = None):
    print '\tPICARD - MergeSamFiles...\n'
    if output_file == None:
        output_file = input_list[0].rsplit('.',1)[0] + '_MERGED.bam'
    
    command_list = ['java', '-jar', os.path.join(picard_exec,'MergeSamFiles.jar')]
    
    for input_value in input_list:
        print '\tPICARD - MergeSamFiles - Input value: INPUT=' + input_value + '\n'
        command_list.append('INPUT='+input_value)
         
    command_list.append('OUTPUT='+output_file)
    status = call(command_list)
    print '\tPICARD - MergeSamFiles...DONE...Status code: ' + str(status) + '\n\n'

    return (output_file)
    
def create_dictionary(ref_genome_file, output_file = None):
    print '\tPICARD CreateSequenceDictionary...\n'
    if output_file == None:
        output_file = ref_genome_file.rsplit('.',1)[0] + '.dict'
    
    # Check if the output file exists, if it does, rename it to .old
    if os.path.exists(output_file):
        shutil.move(output_file, output_file + '.old')
    status = call(['java', '-jar', os.path.join(picard_exec,'CreateSequenceDictionary.jar'), 'R=' + ref_genome_file, 'O=' + output_file])
    print '\tPICARD CreateSequenceDictionary...DONE...Status code: ' + str(status) + '\n\n'
    return (status, output_file)

def build_bam_index(input_file, output_file=None):
    print '\tPICARD BuildBamIndex...\n'
    if output_file == None:
        output_file = input_file.rsplit('.',1)[0] + '.bai'
    status = call(['java', '-jar', os.path.join(picard_exec, 'BuildBamIndex.jar'), 'INPUT='+input_file, 'OUTPUT='+output_file])
    print '\tPICARD BuildBamIndex...DONE...Status code: ' + str(status) + '\n\n'
    return (status, output_file)

def mark_duplicates(input_file, output_file = None, metrics_file = None, remove_duplicates = False):
    print '\tPICARD MarkDuplicates...\n'
    if output_file == None:
        output_file = input_file.rsplit('.',1)[0] + '_marked.' + input_file.rsplit('.',1)[1]
    if metrics_file == None:
        metrics_file = input_file.rsplit('.',1)[0] + '_marked.metrics'
    
    status = call(['java', '-jar', os.path.join(picard_exec, 'MarkDuplicates.jar'), 'INPUT='+input_file, 'OUTPUT='+output_file, 'METRICS_FILE='+metrics_file, 'REMOVE_DUPLICATES='+str(remove_duplicates)])
    print '\tPICARD MarkDuplicates...DONE...Status code: ' + str(status) + '\n\n'
    return (status, output_file, metrics_file)

def remove_duplicates(input_file, output_file = None, metrics_file = None):
    if output_file == None:
        output_file = input_file.rsplit('.',1)[0] + '_NODUP.' + input_file.rsplit('.',1)[1]
    return mark_duplicates(input_file, output_file=output_file, metrics_file=metrics_file, remove_duplicates=True)

def check_rename_reference(ref_genome_file, output_file = None):
    if (ref_genome_file.rsplit('.',1)[1] != 'fa') and (ref_genome_file.rsplit('.',1)[1] != 'fasta'):
        print "Provided FASTA input file <" + str(ref_genome_file) + "> doesn't have a compatible extension - .fa or .fasta, creating copy with .fa extension."
        output_file = ref_genome_file.rsplit('.',1)[0] + '.fa'
        shutil.copy(ref_genome_file, output_file)
        return (output_file, )
    else:
        return (ref_genome_file, )
