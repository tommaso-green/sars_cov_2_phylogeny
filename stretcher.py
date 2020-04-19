import subprocess
import time
import os
from itertools import combinations

from Bio.Emboss.Applications import StretcherCommandline


def align(num_sequences):
    cov_sequences = os.listdir("test_sequences/input_sequences")[:num_sequences]
    combos = list(combinations(cov_sequences, 2))
    total_alignments = len(combos)
    stretch_cline = StretcherCommandline()
    pairs_completed = 0
    start_time = 0
    execution_start_time = time.time()
    processes = []
    i = 1
    for pair in combos:
        stretch_cline.asequence = "test_sequences/input_sequences/" + pair[0]
        stretch_cline.bsequence = "test_sequences/input_sequences/" + pair[1]
        stretch_cline.gapopen = 10
        stretch_cline.gapextend = 1
        codename_a = pair[0][:10]
        codename_b = pair[1][:10]
        filename = codename_a + "_vs_" + codename_b + ".phy"
        stretch_cline.outfile = filename
        stretch_cline.aformat = "phylip"
        full_command = str(stretch_cline) + " -sid1=" + codename_a + " -sid2=" + codename_b
        full_command += " -adirectory3 test_sequences/out"
        proc = subprocess.Popen(full_command, shell=True)
        start_time = time.time()
        processes.append((proc, "*** Completed Alignment %d %s vs %s ***" % (
            i, codename_a, codename_b), start_time))
        i += 1

    while processes:
        for element in processes:
            if element[0].poll() is not None:
                print(element[1] + " in %d minutes and %d seconds" % (divmod(time.time() - element[2], 60)))
                pairs_completed += 1
                print("Completed %d/%d Alignments \n" % (pairs_completed, total_alignments))
                processes.remove(element)

    print(
        "###### TASK COMPLETED in %d minutes and %d seconds ######" % (divmod(time.time() - execution_start_time, 60)))
    print("--------Done-------")
