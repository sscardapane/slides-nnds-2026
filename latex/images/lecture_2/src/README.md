# Lecture 2 figure sources

This directory contains the editable sources for generated Lecture 2 assets.
Keep each source versioned beside its exported figure.

| Source | Export | Notes |
|---|---|---|
| `plot_gradient_info.py` | `../gradient_info.pdf` | Recovered from NNDS 2024 preliminaries |
| `plot_taylor_approximation.py` | `../taylor_approximation.pdf` | Recovered from NNDS 2024 preliminaries |
| `plot_saddle_point.py` | `../saddle_point.pdf` | Recovered from NNDS 2024 preliminaries |
| `plot_full_vs_minibatch.py` | `../full_vs_minibatch.pdf` | Native 2026 replacement for the former external raster screenshot |
| `plot_stationary_points.py` | `../stationary_points.pdf` | Native 2026 replacement for the former external Wikimedia raster; includes a stationary inflection on the same curve |
| `plot_epoch_batches.py` | `../epoch_batches.pdf` | Native 2026 candidate with explicit batch-size and updates-per-epoch notation |
| `stochastic_optimization.drawio` | `../stochastic_optimization.pdf` | Authoritative source from NNDS 2024 `Book figures`; current PDF matches the archived export |
| `mini_batch.drawio` | `../mini_batch.pdf` | Authoritative source from NNDS 2024 `Book figures`; current PDF matches the archived export |
| `tensors.drawio` | no current export | Non-empty source from NNDS 2024 `Book figures`; retained for possible reuse |

The similarly named
`NNDS_2024/2_Preliminaries/draw.io/Tensors.drawio` is an empty Draw.io
document and is intentionally not preserved here.

## Rules

1. Edit the native source, not an exported PDF or PNG.
2. Export vector PDF or SVG whenever possible.
3. Keep notation, colors, and typography consistent with the current deck.
4. Render the complete slide after every export; inspecting the asset alone is
   not sufficient.
5. New scripts should write to an explicit output path and avoid dependencies
   that are no longer maintained.
