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

    Next thing i did is take this same signature(pam50) and compare it with my GEO expression data gene list. I know the GEO data set is new cause when i ran tcga project i came to this naming problem, cause 234 genes were not found in the GEO set that is found in TCGA data. 

    Data:
        1)GEO Expression data(stripped the gene names only.) (data/raw/GSE96058_gene_expression_3273_samples_and_136_replicates_transformed.csv) from my breast cancer external validation.
        2)The same pam50 data from the forum.

    what i ran:
        I compared these two gene names same way as before.
        and found out one gene is missing in the GEO dataset.
        that gene is 'ORC6L'. its because the ORC6L was changed to ORC6 and i checked it using hgnc tool.

    This is the problem faced by many people daily, a gene will be missing even then the program will run successfully but it would have negleted the missing genes, for my experimentation it was 1 gene missing from one cohort compared with one signature.
    What will happen if i take 3 cohorts and compare them individually with 3 signatures including one from older platform era where drift should be worse?

    And the question after that will be does losing that gene actually change the AUC, or does the signature not care? 

    The False result in this run: 
        my first comparison between these two returned 47 missing genes because the file was still being copied and pandas read a truncated version. Cause i copy pasted using drag and drop method, so i used cp which will only allow the program to run after the copying is done so after that i got correct results.
