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
File created on Aug 7, 2012

@author: jhc02
'''
# Samtools module provides functions for various samtools operations

from subprocess import call

samtools_exec = '/usr/local/bio/samtools-0.1.19/samtools' 
bcftools_exec = '/usr/local/bio/samtools-0.1.19/bcftools/bcftools' 

def set_samtools_exec(samtools_location):
    global samtools_exec
    samtools_exec = samtools_location

def get_samtools_exec():
    return samtools_exec

def import_sam(ref_genome_file, sam_file, bam_file = None):
    if bam_file == None:
        bam_file = sam_file.rsplit('.',1)[0] + '.bam'
    print '\tSAM import...\n'
    status = call([samtools_exec, 'import', ref_genome_file, sam_file, bam_file])
    print '\tSAM import...DONE...Status code: ' + str(status) + '\n\n'
    return (status, bam_file)
    
def sort(bam_input_file, sorted_output_file = None):
    if sorted_output_file == None:
        # Suffix is automatically added by sort
        sorted_output_file = bam_input_file.rsplit('.',1)[0] + '_SORTED'
    else:
        sorted_output_file = bam_input_file.rsplit('.',1)[0]
    print '\tSAM sort...\n'
    status = call([samtools_exec, 'sort', bam_input_file, sorted_output_file])
    print '\tSAM sort...DONE...Status code: ' + str(status) + '\n\n'
    return (status, sorted_output_file + '.bam')

def index(input_file, output_file = None):
    if output_file == None:
        output_file = input_file.rsplit('.',1)[0] + '.bai'
    print '\tSAM index...\n'
    status = call([samtools_exec, 'index', input_file, output_file])
    print '\tSAM index...DONE...Status code: ' + str(status) + '\n\n'
    return (status, output_file)

def faidx(input_file, output_file = None):
    if output_file == None:
        output_file = input_file.rsplit('.',1)[0] + '.fai'
    print '\tsamtools FA idx...\n'
    status = call([samtools_exec, 'faidx', input_file, output_file])
    print '\tsamtools faidx...DONE...Status code: ' + str(status) + '\n\n'
    return (status, output_file)

def mpileup(input_file, output_file = None):
    if output_file == None:
        output_file = input_file.rsplit('.',1)[0] + '.bcf'
    output_file_handle = open(output_file,'w')
    print '\tsamtools mpileup...\n'
    status = call([samtools_exec, 'mpileup', '-u', input_file], stdout=output_file_handle)
    output_file_handle.close()
    print '\tsamtools mpileup...DONE...Status code: ' + str(status) + '\n\n'
    return (status, output_file)

def bcf2vcf(input_file, output_file = None):
    if output_file == None:
        output_file = input_file.rsplit('.',1)[0] + '.vcf'
    output_file_handle = open(output_file,'w')
    print '\tbcftools view...\n'
    status = call([bcftools_exec, 'view', input_file], stdout=output_file_handle)
    output_file_handle.close()
    print '\tbcftools view...DONE...Status code: ' + str(status) + '\n\n'
    return (status, output_file)

