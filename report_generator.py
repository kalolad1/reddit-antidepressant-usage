import pandas as pd

import matplotlib.pyplot as plt

DATA_FILE_PATH = "analyzed_posts.csv"


def read_posts_from_csv_file(file_path):
    return pd.read_csv(file_path)

def create_sentiment_analysis_comparative_bar_graph(data):
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
    sorted_data = grouped_data.sort_values(by="positive_percentage", ascending=False)

    # Create the graph
    plt.figure(figsize=(10, 6))
    sorted_data[["negative_percentage", "neutral_percentage", "positive_percentage"]].plot(
        kind="bar", stacked=True
    )
    plt.xlabel("Drug")
    plt.ylabel("Percentage")
    plt.title("Sentiment Analysis by Drug")
    plt.legend(loc="lower right")
    plt.show()


def create_post_stats_table(data):
    grouped_data = data.groupby(["drug", "sentiment"]).size().unstack()
    grouped_data["total"] = grouped_data.sum(axis=1)
    print(grouped_data)


    fig, ax = plt.subplots()
    ax.axis("off")
    ax.table(cellText=grouped_data.values, colLabels=grouped_data.columns, rowLabels=grouped_data.index, loc="center")
    plt.show()

    return grouped_data


def main():
    data = read_posts_from_csv_file(DATA_FILE_PATH)
    create_post_stats_table(data)
    # create_sentiment_analysis_comparative_bar_graph(data)


if __name__ == "__main__":
    main()
