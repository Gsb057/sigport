import pandas

with open("data/signatures/pam50_biostars2013.txt", "r") as file:
    pam50_genes = file.read().strip().split(",")

assert len(pam50_genes) == 50
'''
#comparing my tcga expression data gene names with pam 50 gene names
TCGA = pandas.read_csv("data/raw/HiSeqV2", sep='\t')

TCGA_genes = TCGA['sample'].tolist()

missing_genes = list(set(pam50_genes) - set(TCGA_genes))

print(f"Number of PAM50 genes missing from TCGA: {len(missing_genes)}")
print("Missing gene names:", missing_genes)

print(len(pam50_genes))
print(pam50_genes[:5])

print('ORC6L' in TCGA_genes, 'ORC6' in TCGA_genes)

#comparing my geo data gene names with pam50 gene names

GSE = pandas.read_csv("data/raw/GSE96058_gene_expression_3273_samples_and_136_replicates_transformed.csv", sep=',')
GSE_genes = GSE.iloc[:, 0].tolist()

missing_genes2 = list(set(pam50_genes) - set(GSE_genes))

print(f"Number of PAM50 genes missing from GSE96058: {len(missing_genes2)}")
print("Missing gene names:", missing_genes2)

print(len(GSE_genes))
print(GSE_genes[:10])

print('ORC6' in GSE_genes)
'''
#Comparing GPL96 gene name with my pam50 genes
#Load just the Gene Symbol column from the GPL96 platform file
gpl_df = pandas.read_csv("data/raw/GPL96-57554.txt", comment="#", sep="\t", low_memory=False)

#Correctly flatten and strip all mapped symbols
GPL96_genes_set = set()
for raw_val in gpl_df["Gene Symbol"].dropna():
    if str(raw_val) != "nan":
        # Split by " /// ", strip each, and add to the set
        for gene in str(raw_val).split(" /// "):
            clean_gene = gene.strip()
            if clean_gene:
                GPL96_genes_set.add(clean_gene)

GPL96_genes = list(GPL96_genes_set)

#Compare directly
missing_genes = list(set(pam50_genes) - set(GPL96_genes))

print(f"Total unique genes in GPL96: {len(GPL96_genes)}")
print(f"Number of PAM50 genes missing from GPL96: {len(missing_genes)}")
print("Missing gene names:", missing_genes)

#Check for CDCA1 (NUF2 alias)
print(f"Is CDCA1 in GPL96?: {'CDCA1' in GPL96_genes}")