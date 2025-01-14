from io import StringIO
from pathlib import Path

import pandas as pd
import requests
import wikipedia as wp
from Src.Utilities.FileExplorerTools import MakeStringSystemSafe

MASTER_FOLDER = Path(r".\Episode Listings")
UA = {"User-Agent": "Aedan McHale (aedan.mchale@gmail.com)"}


def GetHTML(topic) -> str:
    try:
        html = wp.page(topic).html()
    except wp.exceptions.PageError:
        r = requests.get(
            f"http://en.wikipedia.org/w/api.php?action=parse&prop=text&page={topic}&format=json",
            timeout=1000,
            headers=UA,
        )
        html = r.json()["parse"]["text"]["*"]
    return html


def LoadEpisodes(topic, _isShow):
    html = GetHTML(topic)

    season = 1
    epList = []
    for df in pd.read_html(StringIO(html)):
        keyList = "".join([str(x) for x in list(df.keys())])
        if "Title" in keyList and "No." in keyList:
            badTitle = [str(x) for x in df.keys() if "Title" in x][0]
            badSeason = [str(x) for x in df.keys() if "No." in x]
            if len(badSeason) > 1:
                badSeason = [x for x in badSeason if "overall" not in x][0]
            else:
                badSeason = badSeason[0]
            df = df.rename(
                columns={
                    badSeason: "epNum",
                    badTitle: "Title",
                }
            )
            df = df[["epNum", "Title"]]
            df = df[pd.to_numeric(df["epNum"], errors="coerce").notna()]
            for _idx, row in df.iterrows():
                epList.append(
                    f"S{season:02d}E{int(row["epNum"]):02d},{row["Title"].replace('?','')}"
                )
            season += 1
    if epList:
        topic = topic.replace("(TV Series)", "")
        with (MASTER_FOLDER / f"{MakeStringSystemSafe(topic)}_Episodes.csv").open(mode="w") as fp:
            fp.write("\n".join(epList))
        return f'{MASTER_FOLDER / f"{MakeStringSystemSafe(topic)}_Episodes.csv"} Written'
    return "ERROR None Found"
