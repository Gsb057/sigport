import pandas

#comparing my tcga expression data gene names with pam 50 gene names
TCGA = pandas.read_csv("data/raw/HiSeqV2", sep='\t')

TCGA_genes = TCGA['sample'].tolist()

with open("data/signatures/pam50_biostars2013.txt", "r") as file:
    pam50_genes = file.read().strip().split(",")

assert len(pam50_genes) == 50
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