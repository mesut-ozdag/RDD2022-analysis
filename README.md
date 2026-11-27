# RDD2022-analysis

**Quantifying Reproducibility and Comparability in the RDD2022 Road Damage Detection Literature**

This repository contains the Supplementary Data file, the search and analysis code and the codebooks of the article above. The study is a meta-research measurement of how comparable the experiments of road damage detection studies that use the RDD2022 dataset are, and how completely these studies report their evaluation protocols. It starts from 554 OpenAlex records citing or mentioning RDD2022 and indexed by 12 October 2026; together with two supplementary searches, these records yielded 297 studies with confirmed use of the dataset, which were coded by model family and contribution type. For an analysis set of 21 studies, the experimental conditions were coded with a comparability matrix (subset, class set, test definition and data split), and reporting completeness was scored with the Protocol Reporting Completeness Index (PRCI), an exploratory eight-item index developed in this research.

**Authors:** Mesut ÖZDAĞ¹\*, Gökay BOYNUKISA¹, Sude Yaren ÇELİK², Esra CANPOLAT², Saliha Cansu PULAT², Meryem ÜNALDI²

¹ Department of Database, Network Design and Management, Vocational School of Information Technologies, Karabük University, Karabük, Türkiye  
² Department of Computer Engineering, Faculty of Computing and Informatics Science, Karabük University, Karabük, Türkiye  
\* Corresponding author

## Contents

| File or folder | Description |
|---|---|
| `Supplementary_Data.xlsx` | Supplementary Data file. A README sheet and sheets S1–S17 give the record-selection flow, the search logs, the record-level decisions, the 297 classified studies, the experiment records of the 21 studies in the analysis set, the PRCI codes, the comparability matrix and study pairs, the checklist, the contribution types, the reported gains and the codebooks. |
| `code/` | Search, analysis and figure scripts, codebooks and intermediate outputs. Each file is described in `code/README.md`. |
| `LICENSE` | MIT License. |

## Reproducing the figures and the analysis

- **Figures:** `cd code && python3 figures.py ../figures` draws Figures 1–6 of the article (`figure1.png` … `figure6.png`) from `code/results.json`, without network access. It needs Python 3 with matplotlib and NumPy and the Times New Roman font; the font path in `figures.py` is for macOS (`/System/Library/Fonts/Supplemental/`) and has to be changed on other systems.
- **Analysis numbers:** `code/results.json` is the archived output of `code/analysis.py`; most of the analysis numbers in the article are taken from this file. `analysis.py` cannot be re-run with this repository alone, because some of its input files contain publisher texts (abstracts) and the intermediate decision and data-extraction files are not shared; the full list of inputs is given in `code/README.md`. The search-flow counts (Table 1, S1) were transferred manually from the records.
- **Searches:** the queries can be re-run with `code/openalex_search.sh`, `code/openalex_corpus.py` and `code/supp_search.py` (network access required). Because the indexes are updated continuously, the results may differ from the numbers in the article.
- **Record-level decisions:** all final decisions are in `Supplementary_Data.xlsx`.

## Data notes

- **PRCI:** the Protocol Reporting Completeness Index is an exploratory reporting index developed in this research. Its codebook is in `code/PRCI_codebook.md` and in sheet S16 of the Supplementary Data file. The criteria are labeled C1–C8 in the documents and stored as K1–K8 in the code and JSON files.
- **Language of the Supplementary Data file:** sheet names, column headers, the README sheet, the codebook sheet S16, the short-label sheets S1, S13 and S14 and all fixed categorical values are in English. The long free-text columns are kept in their original Turkish: S2 “Query” (literal search strings), S4 “Evidence note”, S5 “Reason for inclusion”, S6 “Reason use could not be confirmed”, S7 “Re-check evidence note”, and S10 “Initial evidence note (if changed)” and “Evidence note”. Titles, author names and venues are given as in the bibliographic records.
- **Language of the code files:** comments, docstrings, printed text and figure labels are in English. The data values in the JSON and TSV files are unchanged from the analysis: free-text notes and several value codes and labels are in Turkish, and the JSON keys are kept because the scripts read them. `code/README.md` explains these identifiers and values.
- **Same coder:** the two codings in S10 and S17 and in `code/recheck_coders.json` and `code/contribution_coding_v4_raw.json` are two separate assessments made by the same coder at different times; they do not count as independent coders.

## License

MIT License; see `LICENSE`.

## Citation

Manuscript under review. The full citation will be added here when the article is published.
