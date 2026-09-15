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
        this was done against TCGA 

        Inference, based on one gene (ORC6L). 49 of 50 symbols are stable and would match in any era, so they provide no evidence either way.

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
        pandas saw 4,213 rows when the file has 30,865 when i used drag and drop method. TCGA ~20,000 genes, GSE96058 30,865 genes, truncated read 4,213 rows.

15-09-2026

    To push this further, I needed to test an older platform era where naming drift should be much worse. I took the GPL96 platform file (which maps probes to gene symbols for older Affymetrix arrays) and compared it against the PAM50 signature.

    Data: 
        1) GPL96 platform annotation file (data/raw/GPL96-57554.txt).
        2) The same PAM50 gene list from the Biostars 2013 forum.

    What i ran: 
        I extracted just the Gene Symbol column from GPL96 to see how many PAM50 genes were missing. 
        At first, my code returned 8 missing genes. But one of the missing genes was KRT17. KRT17 is a core basal-subtype marker, and it was biologically implausible that a 22,283-probe array from 2002 wouldn't measure it. 
        
        That suspicion made me check my code. I found a bug: when a probe maps to multiple genes (like "KRT17P1 /// KRT17"), my code `split(" /// ")[0]` was keeping the first symbol and silently throwing the rest away. I was creating the data loss myself.

        The Fix & New Counts: 
        I fixed the loop to flatten and keep every symbol from every cell. 
        When I reran it, KRT17 came back. The count of missing genes dropped from 8 to 7. 
        The 7 missing genes are: 'CXXC5', 'UBE2T', 'NUF2', 'ANLN', 'GPR160', 'ORC6L', 'TMEM45B'.

        The Row Counts (Sanity Check):
        The 22,283 probes on GPL96 collapsed into exactly 14,208 unique gene symbols. Comparing this to TCGA (~20,000 genes) and GSE96058 (30,865 genes), that massive gap explains why genuine gene absence exists in this older dataset and not in my newer cohorts.

        The Gemini Verdict: 
        Earlier, Gemini told me there were 6 missing genes on this platform. Gemini's 6 are all in my 7—so it wasn't fabricating, but it was incomplete. It missed ORC6L. 
        Why? Because Gemini was reciting a community-repeated list of "genes not on U133A" which quietly folds naming drift into absence. ORC6L is missing from GPL96 because it was later renamed to ORC6, not because the array lacks it. I found this out by actually measuring it, not just asking. 

        The CDCA1 Check & Next Steps:
        I wanted to see if NUF2 was just hiding under its old alias, CDCA1. I checked the GPL96 list for CDCA1, and it returned False. 
        But this False just means it's not under *that specific* alias. I can't resolve this by guessing aliases one gene at a time for all 7 genes. I need an alias table (like from HGNC) that I can query systematically to split these 7 genes into two categories: "recoverable drift" vs. "genuinely absent (no probe exists)". Without this, I'd report a biological limitation that is actually just a clerical data-wrangling error.