import csv
import configparser
import logging
import time
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

# Set up the range of rows to process
start_row = 1
end_row = 2

# Open the CSV file and read data
created_lexemes = []
with open(
    "datasets/puno_quechua_verbs_with_forms_senses.csv", mode="r", encoding="utf-8"
) as file:
    reader = csv.DictReader(file)
    row_number = 0
    for row in reader:
        row_number += 1
        if row_number < start_row:
            continue
        elif row_number > end_row:
            break

        # Create a new lexeme with the provided information
        new_lexeme = wbi.lexeme.new(
            lexical_category=row["lex_cat_wikidata"], language="qu"
        )
        new_lexeme.lemmas.set(language="qu", value=row["lemma"])

        sense = Sense()
        sense.glosses.set(language="en", value="English gloss")
        sense.glosses.set(language="fr", value="French gloss")
        claim = String(prop_nr="P828", value="Create a string claim for sense")
        sense.claims.add(claim)
        new_lexeme.senses.add(sense)

        form = Form()
        form.representations.set(language="qu", value=row["form1_representation"])
        form.grammatical_features = ["Q179230"]  # Q179230 is infinitive
        new_lexeme.forms.add(form)

        # Set up references for claims
        references = [
            [
                URL(value=unquote(row["entry"]), prop_nr="P854"),
                Time(
                    time="+2024-05-02T00:00:00Z",
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
        created_lexeme = new_lexeme.write()
        created_lexemes.append((created_lexeme.id, row))

        time.sleep(0.7)  # Delay to avoid rate limiting

# Write the new CSV with the Lexeme IDs
new_csv_filename = "datasets/puno_quechua_verbs_with_forms_senses_with_lexeme_ids.csv"
with open(new_csv_filename, mode="w", encoding="utf-8", newline="") as file:
    fieldnames = list(reader.fieldnames) + ["Lexeme_ID"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for lexeme_id, row_data in created_lexemes:
        row_data["Lexeme_ID"] = lexeme_id
        writer.writerow(row_data)
