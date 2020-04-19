from Bio import SeqIO
import os


cov_sequences = list(SeqIO.parse("mixed.fasta", "fasta"))
print(len(cov_sequences))
os.chdir("test_sequences/input_sequences")
for sequence in cov_sequences:
    code_start = sequence.description.find("ISL")
    sequence_code = sequence.description[code_start:code_start+10]
    sequence.id = sequence_code
    sequence.description = sequence_code
    SeqIO.write(sequence, sequence_code + ".fasta", "fasta")
