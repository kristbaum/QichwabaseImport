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
    for row in reader:
        # Create a new lexeme with the provided information
        new_lexeme = wbi.lexeme.new(
            lexical_category=row["lex_cat_wikidata"], language=row["language"]
        )
        new_lexeme.lemmas.set(language=row["language"], value=row["lemma"])

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

        # Write the new lexeme to the Wikibase
        new_lexeme.write()
        time.sleep(0.7)  # Delay to avoid rate limiting
        exit() # for testing
