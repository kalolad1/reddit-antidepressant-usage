import enum
from typing import List


class AntidepressantClass(enum.Enum):
    SSRI = 1
    SNRI = 2
    SMS = 3
    SARI = 4
    NRI = 5
    NDRI = 6
    TCA = 7
    TeCA = 8
    MAOI = 9
    ATYPICAL_ANTIPSYCHOTICS = 10
    OTHER = 11


class Drug:

    def __init__(
        self,
        generic_name: str,
        brand_names: List[str],
        drug_class: AntidepressantClass,
    ) -> None:
        self.generic_name = generic_name
        self.brand_names = brand_names
        self.drug_class = drug_class


def create_list_of_antidepressants() -> List[Drug]:
    antidepressants = [
        Drug("citalopram", ["celexa", "cipramil"], AntidepressantClass.SSRI),
        Drug("escitalopram", ["lexapro", "cipralex"], AntidepressantClass.SSRI),
        Drug("fluoxetine", ["prozac", "sarafem"], AntidepressantClass.SSRI),
        Drug("paroxetine", ["paxil", "seroxat"], AntidepressantClass.SSRI),
        Drug("sertraline", ["zoloft", "lustral"], AntidepressantClass.SSRI),
        Drug("duloxetine", ["cymbalta"], AntidepressantClass.SNRI),
        Drug("milnacipran", ["savella", "ixel"], AntidepressantClass.SNRI),
        Drug("venlafaxine", ["effexor", "trevilor"], AntidepressantClass.SNRI),
        Drug("trazodone", ["desyrel"], AntidepressantClass.SARI),
        Drug("bupropion", ["wellbutrin", "elontril"], AntidepressantClass.NDRI),
        Drug("amitriptyline", ["elavil", "endep"], AntidepressantClass.TCA),
        Drug("clomipramine", ["anafranil"], AntidepressantClass.TCA),
        Drug("doxepin", ["adapin", "sinequan"], AntidepressantClass.TCA),
        Drug("imipramine", ["tofranil"], AntidepressantClass.TCA),
        Drug("nortriptyline", ["pamelor", "aventyl"], AntidepressantClass.TCA),
        Drug("mirtazapine", ["remeron"], AntidepressantClass.TeCA),
        Drug("isocarboxazid", ["marplan"], AntidepressantClass.MAOI),
        Drug("phenelzine", ["nardil"], AntidepressantClass.MAOI),
        Drug("selegiline", ["eldepryl", "zelapar", "emsam"], AntidepressantClass.MAOI),
        Drug("quetiapine", ["seroquel"], AntidepressantClass.ATYPICAL_ANTIPSYCHOTICS),
        Drug("esketamine", ["spravato"], AntidepressantClass.OTHER),
        Drug("ketamine", ["ketalar"], AntidepressantClass.OTHER),
        Drug(
            "tryptophan", ["tryptan", "optimax", "aminomine"], AntidepressantClass.OTHER
        ),
    ]
    return antidepressants


def create_search_keywords_from_drugs(drugs: List[Drug]) -> List[str]:
    keywords = []
    for drug in drugs:
        keywords.append(drug.generic_name)
        keywords.extend(drug.brand_names)
    return keywords


def get_antidepressant_search_keywords() -> List[str]:
    drugs = create_list_of_antidepressants()
    keywords = create_search_keywords_from_drugs(drugs)
    return keywords
