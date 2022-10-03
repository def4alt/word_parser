#!/usr/bin/env python3

import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import re

words_data_df = pd.read_excel("words.xlsx")

words = words_data_df["Word"].tolist()

df = pd.DataFrame(columns=["word", "part of speech", "gender", "plural", "prateritum", "perfect", "definition", "example"])

for word in words:
    r = requests.get("https://www.dwds.de/wb/" + word)
    soup = BeautifulSoup(r.content, "html.parser")

    part_of_speech = ""
    gender = ""
    plural = ""
    prateritum = ""
    perfect = ""
    definition = ""
    example = ""

    ft = soup.find("div", class_="dwdswb-ft")
    if ft:
        ft_blocktext = ft.find("span", class_="dwdswb-ft-blocktext")
        if ft_blocktext:
            spans = ft_blocktext.find_all("span")
            parts_and_gender = []
            if len(spans) > 0:
                part_and_gender = spans[0].text.split("(")
                part_of_speech = part_and_gender[0].strip()

            if part_of_speech == "Substantiv":
                if len(part_and_gender) >= 2:
                    gender = part_and_gender[1].replace(")", "").strip()
                bs = ft_blocktext.find_all("b")
                if len(bs) >= 2:
                    plural = bs[1].text

            if part_of_speech == "Verb":
                flexionen = ft_blocktext.find_all("span", class_="dwdswb-flexion-hl")
                if flexionen and len(flexionen) >= 4:
                    prateritum = flexionen[1].text
                    if len(flexionen) == 5:
                        perfect = flexionen[2].text + "/" + flexionen[3].text + " " + flexionen[4].text
                    else:
                        perfect = flexionen[2].text + " " + flexionen[3].text

    for definition_box in soup.find_all("div", {"id": re.compile('^d-[0-9]-[0-9]$')}):
        definition_temp = definition_box.find("span", class_="dwdswb-definition")
        if definition_temp:
            definition += definition_temp.text + "|"

        examples = definition_box.find_all("div", class_="dwdswb-kompetenzbeispiel")

        if examples:
            example_temp = random.choice(examples).find("span", class_="dwdswb-belegtext")
            if example_temp:
                example += example_temp.text + "|"


    if part_of_speech != "":
        df = pd.concat([df, pd.DataFrame({
            "word": word,
            "part of speech": part_of_speech,
            "gender": gender,
            "plural": plural,
            "prateritum": prateritum,
            "perfect": perfect,
            "definition": definition,
            "example": example}, index=[0])], ignore_index=True, sort=False)

df.to_excel("output.xlsx")
