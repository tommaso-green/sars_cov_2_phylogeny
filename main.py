import stretcher
import fdnadist
import time
import shutil
import os
import subprocess
from Bio.Emboss.Applications import FNeighborCommandline


def cleanup():
    folders = ["test_sequences/matrices", "test_sequences/out"]
    for f in folders:
        shutil.rmtree(f)
        os.makedirs(f)
        print("Deleted alignments and matrices of previous run")
    if os.path.exists("test_sequences/final_matrix.phy"):
        os.remove("test_sequences/final_matrix.phy")
        print("Deletion of previous matrix file completed")
    else:
        print("The matrix file does not exist")


def create_tree():
    os.chdir("test_sequences")
    neighbor_line = FNeighborCommandline()
    neighbor_line.datafile = "final_matrix.phy"
    neighbor_line.matrixtype = "l"
    neighbor_line.treetype = "n"
    neighbor_line.outfile = "outtree"
    subprocess.Popen(str(neighbor_line()), shell=True)


def main():
    cleanup()
    start = time.time()
    num_sequences = len(os.listdir("test_sequences/input_sequences"))
    print("Starting procedure for %d sequences." % num_sequences)
    stretcher.align(num_sequences)
    fdnadist.compute_pairwise_matrices()
    fdnadist.create_final_matrix(num_sequences)
    final = time.time() - start
    print("Done in %d minutes and %d seconds" % (divmod(final, 60)))


# main()

create_tree()
