import getopt
import os
import shutil
import subprocess
import sys
import time

from Bio.Emboss.Applications import FNeighborCommandline

import fasta_divider
import fdnadist
import stretcher


def cleanup():
    folders = ["data/input_sequences", "data/matrices", "data/alignments"]
    for f in folders:
        shutil.rmtree(f)  # deleting the folders
        os.makedirs(f)  # recreating them
    print("Deleted input sequences, alignments and matrices of previous run (if there were any)")
    if os.path.exists("data/final_matrix.phy"):
        os.remove("data/final_matrix.phy")
        print("Deletion of previous matrix file completed")
    if os.path.exists("data/tree_output/pairwisetree_visual"):
        os.remove("data/tree_output/pairwisetree_visual")
        print("Deletion of previous tree visualization file completed")
    if os.path.exists("data/tree_output/pairwisetree.nwk"):
        os.remove("data/tree_output/pairwisetree.nwk")
        print("Deletion of previous Newick tree file completed")


def create_tree():
    neighbor_line = FNeighborCommandline()
    neighbor_line.datafile = "data/final_matrix.phy"
    neighbor_line.matrixtype = "l"  # lower triangular distance matrix
    neighbor_line.treetype = "n"  # neighbor joining algorithm
    neighbor_line.outfile = "data/tree_output/pairwisetree_visual"
    neighbor_line.outtreefile = "data/tree_output/pairwisetree.nwk"
    subprocess.Popen(str(neighbor_line()), shell=True)


def main():
    cleanup()
    for filename in os.listdir("fasta_files"):  # dividing all fastas
        fasta_divider.divide("fasta_files/" + filename)  # and exporting them to data/input_sequences
    argument_list = sys.argv[1:]
    short_options = "n:"
    long_options = ["no_seq"]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)
    for current_argument, current_value in arguments:
        if current_argument in ("-n", "no_seq"):
            if current_value.isdigit():
                num_sequences = int(current_value)
            elif current_value == "all":
                num_sequences = len(os.listdir("data/input_sequences"))
            else:
                print("Invalid number of sequences.")
                raise ValueError
    start = time.time()
    print("Starting procedure for %d sequences." % num_sequences)
    stretcher.align(num_sequences)  # aligning sequences using stretcher
    fdnadist.create_final_matrix(num_sequences)  # computing distance matrix
    create_tree()  # creating phylogenetic tree using neighbor
    final = time.time() - start
    print("Done in %d minutes and %d seconds" % (divmod(final, 60)))


if __name__ == "__main__":
    main()