import pandas as pd
import json
import sys
import re
from datetime import datetime
from Match import Match
import string
from bs4 import BeautifulSoup
import requests

with open("/cricinfo/teams_matches/matches_revised.txt") as g:
    all_match_dict=json.loads(g.read())

def format_date(date):
    to_conv="0"+date if len(date)==10 else date
    return datetime.strptime(to_conv, "%d %b %Y")

team_dict={"Afghanistan": "AFG", "Australia":"AUS", "Bangladesh":"BAN", "England":"ENG", "India":"IND", "Ireland":"Ire", "New Zealand":"NZ", "Pakistan":"PAK", "South Africa":"SA", "Sri Lanka":"SL", "West Indies":"WO", "Zimbabwe":"ZIM" }

for key in all_match_dict:
    all_match_dict[key]["Date"]=format_date(all_match_dict[key]["Date"])
    if all_match_dict[key]["Winner"] in team_dict.keys():
        all_match_dict[key]["Winner"]= team_dict[all_match_dict[key]["Winner"]]


matches=[]
for key in all_match_dict.keys():
    my_match=Match(key, all_match_dict[key]["Home"], all_match_dict[key]["Away"], all_match_dict[key]["Date"], all_match_dict[key]["Ground"], all_match_dict[key]["Winner"], all_match_dict[key]["Margin"])
    matches.append(my_match)


def get_match_id():
    series_results=[]
    while len(series_results)==0:
        x=input("Enter the home team (Aus, Ban, Eng, Ind, NZ, Pak, SA, SL, WI, Zim)").upper()
        y=input("Enter the away team (Aus, Ban, Eng, Ind, NZ, Pak, SA, SL, WI, Zim)").upper()
        z=int(input("Enter the year"))
        for match in matches:
            if match.home==x and match.away==y and match.date.year-1<=z<=match.date.year+1:
                series_results.append(match)
        if len(series_results)==1:
            match_id=match
        elif len(series_results)>1:
            print(f"\nThere were {len(series_results)} tests played in {x} by {y} from {z-1} to {z+1}:")
            count=1
            for game in series_results:
                print(f"\t{count}: {game}")
                count+=1
            m=int(input(f"\nPlease choose a match by entering a number between 1 and {len (series_results)}"))
            match_id=series_results[m-1]
        else:
            print("No matches found")
    return match_id

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
new_matches=[]
# def update_matches(i=1):
#     endpoint = "https://stats.espncricinfo.com/ci/engine/stats/index.html?class="+str(i)+";orderby=start;orderbyad=reverse;page=1;template=results;type=aggregate;view=results"
#     response = requests.get(endpoint)
#     soup = BeautifulSoup(response.content, "html.parser")
#     new_match_ids = []
#
#     match_links = soup.find_all("a", attrs={"href": re.compile("match/\d\d*.html")})
#     for link in match_links:
#         match_id = link["href"].split("/")[-1][:-5]
#         if match_id not in all_match_dict.keys():
#             new_match_ids.append(match_id)
#     table = soup.tbody
#     rows = table.find_all("tr")
#     count=0
#     team_dict={"Afghanistan": "AFG", "Australia":"AUS", "Bangladesh":"BAN", "England":"ENG", "India":"IND", "Ireland":"Ire", "New Zealand":"NZ", "Pakistan":"PAK", "South Africa":"SA", "Sri Lanka":"SL", "West Indies":"WO", "Zimbabwe":"ZIM" }
#     for row in rows:
#         data = row.find_all("td")
#         result = data[1].string
#         if result in ["draw", "canc", "aban"]:
#             winner = result
#             margin = "N/A"
#         else:
#             winner = data[0].string
#             margin = data[2].string
#         teams = data[4].string
#         home=team_dict[teams.split(" v ")[0]]
#         away=team_dict[teams.split(" v ")[1]]
#         ground = data[5].string
#         date = format_date(data[6].string)
#         row_match=Match(match_id, home, away, date, ground, winner, margin)
#         if row_match not in matches:
#             new_matches.append(row_match)
#             count+=1
#
#
#     if count==50:
#         print("run again with i=2")
#     return f"{count} matches added", new_matches
#
# update_matches()
# j=matches[-1]
# k=new_matches[0]
# for i in [j,k]:
#     print(i.date, i.home, i.away, i.ground, i.margin, i.matchID, i.winner)


