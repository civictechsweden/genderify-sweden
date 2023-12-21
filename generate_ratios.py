import pandas as pd
from genderify import Genderify

URL_2021 = "https://www.scb.se/contentassets/5a07e6b5601f49ffbb1f31a14d0ad59f/namn-med-minst-tva-barare-31-december-2021_20220404.xlsx"
URL_2022 = "https://www.scb.se/globalassets/namn-med-minst-tva-barare-31-december-2022_20230228.xlsx"
# file = pd.ExcelFile(requests.get(URL_2022).content)
file = pd.ExcelFile("namn-med-minst-tva-barare-31-december-2022_20230228.xlsx")


def get_from_excel(name_type, gender):
    df = pd.read_excel(file, f"{name_type} {gender}", skiprows=4)
    df.rename(columns={name_type: "name", "Antal bärare": "popularity"}, inplace=True)
    df["name"] = df["name"].apply(Genderify.lowercase_and_normalise)
    df = df.groupby("name").aggregate({"popularity": "sum"})

    print(f"{len(df)} unika {name_type} för {gender} (totalt {df['popularity'].sum()})")

    return df


def smart_merge(df1, df2, sum_on="popularity"):
    df = pd.merge(df1, df2, on=["name"], how="outer")
    df = df.fillna(0)
    df["popularity"] = df[f"{sum_on}_x"] + df[f"{sum_on}_y"]
    df["ratio"] = df[f"{sum_on}_x"] / df["popularity"]
    df["ratio"] = df["ratio"].round(3)
    df["ambiguousness"] = 1 - abs(df["ratio"] - 0.5) * 2

    return df[["popularity", "ratio", "ambiguousness"]]


tilltalsnamn_women = get_from_excel("Tilltalsnamn", "kvinnor")
tilltalsnamn_men = get_from_excel("Tilltalsnamn", "män")

df = smart_merge(tilltalsnamn_women, tilltalsnamn_men)
df = df.sort_values("popularity", ascending=False)


def save_json(df, filename):
    df["ratio"].to_json(filename, force_ascii=False, indent=4)


save_json(df, "gender.json")
save_json(df[df["popularity"] > 7], "gender_99.json")
save_json(df[df["popularity"] > 2], "gender_998.json")

writer = pd.ExcelWriter("gender.xlsx", engine="xlsxwriter")


def add_tab(name, df):
    df.to_excel(writer, sheet_name=name)


df["gender_99"] = df["ratio"].apply(lambda x: Genderify.gender_from_ratio(x, 0.02))
df["gender_90"] = df["ratio"].apply(lambda x: Genderify.gender_from_ratio(x, 0.2))

add_tab("all", df)

writer.close()
