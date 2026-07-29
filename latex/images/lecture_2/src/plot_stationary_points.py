"""Plot stationary extrema and a one-dimensional stationary saddle point."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


DARK_CERULEAN = "#08457D"
DARK_RED = "#8C0000"
PASTEL_BLUE = "#3A82B8"
DRAW_GRAY = "#52646B"
GRID_GRAY = "#D9E0E2"
SADDLE_ORANGE = "#C46A00"

DOMAIN = (0.10, 1.02)
ROOTS = np.asarray([0.15, 0.36, 0.52, 0.52, 0.80, 0.98])
CRITICAL_POINTS = np.unique(ROOTS)
DERIVATIVE = np.poly1d(ROOTS, True)
OBJECTIVE = np.polyint(DERIVATIVE)
DOMAIN_VALUES = OBJECTIVE(np.linspace(*DOMAIN, 1000))
OBJECTIVE_CENTER = (DOMAIN_VALUES.max() + DOMAIN_VALUES.min()) / 2
OBJECTIVE_SCALE = 3 / (DOMAIN_VALUES.max() - DOMAIN_VALUES.min())


def objective(x: np.ndarray | float) -> np.ndarray | float:
    return OBJECTIVE_SCALE * (OBJECTIVE(x) - OBJECTIVE_CENTER)


def plot_extrema(axis: plt.Axes) -> None:
    x = np.linspace(*DOMAIN, 700)
    values = objective(CRITICAL_POINTS)
    axis.plot(x, objective(x), color=DARK_CERULEAN, linewidth=2.8)

    colors = [DARK_RED, PASTEL_BLUE, SADDLE_ORANGE, PASTEL_BLUE, DARK_RED]
    labels = [
        "global maximum",
        "local minimum",
        "saddle point",
        "local maximum",
        "global minimum",
    ]
    label_positions = [
        (0.26, 1.62),
        (0.25, -0.88),
        (0.53, 0.15),
        (0.72, 1.15),
        (0.84, -1.18),
    ]

    for point_x, point_y, color, label, label_position in zip(
        CRITICAL_POINTS,
        values,
        colors,
        labels,
        label_positions,
    ):
        axis.scatter(
            [point_x],
            [point_y],
            s=62,
            color=color,
            edgecolor="white",
            linewidth=1.2,
            zorder=4,
        )
        axis.annotate(
            label,
            xy=(point_x, point_y),
            xytext=label_position,
            color=color,
            fontsize=12.5,
            weight="semibold",
            ha="center",
            arrowprops={
                "arrowstyle": "-",
                "color": color,
                "linewidth": 1.1,
                "shrinkA": 3,
                "shrinkB": 5,
            },
        )

    axis.set_xlim(*DOMAIN)
    axis.set_ylim(-1.75, 1.75)
    axis.set_xlabel(r"$x$")
    axis.set_ylabel(r"$f(x)$")
    axis.set_xticks([])
    axis.set_yticks([])
    axis.spines[["top", "right"]].set_visible(False)
    axis.spines[["bottom", "left"]].set_color(DRAW_GRAY)
    axis.axhline(0, color=GRID_GRAY, linewidth=0.8, zorder=0)
def build_figure(output: Path) -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Fira Sans", "DejaVu Sans"],
            "font.size": 12.5,
            "axes.labelsize": 14,
            "axes.linewidth": 0.9,
            "mathtext.fontset": "cm",
            "pdf.fonttype": 42,
        }
    )

    figure, axis = plt.subplots(figsize=(8.4, 4.15), constrained_layout=True)
    plot_extrema(axis)

    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, bbox_inches="tight", pad_inches=0.03)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "stationary_points.pdf",
    )
    args = parser.parse_args()
    build_figure(args.output)


if __name__ == "__main__":
    main()
