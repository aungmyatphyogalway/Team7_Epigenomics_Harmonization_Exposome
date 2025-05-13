
# Team7_Epigenomics_Harmonization_Exposome

## The Challenge

**How do we connect multiple disparate data types to obtain a meaningful understanding of the biological functions of an organism?**

## Publicly Available Epigenomic and Exposome Data Sets

### 🔬 Exposome Data Sets
- **Exposome Correlation and Interpretation Database (ECID):** 250 publicly available datasets sourced from:
  - NHANES (National Health and Nutrition Examination Survey)
  - HHEAR
  - Metabolomics WorkBench
  - EBI Metabolights
  - ECHO  
- **NHANES:** Temporal `.xpt` files available for download

### 🧬 Epigenomic Datasets / Databases
- **ENCODE:** Python-wrapped datasets available (high-throughput sequencing)
- **GEO (Gene Expression Omnibus):** DNA methylation datasets
- **The Cancer Genome Atlas (TCGA):** Methylation array profiles


## 🔍 Project Team Breakdown & Responsibilities

To address the challenge of integrating disparate data types across epigenomics and the exposome, our team has been divided into three focused sub-teams with complementary roles:

---

### 🧠 Team A: Automate Epigenomics & Bioinformatics Data Acquisition

**Goal:** Develop scripts and tools to automate the querying and downloading of publicly available epigenomic data.

**Tasks:**
- 🔗 Explore and utilize the **GEOSeq Bioconductor R package** for automated downloads from GEO (Gene Expression Omnibus).
- 🧬 Automate the download of **high-throughput sequencing data** from the **NIH Epigenomics Roadmap**.

> ✅ Output: A fully automated pipeline to gather high-quality epigenomic datasets for downstream analysis.

---

### 🧬 Team B: Bioinformatics Pipelines for Data Harmonization & Analytics

**Goal:** Build robust pipelines to process and harmonize datasets from multiple sources.

**Tasks:**
- 🛠️ Design pipelines for processing **diverse epigenomic assay datasets**.
- 🔄 Perform **harmonization** by integrating processed epigenomic data with **exposome datasets** and optionally **RNA-Seq data**.
- 📊 Conduct downstream analyses such as:
  - Gene Set Enrichment Analysis (**GSEA**)
  - Gene Ontology (**GO**) analyses using **R**.

> ✅ Output: A modular pipeline enabling end-to-end data integration and biological insight generation.

---

### 🧹 Team C(lean): Cleaning & Imputation of Public Exposome Data

**Goal:** Handle preprocessing, cleaning, and integration of exposome datasets with epigenomic data.

**Tasks:**
- 📥 Download and import **NHANES `.xpt` files** and related exposome data from **TCGA** into Python or R.
- 🧰 Build **custom tools** to streamline access to exposome datasets and **high-throughput sequencing data** from NIH's Epigenomics Roadmap.
- 🔗 **Harmonize exposome data (Step 1)** and integrate it with epigenomic datasets (Step 2).

> ✅ Output: Clean, imputed exposome data prepared for merging with epigenomic profiles, enabling rich integrative analysis.

---

### 🤝 Cross-Team Collaboration

- 🔄 **Team A** provides raw data access pipelines to **Team B** and **Team C**.
- 🧬 **Team B** builds the integrative analytics pipelines using processed datasets.
- 🧹 **Team C** ensures exposome data is cleaned and harmonized for final integration.

**Methodology**

-Step 1: C-PTAC-2-Proteomic data, RNA-Seq and MiRNA data collection (TARGET, Geospatial:JPSS (NOAA)
Step 2a. Automate pulling these databases into our cleaning / imputation/ ML PYTHON script
Step 2b. Code one kind of Bidirectional Recurrent Neural Network model, taking in input from C-PTAC-2, TARGET, and JSSS 
Step 2c.. ML code also to split the data into training and test data sets
Step 3. Validation




  
