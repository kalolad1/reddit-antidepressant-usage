from typing import Any

import pandas as pd
import tableone

import matplotlib.pyplot as plt  # type: ignore[import-not-found]
import scienceplots  # type: ignore[import-not-found]

from mongodb import mongodb_client

plt.style.use("science")


def read_posts_from_mongodb() -> pd.DataFrame:
    posts = []
    for post in mongodb_client.online_drug_surveillance_db.analyzed_posts.find():
        posts.append(post)

    return pd.DataFrame(posts)


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
    )  # Remove the axis
    plt.axis("off")

    # Save the table as an image
    plt.savefig("figures/drug_adverse_effect_count_table.png", dpi=300)


def create_per_drug_adverse_effect_frequency_graph(data: pd.DataFrame) -> None:
    # Group the data by drug and adverse effect
    df = data[["drug", "adverse_effects"]].copy()

    # Count the number of posts (records) for each drug
    drug_counts = df["drug"].value_counts()

    # Select the top 10 drugs by post count
    top_10_drugs = drug_counts.nlargest(10).index

    # Filter the DataFrame to include only the top 10 drugs
    df_top_10 = df[df["drug"].isin(top_10_drugs)]

    # Explode the list of adverse effects to create one row per effect
    df_exploded = df_top_10.explode("adverse_effects")

    # Group the data by Drug and Adverse Effects
    grouped = (
        df_exploded.groupby(["drug", "adverse_effects"]).size().unstack(fill_value=0)
    )

    # Calculate percentage frequency
    percentage_grouped = grouped.div(grouped.sum(axis=1), axis=0) * 100

    # Plot a separate bar graph for each drug
    for drug in percentage_grouped.index:
        effect_percentages = percentage_grouped.loc[drug].sort_values(ascending=False)

        plt.figure(figsize=(8, 5))
        effect_percentages.plot(kind="bar", color="skyblue")
        plt.title(f"Percentage of Adverse Effects for {drug} (Ranked)")
        plt.xlabel("Adverse Effect")
        plt.ylabel("Percentage Frequency")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()


def create_drug_perscription_relative_frequency_pie_chart() -> None:
    """
    Source of data: https://clincalc.com/DrugStats/TC/SsriAntidepressants

    """
    # Data for the top most prescribed antidepressants, number of prescriptions in
    # the US 2022
    top_prescribed_antidepressants = {
        "sertraline": 39900000,
        "escitalopram": 30800000,
        "fluoxetine": 24000000,
        "citalopram": 15000000,
        "duloxetine": 13500000,
        "bupropion": 10500000,
        "venlafaxine": 9100000,
        "paroxetine": 7100000,
        "mirtazapine": 5400000,
        "amitriptyline": 4300000,
        "other": 80400000,
    }

    # Create a pie chart using matplotlib
    plt.figure(figsize=(8, 8))
    plt.pie(
        top_prescribed_antidepressants.values(),
        labels=top_prescribed_antidepressants.keys(),
        autopct="%1.1f%%",
        startangle=140,
    )
    plt.title(
        "Relative Frequency of Prescriptions for the Top 20 Antidepressants in the US During 2022"
    )
    plt.savefig("figures/drug_prescription_relative_frequency_pie_chart.png", dpi=300)


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
    # data = read_posts_from_mongodb()

    create_drug_perscription_relative_frequency_pie_chart()
    # create_per_drug_adverse_effect_frequency_graph(data)
    # create_drug_adverse_effect_count_table(data)
    # create_demographics_by_sentiment_table(data)
    # create_demographics_by_drug_table(data)
    # create_sentiment_analysis_comparative_bar_graph(data)


if __name__ == "__main__":
    main()
