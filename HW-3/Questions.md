# Homework-3

Due date: June 2. Feel free to submit it much earlier than that.
I am away from May 16-31.

Feel free to discuss any part of the following with me.  Your task is
to construct a phylogenetic tree for 18 yeast species, as follows.

1. Download the file
http://www.imsc.res.in/~rsidd/yeast_orthologues.tar.gz
and extract it.  Each file therein is named after a S.cerevisiae gene,
and contains that sequence as well as orthologous sequence from 17
other species.  In the headers, after ">" the first four characters
are a short form of the species name (eg, Scer = Saccharomyces
cerevisiae) and, after the underscore ("_"), the rest is the gene name
in that species.  You can ignore this information.

2. Run a multiple alignment program of your choice on each of these
files, output to multi-fasta format.

3. Write a program to concatenate all these alignments, stripping out
all columns with dashes, into one file.  (Check the output carefully.
If a column is aligned in the original file, it must be aligned in the
concatenated file).  For example, if you have two files like
1
ATCAACA
2
AT-GACA

and
1
CAG--ATT
2
C-GCCATT

then the concatenated output with gaps removed will be
1
ATCAACACGATT
2
ATGACACGATT

3.  Use a program of your choice to infer a phylogenetic tree from
these alignments.  Standard programs these days are PhyML, MrBayes,
BioNJ (for ML, Bayesian, Neighbour-joining respectively).

4. Also use UPGMA for which I previously sent you an implementation.

5. The above programs will probably output a tree in "Newick" format.
Use a tree-drawing program to convert those to a visual tree.

6. Document whatever you did and write it up.

You may like to look at http://www.phylogeny.fr/ which provides a web
interface to several programs, though I would recommend using it only
for the tree-drawing part and running other programs "locally".