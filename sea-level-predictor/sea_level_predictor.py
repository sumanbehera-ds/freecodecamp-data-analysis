import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def draw_plot():
    df = pd.read_csv("epa-sea-level.csv")

    x = df["Year"]
    y = df["CSIRO Adjusted Sea Level"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y)

    res = linregress(x, y)
    x_pred = pd.Series(range(1880, 2051))
    y_pred = res.intercept + res.slope * x_pred
    ax.plot(x_pred, y_pred)

    df_recent = df[df["Year"] >= 2000]
    x_recent = df_recent["Year"]
    y_recent = df_recent["CSIRO Adjusted Sea Level"]

    res_recent = linregress(x_recent, y_recent)
    x_pred_recent = pd.Series(range(2000, 2051))
    y_pred_recent = res_recent.intercept + res_recent.slope * x_pred_recent
    ax.plot(x_pred_recent, y_pred_recent)

    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Level (inches)")
    ax.set_title("Rise in Sea Level")

    fig.savefig("sea_level_plot.png")
    return fig