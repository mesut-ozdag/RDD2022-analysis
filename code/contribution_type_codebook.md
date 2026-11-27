# Contribution type codebook

Each study is coded by reading its title and abstract (for studies not among the abstracts compiled for coding, the evidence note and short summary recorded when its use was confirmed). Only the types that the text explicitly states as the study’s own contribution or method are coded; no inference is made from the name of the model used. A study may fall into more than one type. If no type fits, “Other” is coded.

| Code | Name | Condition for assigning 1 |
|---|---|---|
| architecture-improvement | Architecture improvement | A change to the backbone, neck, head, block or convolution structure of a detector, or a new network structure, is proposed. Structural changes aimed at attention, the neck or lightweighting also fall under this code. A change only to training settings, data or loss does not receive this code. |
| attention-module | Attention module | Adding or modifying a channel, spatial or self-attention mechanism (e.g., SE, CBAM, CA, EMA, transformer attention block) is stated as a contribution. Using an off-the-shelf transformer detector (e.g., RT-DETR) without modification does not receive this code. |
| lightweight/edge | Lightweight model / edge device | Reducing the parameters, computational load or model size, increasing inference speed, or running on a mobile, embedded or edge device is stated as an explicit goal. |
| neck/feature-fusion | Neck / feature fusion | The neck structure or multi-scale feature fusion (FPN, PAN, BiFPN, a new fusion module, cross-scale connections) is modified. Adding only an attention block to the neck does not receive this code. |
| loss/IoU | Loss function / IoU | The bounding-box regression loss or another loss function is modified or proposed (e.g., WIoU, SIoU, EIoU, Inner-IoU, focal loss). |
| data-augmentation/synthetic | Data augmentation / synthetic data | A new data augmentation method, or synthetic or generated data, is presented as a contribution. Using standard augmentation does not receive this code. |
| ensemble/TTA | Ensemble / TTA | Combining several models, or test-time augmentation, is part of the main method. |
| benchmark/comparison | Model comparison | The main contribution is a comparison of existing models or configurations without proposing a new method, or a new comparison protocol. |
| deployment/system/app | System / application | An application or system is built around the detection (mobile or web application, vehicle-mounted system, mapping, notification). |
| transfer/domain-generalization | Transfer / cross-domain generalization | Transfer learning, domain adaptation, or generalization across countries or datasets is tested as a contribution. |
| semi/self-supervised | Semi- / self-supervised | Semi-supervised, self-supervised or weakly supervised learning, active learning or pseudo-labeling is used. |
| multimodal/VLM/LLM | Vision-language model (VLM/LLM) | A vision-language model, a large language model or multimodal input is used. |
| severity/quantification | Severity / quantification | The size, area or severity of the damage is measured or graded. |
| segmentation | Segmentation | An instance or semantic segmentation task is performed. |
| small-object | Small object | Detection of small objects or small damage is an explicit goal (e.g., a small-object detection layer). |
| drone/UAV | UAV applications | Unmanned aerial vehicle images are the focus of the study. |
| new-dataset | New dataset | A newly collected or labeled dataset other than RDD2022 is introduced. |
| other | Other | None of the types above fits the contribution described in the text. |
