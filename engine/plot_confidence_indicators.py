import matplotlib.pyplot as plt
import pandas as pd

def plot_confidence_indicators(res, res_df):
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(12, 10))
    ord = res_df["time"].astype("int32")
    ts = [pd.Timestamp.fromordinal(d) for d in ord]
    ax1_0 = ax1.twinx()
    ax1.plot(ts, res_df["price"], color="black", linewidth=1.5)
    ax1_0.plot(
        ts,
        res_df["pos_conf"],
        label="bubble indicator (pos)",
        color="red",
        alpha=0.8,
        linewidth=1.5,
    )
    ax2_0 = ax2.twinx()
    ax2.plot(ts, res_df["price"], color="black", linewidth=1.5)
    ax2_0.plot(
        ts,
        res_df["neg_conf"],
        label="bubble indicator (neg)",
        color="green",
        alpha=0.8,
        linewidth=1.5,
    )
    ax1.grid(which="major", axis="both", linestyle="--")
    ax2.grid(which="major", axis="both", linestyle="--")
    ax1.set_ylabel("ln(p)")
    ax2.set_ylabel("ln(p)")
    ax1_0.set_ylabel("bubble indicator (pos)")
    ax2_0.set_ylabel("bubble indicator (neg)")
    ax1_0.legend(loc=2)
    ax2_0.legend(loc=2)
    ax2.tick_params(axis='x', labelsize=14) 