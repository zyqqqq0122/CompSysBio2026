from pathlib import Path
import pandas as pd

base_dir = Path(__file__).resolve().parent / "Group2-TCGA-LUAD-lung-adeno"

rna_seq_path = base_dir / "RNASeq.csv"
cnv_path = base_dir / "CNV.csv"
dnam_path = base_dir / "DNAm.csv"
metadata_path = base_dir / "metadata.csv"

rna_seq = pd.read_csv(rna_seq_path)
cnv = pd.read_csv(cnv_path)
dnam = pd.read_csv(dnam_path)
metadata = pd.read_csv(metadata_path)

# DataFrames are now available:
# rna_seq, cnv, dnam, metadata
