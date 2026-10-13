from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
MONTHS_ABBR = [m[:3] for m in MONTHS]

df = pd.read_csv(
    Path(__file__).with_name("fcc-forum-pageviews.csv"),
    index_col="date",
    parse_dates=True,
)

# Remove the top 2.5% and bottom 2.5% of page views
low, high = df["value"].quantile([0.025, 0.975])
df = df[(df["value"] >= low) & (df["value"] <= high)]


def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df["value"])
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month_name()

    # unstack() sorts month names alphabetically, so force calendar order
    df_pivot = (
        df_bar.groupby(["year", "month"])["value"]
        .mean()
        .unstack()
        .reindex(columns=MONTHS)
    )

    fig, ax = plt.subplots(figsize=(10, 8))
    # 12 months > 10 default colors, so use a palette with enough distinct colors
    df_pivot.plot(kind="bar", ax=ax, colormap="tab20")
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")

    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    df_box = df.copy()
    df_box["year"] = df_box.index.year
    df_box["month"] = df_box.index.strftime("%b")

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # order= keeps Jan..Dec instead of the order months first appear in the data
    sns.boxplot(x="month", y="value", data=df_box, order=MONTHS_ABBR, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig("box_plot.png")
    return fig
