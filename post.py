import enum
import hashlib
from typing import List, Optional, Union
import uuid


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


class Analysis:
    def __init__(
        self,
        drug: str,
        sentiment: str,
        age: Optional[int],
        gender: Gender,
        dose: str,
        adverse_effects: List[AdverseEffect],
        duration_of_treatment: DurationOfTreatment,
    ):
        self.age = age
        self.gender = gender
        self.drug = drug
        self.dose = dose
        self.adverse_effects = adverse_effects
        self.duration_of_treatment = duration_of_treatment
        self.sentiment = sentiment


class Post:
    def __init__(
        self,
        title: str,
        content: str,
        analysis: Optional[Analysis] = None,
    ) -> None:
        self.title = title
        self.content = content
        self.analysis = analysis
        self.post_id = hashlib.sha256(f"{title}{content}".encode()).hexdigest()

    def __str__(self) -> str:
        if self.analysis:
            return f"Title: {self.title[:20]}\nContent: {self.content[:20]}\nPostID: {self.post_id}\nAnalysis: {self.analysis.__dict__}"
        else:
            return f"Title: {self.title[:20]}\nContent: {self.content[:20]}\nPostID: {self.post_id}"
