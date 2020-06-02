import os
import subprocess
from itertools import combinations
from Bio.Emboss.Applications import FDNADistCommandline


def compute_pairwise_matrices():
    alignments = os.listdir("data/alignments")  # get list of all pairwise alignments previously completed
    fline = FDNADistCommandline()  # create FDNADist object
    fline.method = "f"
    fline.stdout = True
    processes = []
    matrix_id = 1
    end_filename = 24  # filename end before ".phy", see below
    for alignment in alignments:
        fline.sequence = "data/alignments/" + alignment  # set sequence parameter
        fline.outfile = alignment[:end_filename] + "_matrix"  # to get string ISL_XXXXXX_vs_ISL_YYYYYY_matrix
        print(str(fline))
        p = subprocess.Popen(str(fline) + " -odirectory2 data/matrices ",
                             shell=True)  # launching subprocess
        processes.append((matrix_id, p))  # appending to process list
        matrix_id += 1

    while processes:
        for proc in processes:
            if proc[1].poll() is not None:  # if process is completed
                processes.remove(proc)  # remove it
                print("Done matrix %d" % (proc[0]))


def get_distances():
    matrix_files = os.listdir("data/matrices")  # get list of all matrix files
    distance_dict = {}  # data structure to save all pairwise distances
    end_filename = 24  # filename end before ".phy"
    for filename in matrix_files:
        f = open("data/matrices/" + filename, "r+")  # open matrix file
        line = f.readlines()[2]  # get third line
        distance_dict[filename[:end_filename]] = line.split(" ")[1]  # get element in position (1,1)
        f.close()
    return distance_dict


def get_distances_by_name(name, distances):
    compared_sequences = [element for element in list(distances.items()) if element[0].find(name) != -1]
    # comp_seq is the list of all (pair, distance between pair) where the pair contains the sequence in name argument
    output = []
    for sequence in compared_sequences:
        # remember that sequence is [ISL_XXXXXX_vs_ISL_YYYYYY, dist]
        involved_sequences = sequence[0].split("_vs_")  # [ISL_XXXXXX, ISL_YYYYYY]
        other_sequence = [sequence for sequence in involved_sequences if sequence != name][0]  # get the other
        # sequence compared to name sequence
        output.append((other_sequence, sequence[1]))
    return output


def create_final_matrix(num_sequences):
    compute_pairwise_matrices()
    distances = get_distances()  # get dictionary of all pairwise distances
    sequences = [sequence_filename.split(".")[0] for sequence_filename in
                 os.listdir("data/input_sequences")[:num_sequences]]  # get list of all sequences (up to num_sequences)
    out_file = open("data/final_matrix.phy", "w+")  # open file which will contain final matrix in low triangular form
    lines = []
    i = 1
    for sequence in reversed(sequences):  # last sequence will be the last line of matrix made of n - 1 entries
        print("Sequence Name : %s" % sequence)
        dist_list = get_distances_by_name(sequence, distances)  # get all distances
        dist_list.sort(key=lambda x: sequences.index(x[0]))  # sort them by compared sequence
        s = sequence
        for element in dist_list[:num_sequences - i]:  # append n - i entries to string name
            s += " " + str(element[1])
        i += 1
        lines.append(s + "\n")  # insert newly created string + NL
    lines.append(str(len(sequences)) + "\n")  # append first line made of n + NL
    out_file.writelines(reversed(lines))  # rewrite them in reversed order
    out_file.close()
