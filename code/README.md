# Search and analysis code

This folder contains the search scripts, the analysis and figure scripts, the codebooks and the intermediate outputs of the study. Sheet numbers S1–S17 refer to `../Supplementary_Data.xlsx`.

## Files

- `openalex_search.sh`: main OpenAlex search queries (12 October 2026); these queries do not request the abstract field.
- `openalex_corpus.py`: merges the responses (572 unique records), retrieves the abstracts from the `abstract_inverted_index` field with a separate query, and applies the keyword and type filter (554 records).
- `targeted_search_queries.tsv`: the 107 web queries run in the targeted search of 12 October 2026 and the numbers of result links (columns `date`, `query_group`, `query`, `n_result_links`; the queries are the literal search strings, some of them in Turkish or Chinese). The search also used Semantic Scholar and OpenAlex citation queries, Semantic Scholar keyword queries, and the Europe PMC and arXiv APIs (counts in S2).
- `supp_search.py`: documented API search (2 November 2026): Crossref, arXiv, Semantic Scholar, Europe PMC. The script also contains DBLP queries, but no results were obtained because the server blocked automated queries (S2).
- `PRCI_codebook.md`: PRCI criteria, application rules, checklist sub-items and comparability variables.
- `contribution_type_codebook.md`: contribution type codebook. The contribution types of the 297 studies were coded twice with this codebook from the title and abstract (for the 28 studies not among the compiled abstracts, from the evidence note and short summary); for the 30 studies on which the two codings disagreed, the decision was made by a third assessment by the same coder.
- `contribution_coding_v4_raw.json`: the two assessments of the contribution type coding (`A`, `B`), the decisions of the third assessment (`ADJ`), the final codes (`final`) and the source of the decision (`src`).
- `analysis.py`: merges the study list and computes most of the analysis numbers; the numbers of the search flow (Table 1, S1) were transferred manually from the records.
- `figures.py`: Figures 1–6 of the article, drawn from `results.json`. Usage: `python3 figures.py OUTPUT_DIR` (writes `figure1.png` … `figure6.png`). Requires matplotlib, NumPy and the Times New Roman font; the font path is for macOS.
- `matrix_cells.py`: the cell text of Table 7 of the article (comparability matrix), keyed by study code; the per-study codes behind it are in S11.
- `recheck_coders.json`: decisions and evidence levels of the two assessments in the third check of 91 records.
- `results.json`: output of `analysis.py`; most of the analysis numbers in the article are taken from this file, and `figures.py` reads it.
- `prci_final_v2.json`: PRCI codes after the application rules, evidence notes and experiment records of 31 studies (written by `analysis.py`).
- `browser_check_3nov.json`: record-level results of re-checking, on 3 November 2026, the publisher pages of the 51 records whose use could not be confirmed.

The two codings in S10, in `recheck_coders.json` and in `contribution_coding_v4_raw.json` are two separate assessments made by the same coder at different times; they do not count as independent coders (article, Sections 2.2.3 and 2.2.5).

## Running the code

`figures.py` runs with the files in this folder alone (no network access):

```
python3 figures.py ../figures
```

`analysis.py` cannot be re-run with this repository alone, because the input files it reads are not included. `corpus.json` and `abstract_alt.json`, which contain the abstract texts, and the intermediate abstract files were not shared because they contain publisher texts. The intermediate decision, data-extraction and coding files are not included either. `analysis.py` expects them next to this folder, in `../data/` (`papers.json`, `corpus.json`, `abstract_alt.json`, `analysis_21.json`, `wf1_result.json`, `deep_result.json`, `deep_targets.json`, `contribution_coding_input_297.json`), `../out/` (`use_status_interim.json`, `wf_main.json`, `new_candidates.json`, `prci_final.json`, `rescreen.json`, `recheck.json`, `verify_auto_from_deep.json`, `contribution_codes_v4.json`, and a copy of `contribution_coding_v4_raw.json`) and `../batches/` (`new_*.json`, `recheck_*.json`). It writes `../out/results.json`, `../out/prci_final_v2.json`, `../out/status_final.json` and `../data/final_studies.json`; the archived outputs `results.json` and `prci_final_v2.json` are included in this folder.

The queries can be reproduced with `openalex_search.sh` and `supp_search.py` (network access and `curl` required; `openalex_search.sh` writes the responses to `oa/`, and `openalex_corpus.py` reads `oa/` and writes `corpus.json` in the working directory); however, the results may differ because the indexes are updated. After 12 October 2026, OpenAlex merged the arXiv and journal records; on 2 November 2026 both IDs return the same 221 records. The raw responses of 12 October (`oa/`) were not kept, and `corpus.json` was rebuilt on 2 November 2026 from the search records. The final record-level decisions are in `../Supplementary_Data.xlsx`. The separate PRCI codes of the two assessments are given in this file (S10) for the 21 studies in the analysis set. For the third check, the evidence for the OpenAlex records and the decisions of the two assessments are in S7; the two codes of the other records are in `recheck_coders.json`.

The citation count in Google Scholar (489) was read only as a cross-check and was not used in the article (S2).

## Identifiers and Turkish values in the code and data files

The data values in the JSON and TSV files are unchanged from the analysis, and the JSON keys are kept as they were produced, because `analysis.py` and `figures.py` read them. As a result, some identifiers and values are in Turkish:

- The PRCI criteria C1–C8 are stored as `K1`–`K8`, and PRCI appears as `prti` (from its Turkish acronym PRTİ) in variable names and in `results.json` keys such as `prti_rows` and `prti_crit`. The checklist sub-items `C1a`–`C6b` use the identifiers of `PRCI_codebook.md`.
- Free-text values (evidence notes, `notes_tr`, `not_tr`, `basis`, `reason`, experiment descriptions and decision notes) are in Turkish, like the free-text columns of the Supplementary Data file.
- Decision codes: `teyit` = use confirmed, `dogrulanamadi` = use could not be confirmed, `kullanmiyor` = does not use the dataset, `yinelenen_surum` = duplicate version, `yayin_turu_uygun_degil` = ineligible publication type, `derleme` = review article, `veri_seti_tanitimi` = dataset paper, `konu_disi` = off-topic.
- Evidence levels: `tam_metin` = full text, `tam_metin_tez` = full text of the thesis of the same study, `ozet_veya_yayinci` = abstract or publisher page, `alinti_veya_dizin` = search snippet or index copy, `yok` = none; `access_level` in `prci_final_v2.json`: `tam_metin` = full text, `ozet` = abstract only.
- `contribution_coding_v4_raw.json`, `src`: `uyum` = the two codings agreed, `hakem` = decided by the third assessment.
- `browser_check_3nov.json`: `sonuc` = result (`acildi_karar_degismedi` = page opened, decision unchanged; `acilamadi` = page could not be opened; `tam_metin_okundu_teyit` = full text read, use confirmed); `not_tr` = note.
- `prci_final_v2.json`, `comparability`: `test_def` `resmi_gizli` = official hidden test, `ayri_test` = separate test split, `dogrulama_test_sayilmis` = validation counted as test, `dis_test` = external test, `tanimsiz` = undefined; `china_type` `İHA` = UAV, `motosiklet` = motorbike, `ikisi` = both, `belirtilmemiş` = not stated, `yok` = no China subset.
- `results.json`: the comparability codes in `matrix_vars` and `test_counts` (`resmi` = official hidden test, `ayri` = separate test split, `dogrulama` = validation counted as test, `tanimsiz` = undefined; subset labels such as `6 ülke` = 6 countries, `Çin` = China, `Çin İHA` = China UAV); `resmi_test` = studies evaluated on the official hidden test (`katilimci` = challenge participants, `ozet` = challenge summary papers, `yarisma` = participants and summary papers together, `diger` = other studies); `checklist_all` (`sinif` = classes, `resmi` = official test, `bolme` = split, `metrik` = metric, `verim` = efficiency, `kod` = code and weights); sensitivity scenarios (`taban` = baseline). Search arms: `Hedefli tarama (12 Ekim 2026)` = targeted search (12 October 2026), `Belgelenmiş tarama (2 Kasım 2026)` = documented search (2 November 2026).
- Model families and contribution types are stored with their Turkish labels (for example `Diğer` = Other, `YOLO (diğer)` = YOLO (other), `DETR ailesi` = DETR family, `Topluluk (ensemble)` = Ensemble, `CNN sınıflandırıcı` = CNN classifier, `Segmentasyon ağı` = Segmentation network, `Görsel-dil modeli` = Vision-language model, `Diğer dedektör` = Other detector). The contribution labels are defined in `CONTRIB_TR` in `analysis.py`, which maps each code of `contribution_type_codebook.md` to its Turkish label; the English names are those of the codebook and of S14.
