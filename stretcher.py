import subprocess
import time
import os
from itertools import combinations

from Bio.Emboss.Applications import StretcherCommandline


def align(num_sequences):  # specify number of sequences in input_sequences folder
    cov_sequences = os.listdir("data/input_sequences")[:num_sequences]  # retrieve names of sequences from
    # folder
    combos = list(combinations(cov_sequences, 2))  # create a list of all n-choose-2 combinations of sequences
    total_alignments = len(combos)
    stretch_cline = StretcherCommandline()  # create a Stretcher Command Line object which will be used later on for
    # all pairwise alignments
    pairs_completed = 0
    execution_start_time = time.time()  # get initial start time
    processes = []  # create an empty list where all parallel alignment processes will be stored
    pairs_started = 0
    limit = 7  # limit of parallel process per batch
    batch_number = 0
    while pairs_started < total_alignments:
        batch_number += 1
        batch_size = len(combos[pairs_started:pairs_started + limit])
        for pair in combos[pairs_started:pairs_started + limit]:
            stretch_cline.asequence = "data/input_sequences/" + pair[0]
            stretch_cline.bsequence = "data/input_sequences/" + pair[1]
            stretch_cline.gapopen = 16  # standard value from documentation
            stretch_cline.gapextend = 4  # standard value from documentation
            codename_a = pair[0][:10]
            codename_b = pair[1][:10]
            filename = codename_a + "_vs_" + codename_b + ".phy"
            stretch_cline.outfile = filename
            stretch_cline.aformat = "phylip"  # output format of alignment file
            full_command = str(stretch_cline) + " -sid1=" + codename_a + " -sid2=" + codename_b  # terminal command
            full_command += " -adirectory3 data/alignments"  # specifying output directory
            proc = subprocess.Popen(full_command, shell=True)  # launching subprocess
            start_time = time.time()  # start time for considered alignment
            pairs_started += 1
            processes.append((proc, "*** Completed Alignment %d %s vs %s ***" % (
                pairs_started, codename_a, codename_b), start_time))  # storing proc,completion_string, and start time

        while processes:
            for element in processes:
                if element[0].poll() is not None:  # if processes is finished
                    print(element[1] + " in %d minutes and %d seconds" % (divmod(time.time() - element[2], 60)))
                    pairs_completed += 1
                    print("Completed %d/%d Alignments \n" % (pairs_completed, total_alignments))
                    processes.remove(element)  # removing element from process list
        print("---> Processing of Batch %d of %d pairs completed!" % (batch_number, batch_size))

    print(
        "###### TASK COMPLETED in %d minutes and %d seconds ######" % (divmod(time.time() - execution_start_time, 60)))
    print("@@@@@@@@@@-------- ALL ALIGNMENTS DONE --------@@@@@@@@@@")
