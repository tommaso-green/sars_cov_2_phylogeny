import stretcher
import fdnadist
import time
import shutil
import os

def cleanup():
    folders = ["test_sequences/matrices", "test_sequences/out"]
    for f in folders:
        shutil.rmtree(f)
        os.makedirs(f)
    if os.path.exists("final_matrix.phy"):
        os.remove("final_matrix.phy")
    else:
        print("The matrix file does not exist")




def main():
    #cleanup()
    start = time.time()
    num_sequences = 23
    stretcher.align(num_sequences)
    fdnadist.compute_matrices()
    fdnadist.create_final_matrix(num_sequences)
    final = time.time() - start
    print("Done in %d minutes and %d seconds" % (divmod(final, 60)))



main()
