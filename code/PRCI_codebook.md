# Protocol Reporting Completeness Index (PRCI): Codebook

Version: 2 November 2026. PRCI is an exploratory reporting index developed in this research. The criteria table, the checklist sub-items and the comparability variables below were fixed before the studies were coded; the “Application rules” section was added during the development of the index.
What is measured is not performance but how completely the article reports its RDD2022 experiment.
Each criterion is scored 0 or 1; the total ranges from 0 to 8. Information that cannot be found explicitly in the article is scored 0.
The assessment is based only on the article’s own text, tables, appendices and the links the article provides.

| Code | Criterion | Condition for 1 point | Examples of 0 points | Rationale |
|---|---|---|---|---|
| C1 | Country subset | The RDD2022 country subsets used in the experiment are stated by name or as "all six countries" | Only "RDD2022 was used" | Subsets differ in image source and class distribution |
| C2 | Data split | The training/validation(/test) ratio or the image counts of the reported experiment are given, and the given counts are consistent with each other and with RDD2022 | No split; the counts contradict each other | Performance depends on the split |
| C3 | Damage classes | The classes used in the evaluation are listed by name or code, and the number of classes is clear | Only "four classes" | The class set directly affects the mAP value |
| C4 | Metric and IoU | The main metric is named and the IoU threshold is given explicitly (such as mAP@0.5, mAP50, AP50, F1@IoU>0.5) | "mAP" without a threshold | Values without a threshold cannot be compared |
| C5 | Seed/repeated-run information | A random seed value is given, or the experiment is repeated at least twice and the mean/deviation is reported | Single run, no seed | A 1–2 point difference in a single run may be noise |
| C6 | Hardware and training settings | The GPU/hardware model and at least three of the following five are given: epochs, batch size, learning rate, optimizer, input size | Only one of them | Required for re-running the experiment |
| C7 | Code or weights | The article contains a link to publicly available code or model weights | "On request", no link | Makes independent testing possible |
| C8 | Test protocol | (a) Evaluated on the official hidden test, or (b) there is a test set separate from validation and its membership can be reconstructed (image list/split file shared or split seed given) | Validation set counted as test; only a random ratio, no seed | If others cannot reconstruct the same test, the result cannot be checked |

## Application rules

The rules below were written down for borderline cases that the table above does not cover. The main-experiment and C7 rules put into writing the practice that the coders followed during coding and did not change any decision. The C2 and C6 rules, in contrast, were clarified during the development of the index, because PRCI is an exploratory index. The rules do not change the criteria in the table; they explain how the criteria are applied; they are also stated in Section 2.2.5 of the article.

- Scoring is based on the article’s main RDD2022 experiment. Omissions in side experiments do not lower the score of the main experiment.
- In C2, a contradiction means a difference of more than 1% between the parts and the total, or the use of a number smaller than the official count without stating that a selection was made.
- In C6, if the article uses the number of rounds in the sense of epochs, this value is counted as epochs.
- In C7, the link must point to the code or weights of the reported RDD2022 experiment. A link containing the code of an earlier study is not sufficient.

These rules changed three decisions (two in C2, one in C6). The initial and final decisions are in sheet S10 of the Supplementary Data file. If, in C2, stating that a selection was made had not been considered sufficient and the reason for the selection had also been required, [15] and [9] would also have scored 0, the number of studies meeting C2 would have been 10/21 and the median total score would have been 4.

## Checklist sub-items (Yes/No)

The sub-item codes C1a–C6b are the identifiers used in analysis.py; they are not related to the PRCI criteria C1–C8.

- C1a the four official classes (D00, D10, D20, D40) are used in full in the main result; C1b if there is an extra class, it is reported separately per class.
- C2a official hidden-test F1 score given; C2b per-country F1 given.
- C3a split ratio or counts given; C3b the subsets used are named; C3c image list/split file shared.
- C4a mAP@0.5 given; C4b mAP@0.5:0.95 given; C4c mean and deviation of at least three repeated runs given.
- C5a number of parameters; C5b GFLOPs; C5c time per image/FPS; C5d stated that the time includes pre- and post-processing; C5e hardware.
- C6a code shared; C6b weights shared.

## Comparability variables

Subset list; China type (UAV, motorbike, both, not stated); number and names of the classes in the main result; split definition;
test definition (Official hidden, Test split defined, Validation counted as test, Undefined, External (cross-dataset) test; values from external tests were not used in the medians, ranges or gain statistics); input size; main result values and the experiment they belong to.
