import os
from collections import defaultdict
from typing import Any

import pandas as pd
import numpy as np
import tableone

import matplotlib.pyplot as plt  # type: ignore[import-not-found]
import scienceplots  # type: ignore[import-not-found]

import drugs
from mongodb_helper import mongodb_client
import os


plt.style.use("science")


def read_posts_from_mongodb() -> pd.DataFrame:
    posts = []
    for post in mongodb_client.online_drug_surveillance_db.posts_v2.find():
        posts.append(post)

    return pd.DataFrame(posts)


def create_sentiment_distribution_by_drug_graph(data: pd.DataFrame) -> None:
    mentioned_antidepressants = defaultdict(int)
    for post_mention in data["drugs_used"]:
        for drug in post_mention:
            mentioned_antidepressants[drug["name"].lower()] += 1

    # Get the top 10 objects in dict with highest int value
    top_mentioned_antidepressants = dict(
        sorted(
            mentioned_antidepressants.items(), key=lambda item: item[1], reverse=True
        )[:10]
    )

    sentiment_counts_by_drug = dict()
    sentiment_counts_by_drug = {
        key: {"negative": 0, "neutral": 0, "positive": 0}
        for key in top_mentioned_antidepressants.keys()
    }

    for index, row in data.iterrows():
        for drug in row["drugs_used"]:
            drug_name = drug["name"].lower()
            if drug_name in top_mentioned_antidepressants:
                sentiment_counts_by_drug[drug_name][row["sentiment"]] += 1

    # Calculate the relative percentage of each sentiment for each drug
    sentiment_percentages = {}
    for drug, sentiments in sentiment_counts_by_drug.items():
        total_mentions = sum(sentiments.values())
        positive_percentage = (sentiments["positive"] / total_mentions) * 100
        neutral_percentage = (sentiments["neutral"] / total_mentions) * 100
        negative_percentage = (sentiments["negative"] / total_mentions) * 100
        sentiment_percentages[drug] = {
            "positive": positive_percentage,
            "neutral": neutral_percentage,
            "negative": negative_percentage,
        }

    # Sort the sentiment percentages in descending order of positive percentage
    sorted_sentiment_percentages = sorted(
        sentiment_percentages.items(), key=lambda x: x[1]["positive"], reverse=True
    )

    # Extract the sorted drug names and sentiment percentages
    sorted_drugs = [drug for drug, _ in sorted_sentiment_percentages]
    positive_percentages = [
        sentiments["positive"] for _, sentiments in sorted_sentiment_percentages
    ]
    neutral_percentages = [
        sentiments["neutral"] for _, sentiments in sorted_sentiment_percentages
    ]
    negative_percentages = [
        sentiments["negative"] for _, sentiments in sorted_sentiment_percentages
    ]

    # Create the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(sorted_drugs, negative_percentages, color="red", label="Negative")
    plt.bar(
        sorted_drugs,
        neutral_percentages,
        bottom=negative_percentages,
        color="orange",
        label="Neutral",
    )
    plt.bar(
        sorted_drugs,
        positive_percentages,
        bottom=np.add(negative_percentages, neutral_percentages),
        color="green",
        label="Positive",
    )
    plt.title("Sentiment Distribution by Drug")
    plt.xlabel("Antidepressant")
    plt.ylabel("Percentage")
    plt.xticks(rotation=45, ha="right")
    legend_labels = ["Negative", "Neutral", "Positive"]
    plt.legend(legend_labels, loc="lower left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig("figures/sentiment_distribution_by_drug.png", dpi=300)
    plt.close()


def create_average_adverse_effect_per_drug_table(data: pd.DataFrame) -> None:
    mentioned_antidepressants = defaultdict(int)
    for post_mention in data["drugs_used"]:
        for drug in post_mention:
            mentioned_antidepressants[drug["name"].lower()] += 1

    # Get the top 10 objects in dict with highest int value
    top_mentioned_antidepressants = dict(
        sorted(
            mentioned_antidepressants.items(), key=lambda item: item[1], reverse=True
        )[:10]
    )

    adverse_effects_by_drug = defaultdict(int)
    adverse_effects_by_drug.update(
        {key: 0 for key in top_mentioned_antidepressants.keys()}
    )

    for post_mention in data["drugs_used"]:
        for drug in post_mention:
            drug_name = drug["name"].lower()
            if drug_name in top_mentioned_antidepressants:
                adverse_effects_by_drug[drug_name] += len(drug["adverse_effects"])

    # Divide the total adverse effects by the number of mentions for each drug
    average_num_adverse_effects_per_drug = {
        drug: adverse_effects_by_drug[drug] / top_mentioned_antidepressants[drug]
        for drug in top_mentioned_antidepressants
    }

    # Create a bar graph for each drug showing the average number of adverse effects for each drug
    # Sort the average number of adverse effects per drug in descending order
    sorted_average_effects = sorted(
        average_num_adverse_effects_per_drug.items(), key=lambda x: x[1], reverse=True
    )

    # Extract the sorted drug names and average effects
    sorted_drugs = [drug for drug, _ in sorted_average_effects]
    sorted_effects = [effect for _, effect in sorted_average_effects]

    # Create the bar graph
    plt.figure(figsize=(8, 5))
    plt.bar(sorted_drugs, sorted_effects, color="skyblue")
    plt.title("Average Number of Adverse Effects for Top 10 Antidepressants")
    plt.xlabel("Antidepressant")
    plt.ylabel("Average Number of Adverse Effects")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"figures/average_adverse_effect_per_drug.png", dpi=300)
    plt.close()


def create_per_drug_adverse_effect_frequency_graph(data: pd.DataFrame) -> None:
    mentioned_antidepressants = defaultdict(int)
    for post_mention in data["drugs_used"]:
        for drug in post_mention:
            mentioned_antidepressants[drug["name"].lower()] += 1

    # Get the top 10 objects in dict with highest int value
    top_mentioned_antidepressants = dict(
        sorted(
            mentioned_antidepressants.items(), key=lambda item: item[1], reverse=True
        )[:10]
    )

    adverse_effects_by_drug = {
        key: defaultdict(int) for key in top_mentioned_antidepressants.keys()
    }

    for post_mention in data["drugs_used"]:
        for drug in post_mention:
            drug_name = drug["name"].lower()
            if drug_name in top_mentioned_antidepressants:
                for effect in drug["adverse_effects"]:
                    adverse_effects_by_drug[drug_name][effect] += 1

    # For each key, get the top 10 adverse effects
    top_adverse_effects_by_drug = {
        drug: dict(sorted(effects.items(), key=lambda item: item[1], reverse=True)[:10])
        for drug, effects in adverse_effects_by_drug.items()
    }
    # Create a bar graph for each drug showing the relative percentage of adverse effects over the total times the drug was mentioned in a post
    for drug, effects in top_adverse_effects_by_drug.items():
        total_mentions = top_mentioned_antidepressants[drug]
        effect_percentages = {
            effect: (count / total_mentions) * 100 for effect, count in effects.items()
        }

        plt.figure(figsize=(8, 5))
        plt.bar(effect_percentages.keys(), effect_percentages.values(), color="skyblue")
        plt.title(f"Frequency of Adverse Effects for {drug} (Top 10)")
        plt.xlabel("Adverse Effect")
        plt.ylabel("Percentage Frequency")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        os.makedirs("figures/drug_adverse_effect_frequency", exist_ok=True)
        plt.savefig(f"figures/drug_adverse_effect_frequency/{drug}.png", dpi=300)
        plt.close()


def create_subreddit_average_sentiment_graph(data: pd.DataFrame) -> None:
    # Create a graph that shows the relative frequency of sentiment values for each subreddit
    grouped_data = data.groupby(["subreddit", "sentiment"]).size().unstack()

    # Calculate the relative percentage of each sentiment for each subreddit
    grouped_data["total"] = grouped_data.sum(axis=1)
    grouped_data["positive_percentage"] = (
        grouped_data["positive"] / grouped_data["total"] * 100
    )
    # If there are no neutral posts, set the percentage to 0
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
    sorted_data = grouped_data.sort_values(by="positive_percentage", ascending=False)

    # Create the graph
    plt.figure(figsize=(14, 8))
    sorted_data[
        ["negative_percentage", "neutral_percentage", "positive_percentage"]
    ].plot(kind="bar", stacked=True, color=["red", "orange", "green"])
    plt.title("Percentage of user sentiments by subreddit", fontsize=10)
    plt.xlabel("")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Percentage")
    legend_labels = ["Negative", "Neutral", "Positive"]
    plt.legend(legend_labels, loc="center left", bbox_to_anchor=(1, 0.5))
    plt.savefig("figures/subreddit_average_sentiment_graph.png", dpi=300)
    plt.close()


def create_antidepressant_prescription_vs_mention_frequency_pie_charts(data) -> None:
    """
    Side by side comparison of prescription frequency pie chart
    and post mention frequency in data set.
    """
    # Source of data: https://clincalc.com/DrugStats/TC/SsriAntidepressants
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

    mentioned_antidepressants = defaultdict(int)
    for post_mention in data["drugs_used"]:
        for drug in post_mention:
            mentioned_antidepressants[drug["name"].lower()] += 1

    # Remove from mentioned antidepressants all keys that are not contained within the drug list
    known_antidepressants = [
        drug.generic_name for drug in drugs.create_list_of_antidepressants()
    ]
    mentioned_antidepressants = {
        k: v for k, v in mentioned_antidepressants.items() if k in known_antidepressants
    }

    # Get the top 10 objects in dict with highest int value
    top_mentioned_antidepressants = dict(
        sorted(
            mentioned_antidepressants.items(), key=lambda item: item[1], reverse=True
        )[:10]
    )
    other_mentions = sum(mentioned_antidepressants.values()) - sum(
        top_mentioned_antidepressants.values()
    )
    top_mentioned_antidepressants["other"] = other_mentions

    plt.figure(figsize=(12, 6))

    # Pie chart for top prescribed antidepressants
    plt.subplot(1, 2, 1)
    plt.pie(
        top_prescribed_antidepressants.values(),
        labels=top_prescribed_antidepressants.keys(),
        autopct="%1.1f%%",
        startangle=140,
    )
    plt.title(
        "Relative Frequency of Prescriptions for the Top 10 Antidepressants in the US During 2022"
    )

    # Pie chart for top mentioned antidepressants
    plt.subplot(1, 2, 2)
    plt.pie(
        top_mentioned_antidepressants.values(),
        labels=top_mentioned_antidepressants.keys(),
        autopct="%1.1f%%",
        startangle=140,
    )
    plt.title("Relative Frequency of the Top 10 Antidepressants Mentioned in Posts")

    plt.tight_layout()
    plt.savefig(
        "figures/antidepressant_prescription_vs_mention_frequency_pie_charts.png",
        dpi=300,
    )
    plt.close()


def create_demographics_by_sentiment_table(data: pd.DataFrame) -> None:
    data = data.copy()
    # Set age to not a number if it is 0
    data["age"] = data["age"].replace(0, pd.NA)

    columns = ["age", "gender"]
    groupby = "sentiment"
    categorical = ["gender"]
    continuous = ["age"]
    nonnormal = ["age"]
    rename = {
        "age": "Age",
        "gender": "Gender",
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


def main():
    # data = read_posts_from_csv_file(DATA_FILE_PATH)
    data = read_posts_from_mongodb()

    create_demographics_by_sentiment_table(data)
    create_antidepressant_prescription_vs_mention_frequency_pie_charts(data)
    create_subreddit_average_sentiment_graph(data)
    create_per_drug_adverse_effect_frequency_graph(data)
    create_average_adverse_effect_per_drug_table(data)
    create_sentiment_distribution_by_drug_graph(data)


if __name__ == "__main__":
    main()
