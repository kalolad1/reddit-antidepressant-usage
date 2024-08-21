import csv
import enum
import warnings
from typing import Any, Dict, List

import dotenv # type: ignore[import-not-found]
import openai
import pydantic
import transformers # type: ignore[import-not-found]

dotenv.load_dotenv()
client = openai.OpenAI( # type: ignore[attr-defined]
    api_key="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",
)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=FutureWarning)
    model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    sentiment_analysis_classifier = transformers.pipeline(
        "text-classification", 
        model=model_path,
        tokenizer=model_path,
        max_length=512,
        truncation=True)


class AdverseEffect(enum.Enum):
    NAUSEA = "nausea"
    DRY_MOUTH = "dry mouth"
    DROWSINESS = "drowsiness"
    INSOMNIA = "insomnia"
    WEIGHT_GAIN = "weight gain"
    SEXUAL_DYSFUNCTION = "sexual dysfunction"
    HEADACHE = "headache"
    DIZZINESS = "dizziness"
    ANXIETY = "anxiety"
    FATIGUE = "fatigue"
    SWEATING = "sweating"
    CONSTIPATION = "constipation"
    DIARRHEA = "diarrhea"
    INCREASED_HEART_RATE = "increased heart rate"
    TREMORS = "tremors"
    BLURRED_VISION = "blurred vision"
    RESTLESSNESS = "restlessness"
    AGITATION = "agitation"
    INCREASED_APPETITE = "increased appetite"
    DECREASED_APPETITE = "decreased appetite"
    MUSCLE_ACHES = "muscle aches"
    DRY_EYES = "dry eyes"
    RASH = "rash"
    NIGHTMARES = "nightmares"
    INCREASED_BLOOD_PRESSURE = "increased blood pressure"
    YAWNING = "yawning"
    HOT_FLASHES = "hot flashes"
    CHILLS = "chills"
    MEMORY_PROBLEMS = "memory problems"
    CONFUSION = "confusion"
    DIFFICULTY_CONCENTRATING = "difficulty concentrating"
    LIGHTHEADEDNESS = "lightheadedness"
    FEELING_FAINT = "feeling faint"
    IRRITABILITY = "irritability"
    MANIC_EPISODES = "manic episodes (in people with bipolar disorder)"
    SEIZURES = "seizures (rare but possible)"
    ERECTILE_DYSFUNCTION = "erectile dysfunction"
    DELAYED_EJACULATION = "delayed ejaculation"
    LOSS_OF_LIBIDO = "loss of libido"
    WEIGHT_LOSS = "weight loss"
    ABDOMINAL_PAIN = "abdominal pain"
    FLATULENCE = "flatulence"
    BRUISING = "bruising"
    SWELLING_IN_EXTREMITIES = "swelling in extremities"
    DECREASED_BLOOD_PRESSURE_UPON_STANDING = "decreased blood pressure upon standing"
    EXCESSIVE_THIRST = "excessive thirst"
    INCREASED_URINATION = "increased urination"
    SHORTNESS_OF_BREATH = "shortness of breath"
    CHEST_PAIN = "chest pain"
    MOOD_SWINGS = "mood swings"


class DurationOfTreatment(enum.Enum):
    LESS_THAN_ONE_MONTH = "less than one month"
    ONE_TO_SIX_MONTHS = "one to six months"
    SIX_TO_TWELVE_MONTHS = "six to twelve months"
    MORE_THAN_ONE_YEAR = "more than one year"

class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"

class PostCharactersticsExtraction(pydantic.BaseModel):
    adverse_effects: list[AdverseEffect]
    duration_of_treatment: DurationOfTreatment
    drug: str
    dose: str
    age: int
    gender: Gender

def get_sentiment_score(post: Dict[str, str]) -> str:
    sentiment = sentiment_analysis_classifier(post["title"] + " " + post["selftext"])
    return str(sentiment[0]["label"])


POST_CHARACTERSTICS_PROMPT = """
You are an expert at structured data extraction. 

You will be given unstructured text from a reddit post about 
someones experience with antidepressants and should extract 
the following characteristics and convert it into the given structure.

For the drug, provide only a single generic name.
If a brand name drug is present convert it to its corresponding generic name.

If the post does not contain a specific characteristic, leave it blank.

If the post contains multiple values for a characteristic,
choose the most relevant one.

Lowercase all text.
"""

def get_post_characteristics(post: Dict[str, str]) -> Any:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": POST_CHARACTERSTICS_PROMPT,
            },
            {"role": "user", "content": f"Title: {post["title"]} Body: {post["selftext"]}"},
        ],
        response_format=PostCharactersticsExtraction,
    )

    extraction = completion.choices[0].message
    return vars(extraction.parsed)

def analyze_post(post: Dict[str, str]) -> Any:
    sentiment = get_sentiment_score(post)
    post_characteristics = get_post_characteristics(post)
    return {"sentiment": sentiment} | post_characteristics


def analyze_posts(posts: List[Dict[str, str]]) -> List[Dict[str, str]]:
    analyzed_posts = []
    for post in posts:
        post_analysis = analyze_post(post)
        analyzed_posts.append({"post_id": post["post_id"]} | post_analysis)
        print(analyzed_posts[-1])
    return analyzed_posts


def write_analyzed_posts_to_csv_file(analyzed_posts: List[Dict[str, Any]]) -> None:
    with open("analyzed_posts.csv", "w") as file:
        file.write("post_id,sentiment,adverse_effects,duration_of_treatment,drug,dose,age,gender\n")
        
        for post in analyzed_posts:
            post_id = post["post_id"]
            sentiment = post["sentiment"]
            adverse_effects = ",".join([effect.value for effect in post["adverse_effects"]])
            duration_of_treatment = post["duration_of_treatment"].value
            drug = post["drug"]
            dose = post["dose"]
            age = post["age"] if post["age"] != 0 else ""
            gender = post["gender"].value

            file.write(f"{post_id},{sentiment},\"{adverse_effects}\",{duration_of_treatment},{drug},{dose},{age},{gender}\n")


def read_posts_from_csv_file(file_path: str) -> List[Dict[str, str]]:
    posts = []
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            posts.append({"title": row["title"], "selftext": row["selftext"], "post_id": row["post_id"]})
    return posts


if __name__ == "__main__":
    posts = read_posts_from_csv_file("filtered_posts.csv")
    print(f"Total posts to analyze: {len(posts)}")

    analyzed_posts = analyze_posts(posts)
    write_analyzed_posts_to_csv_file(analyzed_posts)
