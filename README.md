# Phylogenetic trees by Multiple Pairwise Alignments

This is a repo containing code for creating neighbor-joining
phylogenetic trees. It is mainly based on [Biopython](https://biopython.org) and on
[EMBOSS](http://emboss.sourceforge.net/index.html) and the usage of phylip software through the use of
the EMBASSY package [PHYLIPNEW](http://emboss.sourceforge.net/apps/release/6.6/embassy/phylipnew/) which is basically
a collection of [PHYLIP](http://evolution.genetics.washington.edu/phylip.html) applets in an EMBOSS-like environment

The execution of this software is recommended on Ubuntu due to the great ease of
installation of the dependencies.

## Installation of required software

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Biopython.

```bash
pip install biopython
```
For further installation methods, check the [Biopython Wiki](https://biopython.org/wiki/Download).

The next thing we need is EMBOSS and EMBASSY PHYLIPNEW package.
For both, the procedure on Ubuntu is straightforward.

```bash
sudo apt install emboss
sudo apt install embassy-phylip
```

If you wish to run this software on other Linux Distros:
* [EMBOSS Download and Instructions](http://emboss.sourceforge.net/download/)
* [EMBASSY PHYLIPNEW](http://emboss.sourceforge.net/embassy/) is listed here among other EMBASSY applets,
  scroll down to find the ftp link and download the tarball (instructions inside).

For Windows, to my knowledge, it is possible to download and install EMBOSS but not EMBASSY applets.
What I recommend is to install Ubuntu Windows Subsystem for Linux which is an easy install from the Microsoft Store.
For more details, check the [Ubuntu WSL Installation Guide](https://ubuntu.com/wsl).

## Pipeline

The idea of this software is to implement a pipeline that is able to create a phylogentic tree
starting from multiple pairwise alignments.
The steps are the following:
1. Look for the sequence data in fasta format in the fasta_files directory
   and for each sequence produce a separate fasta file in data/input_sequences.
   *Note*: this software assumes that the data comes from [GISAID](http://gisaid.org).
2. Compute all possible pairwise alignments of the sequences in data/input_sequences, and store them in
   data/alignments. This is done using EMBOSS [stretcher](http://emboss.sourceforge.net/apps/release/6.6/emboss/apps/stretcher.html)
   called using Biopython Command Line Wrapper [StretcherCommandline](https://biopython.org/DIST/docs/api/Bio.Emboss.Applications.StretcherCommandline-class.html).
   For further details check stretcher.py.
3. For each pairwise alignment, a pairwise distance matrix is computed using EMBASSY PHYLIPNEW [FDNADIST](http://emboss.sourceforge.net/apps/cvs/embassy/phylipnew/fdnadist.html) 
   called again using Biopython Command Line Wrapper [FDNADistCommandline](https://biopython.org/DIST/docs/api/Bio.Emboss.Applications.FDNADistCommandline-class.html).
   Using all these matrices, a final matrix comprising all possible pairs is produced. For further details, check fdnadist.py.
4. Using the matrix of step 3, a neighbor-joining tree is computed and stored in data/tree_output using EMBASSY PHILPNEW [FNEIGHBOR](http://emboss.sourceforge.net/apps/cvs/embassy/phylipnew/fneighbor.html)
   called using Biopython Command Line Wrapper [FNeighborCommandline](https://biopython.org/DIST/docs/api/Bio.Emboss.Applications.FNeighborCommandline-class.html). This part is implemented
   in the create_tree() function inside phylogeny_pipeline.py.
## Usage

```bash
python3 phylogeny_pipeline.py -n no_of_sequences
```

where no_of_sequences is a proper integer. 
Please set no_of_sequences = all if you want to consider all the sequences.
In the data folder you can find the results (splitting, alignments, matrices and tree)
of the execution with no_of_sequences = 15. 