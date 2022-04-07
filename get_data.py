import json
import pandas as pd


def extract_data():
    with open("intents.json") as file:
        data = json.load(file)

    tag = []
    pat = []
    res = []
    ids = []

    for i, intent in enumerate(data["intents"]):
        ids += [i]
        tag += [intent["tag"]]
        pat += [intent["patterns"]]
        res += [intent["responses"]]

    referdf = pd.DataFrame({"ids": ids, "tag": tag, "patterns": pat, "responses": res})
    traindf = pd.DataFrame({"ids": ids, "patterns": pat})
    traindf = traindf.explode("patterns", ignore_index=True)

    referdf.to_csv("response.csv", index=False)
    traindf.to_csv("train.csv", index=False)



extract_data()