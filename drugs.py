import enum

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
    OTHER = 1


class Drug:

    def __init__(
        self,
        generic_name,
        brand_names,
        drug_class,
    ):
        self.generic_name = generic_name
        self.brand_names = brand_names
        self.drug_class = drug_class


def create_list_of_antidepressants():
    antidepressants = [
        Drug("citalopram", ["celexa", "cipramil"], AntidepressantClass.SSRI),
        Drug(
            "escitalopram", ["lexapro", "cipralex"], AntidepressantClass.SSRI
        ),
        # Drug("fluoxetine", ["prozac", "sarafem"], AntidepressantClass.SSRI),
        # Drug("fluvoxamine", ["luvox", "faverin"], AntidepressantClass.SSRI),
        # Drug("paroxetine", ["paxil", "seroxat"], AntidepressantClass.SSRI),
        # Drug("sertraline", ["zoloft", "lustral"], AntidepressantClass.SSRI),
        # Drug("desvenlafaxine", ["pristiq"], AntidepressantClass.SNRI),
        # Drug("duloxetine", ["cymbalta"], AntidepressantClass.SNRI),
        # Drug("levomilnacipran", ["fetzima"], AntidepressantClass.SNRI),
        # Drug(
        #     "milnacipran", ["ixel", "savella", "milnaneurax"], AntidepressantClass.SNRI
        # ),
        # Drug(
        #     "venlafaxine", ["effexor", "trevilor"], AntidepressantClass.SNRI
        # ),
        # Drug("vilazodone", ["viibryd"], AntidepressantClass.SMS),
        # Drug(
        #     "vortioxetine", ["trintellix", "brintellix"], AntidepressantClass.SMS
        # ),
        # Drug(
        #     "nefazodone", ["dutonin", "nefadar", "serzone"], AntidepressantClass.SARI
        # ),
        # Drug("trazodone", ["desyrel"], AntidepressantClass.SARI),
        # Drug("reboxetine", ["edronax"], AntidepressantClass.NRI),
        # Drug(
        #     "teniloxazine", ["lucelan", "metatone"], AntidepressantClass.NRI
        # ),
        # Drug("viloxazine", ["vivalan"], AntidepressantClass.NRI),
        # Drug(
        #     "bupropion", ["wellbutrin", "elontril"], AntidepressantClass.NDRI
        # ),
        # Drug("amitriptyline", ["elavil", "endep"], AntidepressantClass.TCA),
        # Drug(
        #     "amitriptylinoxide",
        #     ["amioxid", "ambivalon", "equilibrin"],
        #     AntidepressantClass.TCA,
        # ),
        # Drug("clomipramine", ["anafranil"], AntidepressantClass.TCA),
        # Drug(
        #     "desipramine", ["norpramin", "pertofrane"], AntidepressantClass.TCA
        # ),
        # Drug("dibenzepin", ["noveril", "victoril"], AntidepressantClass.TCA),
        # Drug("dimetacrine", ["istonil"], AntidepressantClass.TCA),
        # Drug("dosulepin", ["prothiaden"], AntidepressantClass.TCA),
        # Drug("doxepin", ["adapin", "sinequan"], AntidepressantClass.TCA),
        # Drug("imipramine", ["tofranil"], AntidepressantClass.TCA),
        # Drug("lofepramine", ["lomont", "gamanil"], AntidepressantClass.TCA),
        # Drug(
        #     "melitracen", ["dixeran", "melixeran", "trausabun"], AntidepressantClass.TCA
        # ),
        # Drug("nitroxazepine", ["sintamil"], AntidepressantClass.TCA),
        # Drug(
        #     "nortriptyline", ["pamelor", "aventyl"], AntidepressantClass.TCA
        # ),
        # Drug(
        #     "noxiptiline", ["agedal", "elronon", "nogedal"], AntidepressantClass.TCA
        # ),
        # Drug("opipramol", ["insidon"], AntidepressantClass.TCA),
        # Drug("pipofezine", ["azafen", "azaphen"], AntidepressantClass.TCA),
        # Drug("protriptyline", ["vivactil"], AntidepressantClass.TCA),
        # Drug("trimipramine", ["surmontil"], AntidepressantClass.TCA),
        # Drug("amoxapine", ["asendin"], AntidepressantClass.TeCA),
        # Drug("maprotiline", ["ludiomil"], AntidepressantClass.TeCA),
        # Drug("mianserin", ["tolvon"], AntidepressantClass.TeCA),
        # Drug("mirtazapine", ["remeron"], AntidepressantClass.TeCA),
        # Drug("setiptiline", ["tecipul"], AntidepressantClass.TeCA),
        # Drug("isocarboxazid", ["marplan"], AntidepressantClass.MAOI),
        # Drug("phenelzine", ["nardil"], AntidepressantClass.MAOI),
        # Drug("tranylcypromine", ["parnate"], AntidepressantClass.MAOI),
        # Drug(
        #     "selegiline", ["eldepryl", "zelapar", "emsam"], AntidepressantClass.MAOI
        # ),
        # Drug("metralindole", ["inkazan"], AntidepressantClass.MAOI),
        # Drug("moclobemide", ["aurorix", "manerix"], AntidepressantClass.MAOI),
        # Drug("pirlindole", ["pirazidol"], AntidepressantClass.MAOI),
        # Drug("bifemelane", ["alnert", "celeport"], AntidepressantClass.MAOI),
        # Drug(
        #     "amisulpride", ["solian"], AntidepressantClass.ATYPICAL_ANTIPSYCHOTICS
        # ),
        # Drug(
        #     "lumateperone", ["caplyta"], AntidepressantClass.ATYPICAL_ANTIPSYCHOTICS
        # ),
        # Drug(
        #     "lurasidone", ["latuda"], AntidepressantClass.ATYPICAL_ANTIPSYCHOTICS
        # ),
        # Drug(
        #     "quetiapine", ["seroquel"], AntidepressantClass.ATYPICAL_ANTIPSYCHOTICS
        # ),
        # Drug("agomelatine", ["valdoxan"], AntidepressantClass.OTHER),
        # Drug(
        #     "brexanolone", ["allopregnanolone", "zulresso"], AntidepressantClass.OTHER
        # ),
        # Drug("esketamine", ["spravato"], AntidepressantClass.OTHER),
        # Drug(
        #     "tianeptine", ["stablon", "coaxil", "tianeurax"], AntidepressantClass.OTHER
        # ),
        # Drug("ketamine", ["ketalar"], AntidepressantClass.OTHER),
        # Drug(
        #     "ademetionine",
        #     ["heptral", "transmetil", "samyl"],
        #     AntidepressantClass.OTHER,
        # ),
        # Drug(
        #     "hypericum perforatum",
        #     ["jarsin", "kira", "movina", "St. John's Wort"],
        #     AntidepressantClass.OTHER,
        # ),
        # Drug(
        #     "oxitriptan",
        #     ["cincofarm", "levothym", "triptum"],
        #     AntidepressantClass.OTHER,
        # ),
        # Drug(
        #     "tryptophan", ["tryptan", "optimax", "aminomine"], AntidepressantClass.OTHER
        # ),
    ]
    return antidepressants


def create_search_keywords_from_drugs(drugs):
    keywords = []
    for drug in drugs:
        keywords.append(drug.generic_name)
        keywords.extend(drug.brand_names)
    return keywords


def get_antidepressant_search_keywords():
    drugs = create_list_of_antidepressants()
    keywords = create_search_keywords_from_drugs(drugs)
    return keywords