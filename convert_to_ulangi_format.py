#!/usr/bin/env python3

import pandas as pd
from itertools import zip_longest

words_data_df = pd.read_excel("output.xlsx")

ulangi_df = pd.DataFrame(columns=["vocabularyText", "definitions"])

for index, row in words_data_df.iterrows():
    vocabularyText = ""

    part_of_speech = row["part of speech"]

    if part_of_speech == "Substantiv":
        gender = row["gender"]
        gender_artikel = ""
        match gender:
            case "Femininum": gender_artikel = "die"
            case "Neutrum": gender_artikel = "das"
            case "Maskulinum": gender_artikel = "der"

        plural = str(row["plural"])

        vocabularyText += gender_artikel + " " + row["word"] + "\n"
        if not plural == "nan":
            vocabularyText += "[plural: " + plural + "]\n"
    elif part_of_speech == "Verb":
        prateritum = str(row["prateritum"])
        perfect = str(row["perfect"])

        vocabularyText += row["word"] + "\n"
        if prateritum == "nan":
            vocabularyText += "[note: " + perfect + "]" + "\n"
        elif perfect == "nan":
            vocabularyText += "[note: " + prateritum + "]" + "\n"
        else:
            vocabularyText += "[note: " + prateritum + ", " + perfect + "]" + "\n"

    else:
        vocabularyText += row["word"] + "\n"

    prefix = ""
    match part_of_speech:
        case "Verb": prefix = "[v]"
        case "Substantiv": prefix = "[n]"
        case "Adverb": prefix = "[adv]"
        case "Adjektiv": prefix = "[adj]"
        case "Präposition": prefix = "[prep]"
        case "Pronomen": prefix = "[pron]"
        case "Konjunktion": prefix = "[konj]"
        case "Interjektion": prefix = "[inter]"
        case "Indefinitpronomen": prefix = "[indpron]"
        case "partizipiales Adjektiv": prefix = "[padj]"
        case "Pronominaladverb": prefix = "[pronadv]"
        case "Possessivpronomen": prefix = "[pospron]"
        case "Demonstrativpronomen": prefix = "[dempron]"
        case "Komparativ": prefix = "[komp]"
        case "Partikel": prefix = "[part]"

    if prefix == "":
        continue

    definitionsText = ""
    definitions = filter(lambda x: x != "nan" and x != "" and x != "None", str(row["definition"]).split("|"))
    examples = filter(lambda x: x != "nan" and x != "" and x != "None", str(row["example"]).split("|"))
    for definition, example in zip_longest(definitions, examples):
        if not definitionsText == "":
            definitionsText += "---\n"

        if definition:
            definitionsText += prefix + " " + definition.strip() + "\n"
        if example:
            definitionsText += "[example: " + example.strip() + "]" + "\n"


    if definitionsText == "" or vocabularyText == "":
        continue

    ulangi_df = pd.concat([ulangi_df, pd.DataFrame({
        "vocabularyText": vocabularyText,
        "definitions": definitionsText
    }, index=[0])], ignore_index=True, sort=False)


ulangi_df.to_excel("ulangi.xlsx")
