import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

import json
import sys

def get_page_matches (i):
    endpoint = "https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;page="+str(i)+";template=results;type=aggregate;view=results"
    response = requests.get(endpoint)
    soup = BeautifulSoup(response.content, "html.parser")
    match_ids = []
    match_links=soup.find_all("a", attrs={"href":re.compile("match/\d\d*.html")})
    for link in match_links:
        match_id = link["href"].split("/")[-1][:-5]
        match_ids.append(match_id)
    table=soup.tbody
    rows=table.find_all("tr")
    count=0
    page_matches={}
    for row in rows:
        data=row.find_all("td")
        result=data[1].string
        if result in ["draw", "canc", "aban"]:
            winner="N/A"
            margin="N/A"
        else:
            winner=data[0].string
            margin=data[2].string
        teams=data[4].string
        ground=data[5].string
        date=data[6].string
        match_dict={"Match ID": match_ids[count], "Teams": teams, "Date":date, "Ground": ground, "Result":result, "Winner": winner, "Margin":margin}
        page_matches[match_ids[count]]=match_dict
        count+=1
    return page_matches

# with open("all_matches.txt", "w") as f:
#     all_matches={}
#     for i in range(1,51):
#         all_matches.update(get_page_matches(i))
#     print(len(all_matches))
#     f.write(json.dumps(all_matches))





