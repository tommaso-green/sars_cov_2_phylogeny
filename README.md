# Phylogenetic trees by Multiple Pairwise Alignments

This is a repo containing code for creating neighbor-joining
phylogenetic trees. It is mainly based on [Biopython] (https://biopython.org) and on
[EMBOSS] (http://emboss.sourceforge.net/index.html) and the usage of phylip software through the use of
the EMBASSY package [PHYLIPNEW] (http://emboss.sourceforge.net/apps/release/6.6/embassy/phylipnew/) 
The execution of this software is recommended on Ubuntu due to the great ease of
installation of the dependecies.

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
* [EMBOSS Download and Instructions] (http://emboss.sourceforge.net/download/)
* [EMBASSY PHYLIPNEW] (ftp://emboss.open-bio.org/pub/EMBOSS/) can be downloaded as a tarball here,
  (instructions inside.)

## Usage

```bash
python3 phylogeny_pipeline.py -n no_of_sequences
```
