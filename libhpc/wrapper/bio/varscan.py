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
# Module that provides BWA tools as functions

from subprocess import call

bwa_exec = '/Users/jhc02/tmp/bio/bwa-0.6.2/bwa'

def set_bwa_exec(bwa_location):
    global bwa_exec
    bwa_exec = bwa_location

def get_bwa_exec():
    return bwa_exec

def index(ref_genome_file, output_file = None):
    print '\tBWA index...\n'
    status = call([bwa_exec, 'index', ref_genome_file])
    print '\tBWA index...DONE...Status code: ' + str(status) + '\n\n'
    return status
    
def align(ref_genome_file, short_read_file, output_file = None):
    print '\tBWA align...\n'
    if output_file == None:
        output_file = short_read_file.rsplit('.',1)[0] + '.sai'
    status = call([bwa_exec, 'aln', '-f', output_file, ref_genome_file, short_read_file])
    print '\tBWA align...DONE...Status code: ' + str(status) + '\n\n'
    return (status, output_file)
    
def sampe(ref_genome_file, short_read_alignment_indexes, short_read_files, sam_output_file = None):
    print '\tBWA sampe...\n'
    # If an output file name is not provided, calculate one based on short read file name
    if sam_output_file == None:
        sam_output_file = short_read_files[0].rsplit('.',1)[0].rsplit('_',1)[0] + '.sam'
    status = call([bwa_exec, 'sampe', '-f', sam_output_file, ref_genome_file, short_read_alignment_indexes[0], short_read_alignment_indexes[1], short_read_files[0], short_read_files[1]])
    print '\tBWA sampe...DONE...Status code: ' + str(status) + '\n\n'
    return (status, sam_output_file)