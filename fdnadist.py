import os
import subprocess
from itertools import combinations
from Bio.Emboss.Applications import FDNADistCommandline




def compute_matrices():
    alignments = os.listdir("test_sequences/out")
    fline = FDNADistCommandline()
    fline.method = "f"
    fline.stdout = True
    processes = []
    i = 1
    for alignment in alignments:
        fline.sequence = "test_sequences/out/" + alignment
        fline.outfile = alignment[:24] + "_matrix"
        print(str(fline))
        proc = subprocess.Popen(str(fline) + " -odirectory2 test_sequences/matrices ", shell=True)
        processes.append((i, proc))
        print(proc.stderr)
        i += 1

    while processes:
        for proc in processes:
            if proc[1].poll() is not None:
                processes.remove(proc)
                print("Done alignment %d" % (proc[0]))


def get_distances():
    os.chdir("test_sequences/matrices")
    matrix_files = os.listdir()
    dict = {}
    for filename in matrix_files:
        f = open(filename, "r+")
        line = f.readlines()[2]
        dict[filename[:24]] = line.split(" ")[1]
    f.close()
    return dict


def get_distances_by_name(name, distances):
    tmp = [element for element in list(distances.items()) if element[0].find(name) != -1]
    for i in range(len(tmp)):
        pair = tmp[0]
        involved_sequences = pair[0].split("_vs_")
        other_sequence = [sequence for sequence in involved_sequences if sequence != name][0]
        tmp.append((other_sequence, pair[1]))
        tmp.remove(pair)
    return tmp


def create_final_matrix(num_sequences):
    distances = get_distances()
    os.chdir("..")
    sequences = [sequence_filename.split(".")[0] for sequence_filename in
                 os.listdir("input_sequences")[:num_sequences]]
    combos = list(combinations(sequences, 2))
    out_file = open("final_matrix.phy", "w+")
    # out_file.write(str(len(sequences)) + "\n")
    lines = []
    i = 1
    for sequence in reversed(sequences):
        print("Sequence Name : %s" % (sequence))
        dist_value = get_distances_by_name(sequence, distances)
        dist_value.sort(key=lambda x: sequences.index(x[0]))
        s = sequence
        for element in dist_value[:num_sequences-i]:
            s += " " + str(element[1])
        i += 1
        lines.append(s + "\n")
    lines.append(str(len(sequences)) + "\n")
    out_file.writelines(reversed(lines))
    out_file.close()


