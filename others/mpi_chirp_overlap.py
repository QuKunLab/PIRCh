#!/usr/bin/python

import os
import re
import numpy as np
from mpi4py import MPI

def single(rank):

    os.popen('mkdir ' + all_files[rank][:-4])
    os.popen('for a in `find ../Chip_V65/H* -maxdepth 0`; do bedtools intersect -a ' + all_files[rank] +  ' -b $a/test_peaks.narrowPeak | wc -l > ' + all_files[rank][:-4] + '/${a##*/}.num.txt; done')
    os.popen('for a in `find ../Chip_V65/H* -maxdepth 0`; do bedtools intersect -a ' + all_files[rank] +  ' -b $a/test_peaks.narrowPeak | awk \'{sum+=$3-$2}END{print sum}\' > ' + all_files[rank][:-4] + '/${a##*/}.length.txt; done')
    os.popen('python ~/scripts/ChIRP_overlap.py ' + all_files[rank] + ' /home/icshape/seq/chromosome/mm9/mm9_nochrM.sizes ../Chip_V65/Bedgraph/**.bedGraph ' + all_files[rank][:-4] +'/' + all_files[rank][:-4] + '.scale_result.txt')
    os.popen('python ~/scripts/ChIRP_Expand.py ' + all_files[rank] + ' /home/icshape/seq/chromosome/mm9/mm9_nochrM.sizes ../Chip_V65/Bedgraph/**.bedGraph ' + all_files[rank][:-4] +'/' + all_files[rank][:-4] + '.expan_result.txt')
    return


read_dir_name = '/home/fangjingwen/Pirch/other_data/V65_Lnc'
all_files = os.listdir(read_dir_name)
all_files = [x for x in all_files if x[-4:]==".bed"]
comm = MPI.COMM_WORLD
nsize = comm.Get_size()
rank = comm.Get_rank()
single(rank)
#for rank in range(0, cell_number):
#    single(rank)
#
