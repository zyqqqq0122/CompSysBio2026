# TCGA-LUAD Multi-Omics Tumor Prediction

This project analyzes TCGA lung adenocarcinoma (LUAD) samples using three omics layers:

- RNA sequencing (`RNASeq`)
- DNA methylation (`DNAm`)
- Copy number variation (`CNV`)

The main notebook, `final.ipynb`, trains tumor-vs-normal classifiers, compares single-omics and pairwise multi-omics models, and performs biological interpretation using SHAP, pathway enrichment, CpG-to-gene mapping, and DIABLO.

## Project Files

```text
.
├── final.ipynb
├── README.md
├── hm450_manifest.csv.gz
├── hm450_manifest_slim.csv
└── Group2-TCGA-LUAD-lung-adeno/
    ├── metadata.csv
    ├── RNASeq.csv
    ├── DNAm.csv
    └── CNV.csv
```

`hm450_manifest.csv.gz` is the manually downloaded Illumina HumanMethylation450 manifest. In this project folder, the file has a `.gz` extension but is read as plain CSV if it is not actually gzip-compressed. The slim cache file, `hm450_manifest_slim.csv`, stores only CpG probe IDs and gene annotations.

## Data Overview

The notebook loads:

| Data layer | Samples | Features |
|---|---:|---:|
| RNASeq | 447 | 14,434 genes |
| DNAm | 420 | 384,629 CpG sites |
| CNV | 424 | 14,434 genes |

Sample IDs are harmonized across metadata and omics files before modeling. Labels are encoded as:

- `0`: Normal
- `1`: Tumor

## Analysis Workflow

The notebook follows this structure:

1. Load and harmonize metadata, RNASeq, DNAm, and CNV data.
2. Select high-variance features for each omics layer.
3. Train tumor-vs-normal classifiers using 5-fold stratified cross-validation.
4. Compare single-omics models with pairwise early-fusion models.
5. Fit DIABLO as a supervised three-layer multi-omics integration model.
6. Interpret model predictions using SHAP and feature-importance methods.
7. Map methylation CpG probes to genes using the Illumina 450K manifest and `mygene`.
8. Run pathway enrichment with Enrichr through `gseapy`.
9. Compare feature stability and biological consistency across methods.

## Models

The active models in `final.ipynb` are:

- Logistic Regression
- Random Forest
- Linear SVM
- XGBoost

RNASeq and DNAm features are scaled and compressed with PCA before modeling. CNV is scaled but kept without PCA. Pairwise models use early fusion, where each modality block is processed separately before concatenation.

## Main Results

Single-omics classification performed very strongly:

| Modality | Best model | AUC-ROC | Balanced accuracy |
|---|---|---:|---:|
| RNASeq | Logistic Regression | 1.000 | 1.000 |
| DNAm | Linear SVM | 1.000 | 1.000 |
| CNV | XGBoost | 0.999 | 0.900 |

Pairwise early-fusion models also reached near-perfect AUC-ROC:

| Combination | Best model | AUC-ROC | Balanced accuracy |
|---|---|---:|---:|
| RNASeq + DNAm | XGBoost | 1.000 | 0.999 |
| RNASeq + CNV | XGBoost | 1.000 | 1.000 |
| DNAm + CNV | Linear SVM | 1.000 | 0.849 |

DIABLO was successfully fitted across all three omics layers and achieved:

- AUC-ROC: 0.952
- Balanced accuracy: 0.500

The lower DIABLO balanced accuracy reflects the strong class imbalance in the shared three-omics sample set, which contains only 9 normal samples and 388 tumor samples.

## Biological Interpretation

The notebook includes several interpretation layers:

- SHAP analysis for XGBoost models.
- PCA backprojection for RNASeq and DNAm SHAP scores.
- Direct gene-level SHAP interpretation for CNV.
- CpG-to-gene mapping for DNAm using the Illumina 450K manifest.
- Gene symbol standardization using `mygene`.
- Enrichr pathway enrichment using `gseapy`.
- Feature stability analysis across folds and random seeds.
- Cross-modality comparison of RNASeq and CNV signals.

Examples of high-ranking features include:

- RNASeq: `MIF`, `RBM34`, `PTP4A1`, `TOMM6`, `LRP11`
- CNV: `HOMEZ`, `RNF138`, `GZMB`, `ELAVL2`, `ZNF713`
- DNAm mapped genes: `LHX1`, `HOXB4`, `GRIA4`, `FLI1`, `VWC2`

## Requirements

The notebook uses Python packages including:

```text
numpy
pandas
matplotlib
seaborn
scikit-learn
xgboost
shap
gseapy
mygene
scipy
```

The DIABLO section uses R through `rpy2` and requires the R package:

```text
mixOmics
```

If optional packages are missing, install them before running the relevant sections.

## Running the Notebook

Open and run:

```text
final.ipynb
```

Make sure the folder `Group2-TCGA-LUAD-lung-adeno/` is present in the same directory as the notebook and contains:

- `metadata.csv`
- `RNASeq.csv`
- `DNAm.csv`
- `CNV.csv`

For the DNAm CpG-to-gene mapping section, keep the manually downloaded `hm450_manifest.csv.gz` file in the project root. The notebook will create or reuse `hm450_manifest_slim.csv`.

## Notes

The classification results are very strong, especially for RNASeq and DNAm. Because the dataset is highly imbalanced toward tumor samples, balanced accuracy and validation design should be interpreted carefully alongside AUC-ROC.

The interpretability sections are intended to support biological interpretation rather than replace independent validation. High-ranking genes and enriched pathways should be treated as candidate signals for discussion and follow-up analysis.
