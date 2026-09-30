# Grokking figures

Original plots from Power, Burda, Edwards, Babuschkin and Misra (2022),
[Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets](https://arxiv.org/abs/2201.02177).

- `grokking-accuracy.png`: Figure 1, left panel (PDF page 1).
- `grokking-loss.png`: Figure 4 (PDF page 7).
- Source: https://arxiv.org/pdf/2201.02177v1
- Source PDF SHA-256: `305dbd1256e1ac198dde517dda42b4f0a7eb9a9d3f4c03527c125b03eb9c62fc`.

`extract_grokking.py` uses pypdf to extract the original embedded images. The curves,
axes, legends and original resolution are preserved; these are published
results, not a local reproduction or schematic. The source paper is not
vendored. To regenerate after downloading the v1 PDF:

```sh
python extract_grokking.py /path/to/2201.02177v1.pdf .
```

The experiment is modular division, a 50% training split, and a small
transformer (not an MLP). The plots show the same experimental setup with
training/validation metrics over optimization steps. Both images retain their source resolution (1228 x 921 for accuracy,
432 x 288 for loss).
The slide identifies the architecture and credits the figures. Both axes
use the original scaling; in particular, optimization steps are logarithmic.
