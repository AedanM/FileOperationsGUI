"""Get episodes from wikipedia."""

from io import StringIO
from pathlib import Path

import requests
from pandas import read_html, to_numeric
from wikipedia import exceptions, page

from Src.Utilities.UtilityTools import MakeStringSystemSafe

MASTER_FOLDER = Path(r".\Episode Listings")
UA = {"User-Agent": "Aedan McHale (aedan.mchale@gmail.com)"}


def GetHTML(topic: str) -> str:
    try:
        html = page(topic).html()
    except exceptions.PageError:
        r = requests.get(
            f"http://en.wikipedia.org/w/api.php?action=parse&prop=text&page={topic}&format=json",
            timeout=1000,
            headers=UA,
        )
        html = r.json()["parse"]["text"]["*"]
    return html


def LoadEpisodes(topic: str, _isShow: bool) -> str:
    html = GetHTML(topic)

    season = 1
    epList = []
    for df in read_html(StringIO(html)):
        keyList = "".join([str(x) for x in list(df.keys())])
        if "Title" in keyList and "No." in keyList:
            badTitle = [str(x) for x in df if "Title" in str(x)][0]
            badSeason = [str(x) for x in df if "No." in str(x)]
            if len(badSeason) > 1:
                badSeason = [x for x in badSeason if "overall" not in x][0]
            else:
                badSeason = badSeason[0]
            df = df.rename(
                columns={
                    badSeason: "epNum",
                    badTitle: "Title",
                },
            )
            df = df[["epNum", "Title"]]
            df = df[to_numeric(df["epNum"], errors="coerce").notna()]  # pyright: ignore[reportAttributeAccessIssue]
            for _idx, row in df.iterrows():
                epList.append(
                    f"S{season:02d}E{int(row['epNum']):02d},{row['Title'].replace('?', '')}",
                )
            season += 1
    if epList:
        topic = topic.replace("(TV Series)", "")
        MASTER_FOLDER.mkdir(exist_ok=True)
        with (MASTER_FOLDER / f"{MakeStringSystemSafe(topic)}_Episodes.csv").open(mode="w") as fp:
            fp.write("\n".join(epList))
        return f"{MASTER_FOLDER / f'{MakeStringSystemSafe(topic)}_Episodes.csv'} Written"
    return "ERROR None Found"
