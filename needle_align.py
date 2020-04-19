from Bio import SeqIO, AlignIO, Align
from Bio.Emboss.Applications import NeedleCommandline
from itertools import combinations
import subprocess
import time


# EPI_ISL_417921
# EPI_ISL_419255

def replace_words(file_content, substitutions):
    for key, val in substitutions.items():
        file_content = file_content.replace(key, val)
    return file_content


def reformat_file(filename, substitutions):
    file = open(filename, 'r')
    file_content = file.read()
    file.close()
    fixed_test = replace_words(file_content, substitutions)
    new_file = open(filename, "w")
    new_file.write(fixed_test)
    new_file.close()


cov_sequences = ["EPI_ISL_417921", "EPI_ISL_419255", "EPI_ISL_419531", "EPI_ISL_419552"]
combos = list(combinations(cov_sequences, 2))
needle_cline = NeedleCommandline()
substitutions = {"EMBOSS_001": "", "EMBOSS_002": ""}
pairs_completed = 1
start_time = 0
execution_start_time = time.time()
for pair in combos:
    start_time = time.time()
    needle_cline.asequence = pair[0] + ".fasta"
    needle_cline.bsequence = pair[1] + ".fasta"
    needle_cline.gapopen = 10
    needle_cline.gapextend = 0.5
    codename_a = pair[0][4:]
    codename_b = pair[1][4:]
    substitutions["EMBOSS_001"] = codename_a
    substitutions["EMBOSS_002"] = codename_b
    needle_cline.outfile = codename_a + "_vs_" + codename_b + ".phy"
    needle_cline.aformat = "phylip"
    stdout, stderr = needle_cline()
    print(stdout + stderr)
    reformat_file(needle_cline.outfile, substitutions)
    finish_time = time.time()
    time_required = finish_time - start_time
    mins, secs = divmod(time_required, 60)
    print("*** Completed Alignment %d %s vs %s in %d minutes and %d seconds ***" % (
        pairs_completed, codename_a, codename_b, mins, secs))
    print(".....Total Time Elapsed: %d minutes and %d seconds....." % (divmod(finish_time - execution_start_time, 60)))
    pairs_completed += 1

print("###### TASK COMPLETED in %d minutes and %d seconds" % (divmod(time.time() - execution_start_time, 60)))
print("--------Done-------")
