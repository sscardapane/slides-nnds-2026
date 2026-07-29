"""Compare full-batch GD and mini-batch SGD on the same objective."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


DARK_CERULEAN = "#08457D"
DARK_RED = "#8C0000"
PASTEL_BLUE = "#789ECC"
DRAW_GRAY = "#52646B"
GRID_GRAY = "#D9E0E2"


def full_batch_loss(iterations: int, learning_rate: float) -> np.ndarray:
    theta = 4.0
    losses = []
    for _ in range(iterations + 1):
        losses.append(0.5 * theta**2)
        theta -= learning_rate * theta
    return np.asarray(losses)


def minibatch_loss(
    iterations: int,
    learning_rate: float,
    batch_size: int,
    seed: int,
) -> np.ndarray:
    random = np.random.default_rng(seed)
    theta = 4.0
    losses = []
    for _ in range(iterations + 1):
        losses.append(0.5 * theta**2)
        gradient_noise = random.normal(scale=1.0 / np.sqrt(batch_size))
        theta -= learning_rate * (theta + gradient_noise)
    return np.asarray(losses)


def log_loss(values: np.ndarray) -> np.ndarray:
    return np.log10(np.maximum(values, 1e-3))


def build_figure(output: Path) -> None:
    iterations = 60
    learning_rate = 0.10
    batch_size = 8
    updates = np.arange(iterations + 1)

    full = full_batch_loss(iterations, learning_rate)
    runs = np.stack(
        [
            minibatch_loss(iterations, learning_rate, batch_size, seed)
            for seed in range(200)
        ]
    )
    mean = runs.mean(axis=0)
    log_runs = log_loss(runs)
    displayed_runs = log_runs[[3, 17, 29, 52, 83, 127, 173]]

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Fira Sans", "DejaVu Sans"],
            "font.size": 13,
            "axes.labelsize": 14,
            "axes.titlesize": 15,
            "axes.linewidth": 0.9,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "mathtext.fontset": "cm",
            "pdf.fonttype": 42,
        }
    )

    figure, axes = plt.subplots(
        1,
        2,
        figsize=(10.6, 3.25),
        sharex=True,
        sharey=True,
        constrained_layout=True,
    )

    for axis in axes:
        axis.set_xlim(0, iterations)
        axis.set_ylim(-3.1, 1.05)
        axis.set_xticks([0, 20, 40, 60])
        axis.set_yticks([-3, -2, -1, 0, 1])
        axis.grid(color=GRID_GRAY, linewidth=0.7, alpha=0.85)
        axis.spines[["top", "right"]].set_visible(False)
        axis.tick_params(colors=DRAW_GRAY)
        axis.set_xlabel("update $t$")

    axes[0].set_ylabel(r"$\log_{10}\mathcal{L}(\boldsymbol{\theta}_t)$")
    axes[0].set_title("Full-batch GD", color=DARK_CERULEAN, weight="semibold")
    axes[1].set_title(
        rf"Mini-batch SGD  $(B={batch_size})$",
        color=DARK_RED,
        weight="semibold",
    )

    axes[0].plot(
        updates,
        log_loss(full),
        color=DARK_CERULEAN,
        linewidth=2.8,
        label=r"$\mathcal{L}(\boldsymbol{\theta}_t)$",
    )

    for index, run in enumerate(displayed_runs):
        axes[1].plot(
            updates,
            run,
            color=PASTEL_BLUE,
            linewidth=1.15,
            alpha=0.58,
            label="SGD runs" if index == 0 else None,
        )
    axes[1].plot(
        updates,
        log_loss(mean),
        color=DARK_RED,
        linewidth=2.8,
        label="mean over runs",
    )

    axes[1].legend(loc="upper right", frameon=False, fontsize=10.5)

    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, bbox_inches="tight", pad_inches=0.03)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "full_vs_minibatch.pdf",
    )
    args = parser.parse_args()
    build_figure(args.output)


if __name__ == "__main__":
    main()
