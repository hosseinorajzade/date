from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


def equity_report_png(path, equity: pd.Series, title: str, windows: pd.DataFrame | None = None,
                      benchmark: pd.Series | None = None, stressed: pd.Series | None = None) -> None:
    fig, ax = plt.subplots(3, 1, figsize=(10, 9), gridspec_kw={"height_ratios": [3, 1.3, 1.5]})
    ax[0].plot(equity.index, equity.values, lw=1.2, label="strategy (net of costs)")
    if stressed is not None:
        ax[0].plot(stressed.index, stressed.values, lw=0.9, ls="--", label="1.5x costs")
    if benchmark is not None:
        ax[0].plot(benchmark.index, benchmark.values, lw=0.8, alpha=0.6, label="buy & hold")
    ax[0].set_yscale("log")
    ax[0].set_title(title)
    ax[0].legend(loc="upper left")
    ax[0].grid(alpha=0.3)
    dd = 1 - equity / equity.cummax()
    ax[1].fill_between(dd.index, -dd.values * 100, 0, color="tab:red", alpha=0.5)
    ax[1].set_ylabel("drawdown %")
    ax[1].grid(alpha=0.3)
    if windows is not None and len(windows):
        col = ["tab:green" if r > 0 else "tab:red" for r in windows["ret"]]
        ax[2].bar(range(len(windows)), windows["ret"] * 100, color=col)
        ax[2].set_ylabel("window return %")
        ax[2].set_xlabel("walk-forward window")
        ax[2].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
