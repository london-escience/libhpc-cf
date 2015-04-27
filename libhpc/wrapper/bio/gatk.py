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
from subprocess import check_output
import os
import platform

gatk_location = '/usr/local/bio/gatk/GenomeAnalysisTK.jar'
java_exec = 'java'     

def init_java():
    global java_exec
    
    this_system = platform.system()

    if 'Darwin' in this_system:
        print "Running on a Mac, setting java exec to the correct JAVA_HOME location"
        java_home = check_output(['/usr/libexec/java_home']).strip()
        java_exec = os.path.join(java_home, 'bin', 'java')
        print 'New java executable value: ' + java_exec



def set_gatk_location(location):
    global gatk_location
    gatk_location = location

def get_gatk_location():
    return gatk_location
    
def create_realigner_targets(ref_genome_file, bam_file, output_file = None):
    init_java()
    
    print '\tGenome Analysis ToolKit - Realigner Target Creator...[' + java_exec + ' -jar ' + gatk_location + ']\n'
    if output_file == None:
        output_file = bam_file.rsplit('.',1)[0] + '.intervals'
    status = call([java_exec, '-jar', gatk_location, '-T', 'RealignerTargetCreator', '-R', ref_genome_file, '-I', bam_file, '-o', output_file])
    print '\tGenome Analysis ToolKit - Realigner Target Creator...DONE...Status code: ' + str(status) + '\n\n'
    #return (status, output_file)
    return (status, output_file)

def create_realigner_targets_with_pre_processing(ref_genome_file, bam_file, output_file = None):
    init_java()
    
    # TODO: Check approach of this extra function
    # Check if the provided ref_genome_file has a .fa or .fasta extension.
    # If it doesn't, we create a copy that has the correct extension for gatk
    # and then run the pre-processing.
    # TODO: ???? - is this the correct approach? It results in dependecies on
    # other processes. Maybe these dependecies should be made explicit by doing
    # this thorugh the co-ordination forms element of the code? 
    
    print '\tGenome Analysis ToolKit - Realigner Target Creator...[' + java_exec + ' -jar ' + gatk_location + ']\n'
    if output_file == None:
        output_file = bam_file.rsplit('.',1)[0] + '.intervals'
    status = call([java_exec, '-jar', gatk_location, '-T', 'RealignerTargetCreator', '-R', ref_genome_file, '-I', bam_file, '-o', output_file])
    print '\tGenome Analysis ToolKit - Realigner Target Creator...DONE...Status code: ' + str(status) + '\n\n'
    #return (status, output_file)
    return (output_file)


def indel_realigner(ref_genome_file, bam_file, target_intervals, output_file = None):
    init_java()
    
    print '\tGenome Analysis ToolKit - Indel Realigner...\n'
    if output_file == None:
        output_file = bam_file.rsplit('.',1)[0] + '_REALIGNED.' + bam_file.rsplit('.',1)[1] 
    status = call([java_exec, '-jar', gatk_location, '-T', 'IndelRealigner', '-R', ref_genome_file, '-I', bam_file, '-targetIntervals', target_intervals, '-o', output_file])
    print '\tGenome Analysis ToolKit - Indel Realigner...DONE...Status code: ' + str(status) + '\n\n'
    return (status, output_file)

def base_recalibrator(ref_genome_file, bam_file, known_sites_file, output_file = None):
    init_java()
    
    print '\tGenome Analysis ToolKit - Base Recalibrator...\n'
    if output_file == None:
        output_file = bam_file.rsplit('.',1)[0] + '_recal.table' 
    status = call([java_exec, '-jar', gatk_location, '-T', 'BaseRecalibrator', '-R', ref_genome_file, '-I', bam_file, '-knownSites:VCF', known_sites_file, '-o', output_file])
    print '\tGenome Analysis ToolKit - Base Recalibrator...DONE...Status code: ' + str(status) + '\n\n'
    return (status, output_file)

def print_reads(ref_genome_file, bam_file, recalibration_table_file, output_file = None):
    init_java()
    
    print '\tGenome Analysis ToolKit - Print Reads...\n'
    if output_file == None:
        output_file = bam_file.rsplit('.',1)[0] + '_final.' + bam_file.rsplit('.',1)[1] 
    status = call([java_exec, '-jar', gatk_location, '-T', 'PrintReads', '-BQSR', recalibration_table_file, '-R', ref_genome_file, '-I', bam_file, '-o', output_file])
    print '\tGenome Analysis ToolKit - PrintReads...DONE...Status code: ' + str(status) + '\n\n'
    return (status, output_file)
