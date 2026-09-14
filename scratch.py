import pandas

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