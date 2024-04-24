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
import csv
import json
import logging
import time
import configparser
from urllib.parse import unquote


config = configparser.ConfigParser()
config.read("config.ini")

logging.basicConfig(level=logging.INFO)
wbi_config["USER_AGENT"] = (
    config["DEFAULT"]["user"]
    + "/1.0 (https://www.wikidata.org/wiki/User:"
    + config["DEFAULT"]["user"]
    + ")"
)

login_instance = wbi_login.Clientlogin(
    user=config["DEFAULT"]["user"], password=config["DEFAULT"]["password"]
)

wbi = WikibaseIntegrator(login=login_instance, is_bot=False)

with open("el_kaikki/trin_matched.json", "r") as readfile:
    file_lines = readfile.readlines()
    for i, line in enumerate(file_lines):
        lemma = json.loads(line)
        if i > 100 and "tria_url" in lemma:
            print(str(i) + lemma["word"])
            new_lexeme = wbi.lexeme.new(lexical_category="Q24905", language="Q36510")
            new_lexeme.lemmas.set(language="el", value=lemma["word"])

            references = [
                [
                    URL(value=unquote(lemma["tria_url"]), prop_nr="P854"),
                    Time(
                        time="+2023-05-02T00:00:00Z",
                        prop_nr="P813",
                        precision=WikibaseDatePrecision.DAY,
                    ),
                    Item(prop_nr="P407", value="Q36510"),
                    MonolingualText(
                        text="Λεξικό της κοινής νεοελληνικής",
                        language="el",
                        prop_nr="P1476",
                    ),
                ]
            ]

            claim1 = Item(prop_nr="P1343", value="Q22906367", references=references)
            new_lexeme.claims.add(claim1)

            new_lexeme.write()
            time.sleep(0.7)
