14-09-2026

I wanted to check myself and see the problem. to check whether this naming problems occur often. so i took my tcga expression data stripped only the gene names and compared them with pam50 gene names.

Data: 
    1)TCGA expression matrix data. from my breast cancer project. data/raw/HiSeqV2
    2)PAM50 gene names i took from an 2013 forum cause i couldnt find the parseable gene names.(biostars.org/p/77590/)
    (Google's AI gave me this list citing a Bruker product page that doesn't contain it, and that the list turned out to be identical to the Biostars post.)

What i ran: 
    I took these two lists and compared them to find what genes are missing in the tcga file. and suprisingly every gene was present in the tcga data that is in pam50 gene.
    so it returned output as 0 missing and 50 loaded.

    i didnt believe it at first but after some digging i found out that these two data are from same time period and follow the same naming convention so they names are identical.(this is my explanation for this result)

    even after i checked for two specific genes ORC6L and ORC 6 and the ORC6L is and previous symbol which got renamed to ORC6 and ORC6 is approved symbol.

    so my program returned True for ORC6L and False for ORC 6 cause it follows old naming convention.

    So the next thing to check would be comparing gene names from different eras and timing.