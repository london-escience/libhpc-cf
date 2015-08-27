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
from libhpc.cf.params import Parameter
from libhpc.cf.component import Component

# COMPONENT PARAMETER DEFINITIONS

fastq_split_input = Parameter('fastq_split_input', 'string', 'input', False)
fastq_split_output1 = Parameter('fastq_split_output1', 'string', 'inout', False)
fastq_split_output2 = Parameter('fastq_split_output2', 'string', 'inout', False)

bwa_index_param1 = Parameter('ref_genome_param', 'string', 'input', False)
bwa_index_output_file = Parameter('ref_genome_param', 'string', 'input', False)
bwa_index_result = Parameter('ref_genome_status', 'int', 'output', True)

bwa_aln_ref_genome = Parameter('ref_genome_param', 'string', 'input', False)
bwa_aln_short_read = Parameter('short_read_file', 'string', 'input', False)
bwa_aln_output_file = Parameter('output_file', 'string', 'inout', False)
bwa_aln_result = Parameter('bwa_aln_status', 'int', 'output', True)

bwa_sampe_param1 = Parameter('ref_genome_param', 'string', 'input', False)
bwa_sampe_param2 = Parameter('short_read_indexes_param', 'list', 'input', False)
bwa_sampe_param3 = Parameter('short_read_file_param', 'list', 'input', False)
bwa_sampe_output_file = Parameter('sam_output_file', 'string', 'output', False)
bwa_sampe_result = Parameter('bwa_sample_status', 'int', 'output', True)

samtools_import_param1 = Parameter('ref_genome_param', 'string', 'input', False)
samtools_import_param2 = Parameter('sam_file_param', 'string', 'input', False)
samtools_import_output = Parameter('bam_file_param', 'string', 'inout', False)
samtools_import_result = Parameter('samtools_import_status', 'int', 'output', True)

samtools_sort_baminput = Parameter('samtools_bam_input_param', 'string', 'input', False)
samtools_sort_sortedoutput = Parameter('samtools_sorted_output_param', 'string', 'output', False)
samtools_sort_result = Parameter('samtools_sort_status', 'int', 'output', True)

samtools_index_input = Parameter('samtools_index_input_param', 'string', 'input', False)
samtools_index_output = Parameter('samtools_index_output_param', 'string', 'output', False)
samtools_index_result = Parameter('samtools_index_status', 'string', 'output', True)

samtools_faidx_input = Parameter('samtools_faidx_input_param', 'string', 'input', False)
samtools_faidx_output = Parameter('samtools_faidx_output_param', 'string', 'output', False)
samtools_faidx_result = Parameter('samtools_faidx_status', 'string', 'output', True)

samtools_mpileup_input = Parameter('samtools_mpileup_input_param', 'string', 'input', False)
samtools_mpileup_output = Parameter('samtools_mpileup_output_param', 'string', 'inout', False)
samtools_mpileup_result = Parameter('samtools_mpileup_status', 'string', 'output', True)

samtools_bcf2vcf_input = Parameter('samtools_bcf2vcf_input_param', 'string', 'input', False)
samtools_bcf2vcf_output = Parameter('samtools_bcf2vcf_output_param', 'string', 'inout', False)
samtools_bcf2vcf_result = Parameter('samtools_bcf2vcf_status', 'string', 'output', True)

picard_remove_duplicates_input = Parameter('picard_remove_duplicates_input', 'string', 'input', False)
picard_remove_duplicates_output = Parameter('picard_remove_duplicates_output', 'string', 'inout', False)
picard_remove_duplicates_metrics = Parameter('picard_remove_duplicates_metrics', 'string', 'inout', False)
picard_remove_duplicates_result = Parameter('picard_remove_duplicates_result', 'int', 'output', True)

picard_add_read_groups_baminput = Parameter('add_read_groups_input_param', 'string', 'input', False)
picard_add_read_groups_rgidinput = Parameter('add_read_groups_rgid_param', 'string', 'input', False)
picard_add_read_groups_rglbinput = Parameter('add_read_groups_rglb_param', 'string', 'input', False)
picard_add_read_groups_rgplinput = Parameter('add_read_groups_rgpl_param', 'string', 'input', False)
picard_add_read_groups_rgpuinput = Parameter('add_read_groups_rgpu_param', 'string', 'input', False)
picard_add_read_groups_rgsminput = Parameter('add_read_groups_rgsm_param', 'string', 'input', False)
#picard_add_read_groups_result = Parameter('add_read_groups_status', 'int', 'output', False)
picard_add_read_groups_output = Parameter('add_read_groups_output_param', 'string', 'output', False)


picard_merge_sam_input = Parameter('merge_sam_input_file_list', 'list', 'input', False)
picard_merge_sam_output = Parameter('merge_sam_output_file', 'string', 'output', False)
picard_merge_sam_status = Parameter('merge_sam_status', 'int', 'output', True)

picard_create_dictionary_ref_input = Parameter('picard_create_dict_ref_input', 'string', 'input', False)
picard_create_dictionary_output = Parameter('picard_create_dict_file', 'string', 'inout', False)
picard_create_dictionary_status = Parameter('picard_create_dict_status', 'int', 'output', True)

picard_build_bam_index_input = Parameter('picard_build_bam_index_input_param', 'string', 'input', False)
picard_build_bam_index_output = Parameter('picard_build_bam_index_output_param', 'string', 'output', False)
picard_build_bam_index_result = Parameter('picard_build_bam_index_status', 'string', 'output', True)

picard_check_reference_input = Parameter('ref_genome_param', 'string', 'input', False)
picard_check_reference_output = Parameter('new_ref_genome_param', 'string', 'inout', False)

gatk_indel_targets_ref_input = Parameter('gatk_indel_targets_ref_input', 'string', 'input', False)
gatk_indel_targets_bam_input = Parameter('gatk_indel_targets_bam_input', 'string', 'input', False)
gatk_indel_targets_output = Parameter('gatk_indel_targets_output', 'string', 'inout', False)
gatk_indel_targets_status = Parameter('gatk_indel_targets_status', 'string', 'output', True)

gatk_indel_realigner_ref_input = Parameter('gatk_realigner_ref_input', 'string', 'input', False)
gatk_indel_realigner_bam_input = Parameter('gatk_realigner_bam_input', 'string', 'input', False)
gatk_indel_realigner_interval_input = Parameter('gatk_realigner_interval_input', 'string', 'input', False)
gatk_indel_realigner_output = Parameter('gatk_realigner_output', 'string', 'inout', False)
gatk_indel_realigner_status = Parameter('gatk_realigner_status', 'string', 'output', True)

gatk_base_recal_ref_genome = Parameter('gatk_recalibrator_ref_input', 'string', 'input', False)
gatk_base_recal_bam_input = Parameter('gatk_recalibrator_bam_input', 'string', 'input', False)
gatk_base_recal_known_sites = Parameter('gatk_recalibrator_known_sites_input', 'string', 'input', False)
gatk_base_recal_output = Parameter('gatk_recalibrator_output', 'string', 'inout', False)
gatk_base_recal_status = Parameter('gatk_recalibrator_status', 'string', 'output', True)

gatk_print_reads_ref_genome = Parameter('gatk_print_reads_ref_input', 'string', 'input', False)
gatk_print_reads_bam_input = Parameter('gatk_print_reads_bam_input', 'string', 'input', False)
gatk_print_reads_recal_table = Parameter('gatk_print_reads_recal_table', 'string', 'input', False)
gatk_print_reads_output = Parameter('gatk_print_reads_output', 'string', 'inout', False)
gatk_print_reads_status = Parameter('gatk_print_reads_status', 'string', 'output', True)

# COMPONENT DEFINITIONS
    
fastq_split = Component('fastq.splitter', 'Paired FASTQ File Splitter', 'libhpc.wrapper.bio.fastqsplitter.split_fastq', [fastq_split_input, fastq_split_output1, fastq_split_output2], [])

#bwa_index = Component('bwa.index', 'BWA Index', 'bwa.index', [bwa_index_param1], [bwa_index_result])
bwa_index = Component('bwa.index', 'BWA Index', 'libhpc.wrapper.bio.bwa.index', [bwa_index_param1, bwa_index_output_file], [bwa_index_result])
bwa_aln = Component('bwa.align', 'BWA Initial Alignment', 'libhpc.wrapper.bio.bwa.align', [bwa_aln_ref_genome, bwa_aln_short_read, bwa_aln_output_file], [bwa_aln_result])
bwa_sampe = Component('bwa.sampe', 'BWA Paired Alignment', 'libhpc.wrapper.bio.bwa.sampe', [bwa_sampe_param1, bwa_sampe_param2, bwa_sampe_param3, bwa_sampe_output_file], [bwa_sampe_result], 'pre')
    
samtools_import = Component('samtools.import', 'SAMtools Import', 'libhpc.wrapper.bio.samtools.import_sam', [samtools_import_param1, samtools_import_param2, samtools_import_output], [samtools_import_result], 'pre')
samtools_sort = Component('samtools.sort', 'SAMtools Sort', 'libhpc.wrapper.bio.samtools.sort', [samtools_sort_baminput, samtools_sort_sortedoutput], [samtools_import_result])
samtools_index = Component('samtools.index', 'SAMtools Index', 'libhpc.wrapper.bio.samtools.index', [samtools_index_input, samtools_index_output], [samtools_index_result])
samtools_faidx = Component('samtools.faidx', 'SAMtools faidx', 'libhpc.wrapper.bio.samtools.faidx', [samtools_faidx_input, samtools_faidx_output], [samtools_faidx_result])
samtools_mpileup = Component('samtools.mpileup', 'SAMtools mpileup', 'libhpc.wrapper.bio.samtools.mpileup', [samtools_mpileup_input, samtools_mpileup_output], [samtools_mpileup_result])
samtools_bcf2vcf = Component('samtools.bcf2vcf', 'SAMtools BCF to VCF conversion', 'libhpc.wrapper.bio.samtools.bcf2vcf', [samtools_bcf2vcf_input, samtools_bcf2vcf_output], [samtools_bcf2vcf_result])

picard_add_read_groups = Component('picard.add_read_groups', 'Picard - Add Read Groups', 'libhpc.wrapper.bio.picard.add_read_groups', [picard_add_read_groups_baminput, picard_add_read_groups_rgidinput, picard_add_read_groups_rglbinput, picard_add_read_groups_rgplinput, picard_add_read_groups_rgpuinput, picard_add_read_groups_rgsminput], [picard_add_read_groups_output]) # , picard_add_read_groups_result removed from return values    
picard_merge_sam = Component('picard.merge_sam', 'Picard - Merge SAM/BAM files', 'libhpc.wrapper.bio.picard.merge_sam', [picard_merge_sam_input], [picard_merge_sam_output])
picard_remove_duplicates = Component('picard.remove_duplicates', 'Picard - Remove Duplicates', 'libhpc.wrapper.bio.picard.remove_duplicates', [picard_remove_duplicates_input, picard_remove_duplicates_output, picard_remove_duplicates_metrics], [picard_remove_duplicates_result])
picard_create_dictionary = Component('picard.create_dictionary', 'Picard - Create Dictionary', 'libhpc.wrapper.bio.picard.create_dictionary', [picard_create_dictionary_ref_input, picard_create_dictionary_output], [picard_create_dictionary_status])
picard_build_bam_index = Component('picard.build_bam_index', 'Picard - Build BAM Index', 'libhpc.wrapper.bio.picard.build_bam_index', [picard_build_bam_index_input, picard_build_bam_index_output], [picard_build_bam_index_result])
picard_check_reference = Component('picard.check_reference', 'Check reference genome extension', 'libhpc.wrapper.bio.picard.check_rename_reference', [picard_check_reference_input, picard_check_reference_output], [])

gatk_realigner_targets = Component('gatk.realigner_targets', 'Generate realigner targets for indel processing', 'libhpc.wrapper.bio.gatk.create_realigner_targets', [gatk_indel_targets_ref_input, gatk_indel_targets_bam_input, gatk_indel_targets_output], [gatk_indel_targets_status])
gatk_indel_realigner = Component('gatk.indel_realigner', 'Realign BAM based on indels', 'libhpc.wrapper.bio.gatk.indel_realigner', [gatk_indel_realigner_ref_input, gatk_indel_realigner_bam_input, gatk_indel_realigner_interval_input, gatk_indel_realigner_output], [gatk_indel_realigner_status])    
gatk_base_recalibrator = Component('gatk.base_recalibrator', 'GATK Base Recalibrator', 'libhpc.wrapper.bio.gatk.base_recalibrator', [gatk_base_recal_ref_genome, gatk_base_recal_bam_input, gatk_base_recal_known_sites, gatk_base_recal_output], [gatk_base_recal_status], 'pre')
gatk_print_reads = Component('gatk.print_reads', 'GATK Print Reads', 'libhpc.wrapper.bio.gatk.print_reads', [gatk_print_reads_ref_genome, gatk_print_reads_bam_input, gatk_print_reads_recal_table, gatk_print_reads_output], [gatk_print_reads_status], 'pre')