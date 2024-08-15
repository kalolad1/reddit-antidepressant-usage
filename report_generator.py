from typing import Any

import pandas as pd

import matplotlib.pyplot as plt  # type: ignore[import-not-found]
import scienceplots  # type: ignore[import-not-found]

plt.style.use("science")

DATA_FILE_PATH = "analyzed_posts.csv"


def read_posts_from_csv_file(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def create_sentiment_analysis_comparative_bar_graph(data: pd.DataFrame) -> None:
    # Group the data by drug and sentiment
    grouped_data = data.groupby(["drug", "sentiment"]).size().unstack()

    # Calculate the relative percentage of each sentiment for each drug
    grouped_data["total"] = grouped_data.sum(axis=1)
    grouped_data["positive_percentage"] = (
        grouped_data["positive"] / grouped_data["total"] * 100
    )
    grouped_data["neutral_percentage"] = (
        grouped_data["neutral"] / grouped_data["total"] * 100
    )
    grouped_data["negative_percentage"] = (
        grouped_data["negative"] / grouped_data["total"] * 100
    )

    # Sort the data by most positive to least positive
    sorted_data = grouped_data.sort_values(by="positive_percentage", ascending=False)  # type: ignore[call-overload]

    # Keep only the top 10 drugs by post count
    top_10_drugs = sorted_data.head(10)

    # Create the graph
    plt.figure(figsize=(14, 8))
    top_10_drugs[
        ["negative_percentage", "neutral_percentage", "positive_percentage"]
    ].plot(kind="bar", stacked=True, color=["red", "orange", "green"])
    plt.title("Percentage of user sentiments by drug (Top 10)", fontsize=10)
    plt.xlabel("")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Percentage")
    legend_labels = ["Negative", "Neutral", "Positive"]
    plt.legend(legend_labels, loc="center left", bbox_to_anchor=(1, 0.5))
    plt.savefig("figures/sentiment_analysis_comparative_bar_graph_top_10.png", dpi=300)


def create_post_stats_table(data: pd.DataFrame) -> Any:
    grouped_data = data.groupby(["drug", "sentiment"]).size().unstack()
    grouped_data["total"] = grouped_data.sum(axis=1)
    grouped_data = grouped_data.fillna(0).astype(int)
    grouped_data.loc["total"] = grouped_data.sum()

    fig, ax = plt.subplots()
    ax.axis("off")
    ax.table(
        cellText=grouped_data.values,
        colLabels=grouped_data.columns,
        rowLabels=grouped_data.index,
        loc="center",
    )

    plt.savefig("figures/sentiment_analysis_count_table.png", dpi=300)


def main():
    data = read_posts_from_csv_file(DATA_FILE_PATH)
    create_post_stats_table(data)
    create_sentiment_analysis_comparative_bar_graph(data)


if __name__ == "__main__":
    main()
