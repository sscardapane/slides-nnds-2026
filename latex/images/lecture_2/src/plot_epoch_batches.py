"""Draw the shuffle → mini-batches → one epoch workflow as a vector figure."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


DARK = "#263B40"
BLUE = "#3A82B8"
RED = "#A92323"
GREEN = "#3F8151"
LIGHT_BLUE = "#DCEAF7"
LIGHT_GREEN = "#E0EEDF"
LIGHT_RED = "#F5DADA"
LIGHT_GRAY = "#F3F5F5"
STROKE = "#52646B"


def box(axis, x, y, width, height, label, *, fill="white", text_color=DARK, rounded=False, fontsize=14):
    patch_type = FancyBboxPatch if rounded else Rectangle
    kwargs = {"boxstyle": "round,pad=0.04,rounding_size=0.12"} if rounded else {}
    patch = patch_type(
        (x, y),
        width,
        height,
        facecolor=fill,
        edgecolor=STROKE,
        linewidth=1.5,
        **kwargs,
    )
    axis.add_patch(patch)
    axis.text(x + width / 2, y + height / 2, label, ha="center", va="center", fontsize=fontsize, color=text_color)


def arrow(axis, start, end, *, color=DARK, dashed=False, connectionstyle="arc3"):
    axis.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.45,
            linestyle="--" if dashed else "-",
            color=color,
            connectionstyle=connectionstyle,
            shrinkA=2,
            shrinkB=2,
        )
    )


def build_figure(output: Path) -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Fira Sans", "DejaVu Sans"],
            "mathtext.fontset": "cm",
            "pdf.fonttype": 42,
        }
    )
    figure, axis = plt.subplots(figsize=(10.4, 4.15), constrained_layout=True)
    axis.set_xlim(0, 12)
    axis.set_ylim(0, 7)
    axis.axis("off")

    box(axis, 2.0, 5.9, 7.5, 0.72, "Dataset", fontsize=15)
    arrow(axis, (5.75, 5.88), (5.75, 5.25))
    axis.text(5.3, 5.52, "shuffle", ha="right", va="center", fontsize=12.5, color=DARK)

    box(axis, 2.0, 4.5, 7.5, 0.72, "Shuffled dataset", fontsize=15)
    arrow(axis, (5.75, 4.47), (5.75, 3.84))
    axis.text(
        5.28,
        4.1,
        r"split into $K$ mini-batches of size $B$",
        ha="right",
        va="center",
        fontsize=12.5,
        color=DARK,
    )

    batch_y = 3.10
    batch_h = 0.72
    batch_x = [2.0, 3.75, 5.5, 7.25]
    batch_labels = [r"$\mathcal{B}_1$", r"$\mathcal{B}_2$", r"$\cdots$", r"$\mathcal{B}_K$"]
    batch_fills = [LIGHT_RED, LIGHT_GREEN, LIGHT_GRAY, LIGHT_BLUE]
    batch_colors = [RED, GREEN, STROKE, BLUE]
    for x, label, fill, color in zip(batch_x, batch_labels, batch_fills, batch_colors):
        box(axis, x, batch_y, 1.75, batch_h, label, fill=fill, text_color=color, fontsize=16)

    update_y = 1.72
    update_w = 1.55
    update_x = [2.10, 3.85, 7.35]
    update_labels = ["SGD update\n1", "SGD update\n2", "SGD update\n$K$"]
    for x, label in zip(update_x, update_labels):
        box(axis, x, update_y, update_w, 0.82, label, fill="white", rounded=True, fontsize=12.5)

    for bx, ux in zip([2.0, 3.75, 7.25], update_x):
        arrow(axis, (bx + 0.875, batch_y - 0.02), (ux + update_w / 2, update_y + 0.84))
    arrow(axis, (3.67, 2.13), (3.83, 2.13))
    arrow(axis, (5.42, 2.13), (7.33, 2.13), dashed=True)

    axis.plot([1.85, 9.65], [1.16, 1.16], color=DARK, linewidth=1.6)
    axis.plot([1.85, 1.85], [1.16, 1.36], color=DARK, linewidth=1.6)
    axis.plot([9.65, 9.65], [1.16, 1.36], color=DARK, linewidth=1.6)
    axis.text(5.75, 0.78, r"one epoch $=K$ updates", ha="center", va="center", fontsize=14.5, color=DARK)

    axis.plot([8.92, 10.0], [2.13, 2.13], color=DARK, linewidth=1.45)
    axis.plot([10.0, 10.0], [2.13, 6.26], color=DARK, linewidth=1.45)
    arrow(axis, (10.0, 6.26), (9.52, 6.26))
    axis.text(10.25, 4.0, "reshuffle", ha="left", va="center", fontsize=12.5, color=DARK)

    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, bbox_inches="tight", pad_inches=0.03)
    plt.close(figure)


if __name__ == "__main__":
    build_figure(Path(__file__).resolve().parents[1] / "epoch_batches.pdf")
