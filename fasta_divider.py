from Bio import SeqIO


def divide(filename):
    cov_sequences = list(SeqIO.parse(filename, "fasta"))  # reading all sequences in file
    print("File %s contains %d sequences" % (filename, len(cov_sequences)))
    offset = 10  # offset which will be used to extract substring ISL_XXXXXX
    for sequence in cov_sequences:
        code_start = sequence.description.find("ISL")  # find index where ISL is
        sequence_code = sequence.description[code_start:code_start + offset]  # get substring ISL_XXXXXX
        sequence.id = sequence_code  # update sequence object
        sequence.description = sequence_code
        SeqIO.write(sequence, "data/input_sequences/" + sequence_code + ".fasta", "fasta")  # write sequence to a single fasta file with name
        # ISL_XXXXXX.fasta
