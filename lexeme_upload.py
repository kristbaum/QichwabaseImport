import csv
import json
import logging
import time
import configparser
from urllib.parse import unquote
from wikibaseintegrator import WikibaseIntegrator, wbi_login
from wikibaseintegrator.datatypes import (
    ExternalID,
    Item,
    String,
    Time,
    URL,
    MonolingualText,
    Form,
    Sense,
)
from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator.wbi_enums import WikibaseDatePrecision

# Read configuration
config = configparser.ConfigParser()
config.read("config.ini")

# Set up logging
logging.basicConfig(level=logging.INFO)
wbi_config["USER_AGENT"] = (
    config["DEFAULT"]["user"]
    + "/1.0 (https://www.wikidata.org/wiki/User:"
    + config["DEFAULT"]["user"]
    + ")"
)

# Login to Wikibase
login_instance = wbi_login.Clientlogin(
    user=config["DEFAULT"]["user"], password=config["DEFAULT"]["password"]
)
wbi = WikibaseIntegrator(login=login_instance, is_bot=False)

# Open the CSV file and read data
with open(
    "datasets/puno_quechua_verbs_with_forms_senses.csv", mode="r", encoding="utf-8"
) as file:
    reader = csv.DictReader(file)
    created_lexemes = []
    for row in reader:
        # Create a new lexeme with the provided information
        new_lexeme = wbi.lexeme.new(
            lexical_category=row["lex_cat_wikidata"], language="qu"
        )
        new_lexeme.lemmas.set(language="qu", value=row["lemma"])

        # Set up references for claims
        references = [
            [
                URL(value=unquote(row["entry"]), prop_nr="P854"),
                Time(
                    time="+2023-05-02T00:00:00Z",
                    prop_nr="P813",
                    precision=WikibaseDatePrecision.DAY,
                ),
                Item(prop_nr="P407", value=row["language"]),
                MonolingualText(
                    text="Lexicon reference",
                    language=row["language"],
                    prop_nr="P1476",
                ),
            ]
        ]

        # Create and add claims
        claim1 = Item(
            prop_nr="P1343", value=row["des_by_source_P1343"], references=references
        )
        new_lexeme.claims.add(claim1)

        # Add senses in four languages
        for lang in ["de", "en", "es", "it"]:
            sense = Sense()
            sense.glosses.set(language=lang, value=row[f"sense1_gloss_{lang}"])
            new_lexeme.senses.add(sense)

        # Add a form
        form = Form()
        form.representations.set(
            language=row["language"], value=row["form1_representation"]
        )
        if "form1_spelling_variant" in row:
            form.grammatical_features.append(row["form1_spelling_variant"])
        new_lexeme.forms.add(form)

        # Write the new lexeme to the Wikibase
        created_lexeme = new_lexeme.write()
        created_lexemes.append(created_lexeme)
        time.sleep(0.7)  # Delay to avoid rate limiting
        exit()  # for testing


# lemma 2 = form with x code
