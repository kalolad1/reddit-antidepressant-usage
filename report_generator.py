from typing import Any

import pandas as pd
import tableone

import matplotlib.pyplot as plt  # type: ignore[import-not-found]
import scienceplots  # type: ignore[import-not-found]

from mongodb import mongodb_client

plt.style.use("science")

DATA_FILE_PATH = "analyzed_posts.csv"


def read_posts_from_csv_file(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def read_posts_from_mongodb() -> pd.DataFrame:
    analyses = []
    for post in mongodb_client.online_drug_surveillance_db.analyzed_posts.find():
        analyses.append(post["analysis"])

    return pd.DataFrame(analyses)


def create_demographics_by_sentiment_table(data: pd.DataFrame) -> None:
    data = data.copy()

    columns = ["age", "gender", "duration_of_treatment"]
    groupby = "sentiment"
    categorical = ["duration_of_treatment", "gender"]
    continuous = ["age"]
    nonnormal = ["age"]
    rename = {
        "age": "Age",
        "gender": "Gender",
        "duration_of_treatment": "Duration of Treatment",
        "sentiment": "Sentiment",
    }

    # Titlecase the sentiment column for better readability
    data["sentiment"] = data["sentiment"].str.title()
    for column in columns:
        if column == "age":
            continue
        data[column] = data[column].str.title()

    table = tableone.TableOne(
        data,
        columns=columns,
        categorical=categorical,
        continuous=continuous,
        groupby=groupby,
        nonnormal=nonnormal,
        rename=rename,
        pval=False,
    )

    table.to_html("figures/demographics_by_sentiment.html")


def create_demographics_by_drug_table(data: pd.DataFrame) -> Any:
    data = data.copy()

    columns = ["age", "gender", "duration_of_treatment", "sentiment"]
    groupby = "drug"
    categorical = ["duration_of_treatment", "gender", "sentiment"]
    continuous = ["age"]
    nonnormal = ["age"]
    rename = {
        "age": "Age",
        "gender": "Gender",
        "duration_of_treatment": "Duration of Treatment",
        "sentiment": "Sentiment",
        "drug": "Drug",
    }

    # Titlecase for better readability
    data["drug"] = data["drug"].str.title()
    for column in columns:
        if column == "age":
            continue
        data[column] = data[column].str.title()

    table = tableone.TableOne(
        data,
        columns=columns,
        categorical=categorical,
        continuous=continuous,
        groupby=groupby,
        nonnormal=nonnormal,
        rename=rename,
        pval=False,
    )

    table.to_html("figures/demographics_by_drug.html")


def create_drug_adverse_effect_count_table(data: pd.DataFrame) -> None:
    # Convert the list of adverse effects to their counts
    print(data)
    data["adverse_effect_count"] = data["adverse_effects"].apply(len)

    # Group the data by drug and calculate the average number of adverse effects per post
    grouped_data = data.groupby("drug")["adverse_effect_count"].mean().reset_index()
    grouped_data["adverse_effect_count"] = grouped_data["adverse_effect_count"].round(2)

    # Sort the data by average number of adverse effects in descending order
    sorted_data = grouped_data.sort_values(by="adverse_effect_count", ascending=False)

    
    # Create the table
    table = plt.table(
        cellText=sorted_data.values,
        colLabels=["Drug", "Average Adverse Effects per Post"],
        cellLoc="center",
        loc="center",
        


    )    # Remove the axis
    plt.axis("off")

    # Save the table as an image
    plt.savefig("figures/drug_adverse_effect_count_table.png", dpi=300)


def create_sentiment_analysis_comparative_bar_graph(data: pd.DataFrame) -> None:
    # Group the data by drug and sentiment
    grouped_data = data.groupby(["drug", "sentiment"]).size().unstack()

    # Calculate the relative percentage of each sentiment for each drug
    grouped_data["total"] = grouped_data.sum(axis=1)
    grouped_data["positive_percentage"] = (
        grouped_data["positive"] / grouped_data["total"] * 100
    )
    try:
        grouped_data["neutral_percentage"] = (
            grouped_data["neutral"] / grouped_data["total"] * 100
        )
    except KeyError:
        grouped_data["neutral"] = 0
        grouped_data["neutral_percentage"] = 0

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


def main():
    # data = read_posts_from_csv_file(DATA_FILE_PATH)
    data = read_posts_from_mongodb()

    create_drug_adverse_effect_count_table(data)
    # create_demographics_by_sentiment_table(data)
    # create_demographics_by_drug_table(data)
    # create_sentiment_analysis_comparative_bar_graph(data)


if __name__ == "__main__":
    main()
