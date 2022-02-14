from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from Player import Player

def find_player(search_term):
    endpoint = "https://search.espncricinfo.com/ci/content/site/search.html"
    params = {"search": search_term}
    response = requests.get(endpoint, params=params)
    soup=BeautifulSoup(response.content, "html.parser")
    results=soup.find("ul", attrs={"class": re.compile("player-list")})
    while results==None:
        search_term=input("Player not found. Please enter another player name")
        params = {"search": search_term}
        response = requests.get(endpoint, params=params)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find("ul", attrs={"class": re.compile("player-list")})
    player_names=[]
    player_ids=[]
    for player in results.find_all("li"):
        link=player.a["href"]
        full_name=player.p.get_text()
        initialised=player.h3.get_text()
        country=player.find("p", attrs={"class":re.compile("country")}).string
        player_names.append(f"{full_name} ({initialised}; {country})")
        player_ids.append(re.search("/\d*\.", link).group()[1:-1])
    if len(player_names)==1:
        player_name=player_names[0].split(",")[0]
        player_id=int(player_ids[0])
    else:
        n=len(player_names)
        print(f"\n{n} results found:")
        for i in range(n):
            print(i+1, player_names[i])
        selection=int(input(f"\nPlease select by entering a number between 1 and {n}:"))
        player_name=player_names[selection-1].split(",")[0]
        player_id=int(player_ids[selection-1])
    return Player(player_id, player_name)

def get_batting_innings_table(player):
    url="https://stats.espncricinfo.com/ci/engine/player/"+str(player.player_id)+".html?class=1;template=results;type=batting;view=innings"
    df=pd.read_html(url, match='Opposition')[0]
    df["Not out"]=df.Runs.apply(lambda x: 1 if "*" in x else 0)
    df.Runs=df.Runs.str.replace("*", "", regex=False)
    df=df[(df.Runs!="DNB")&(df.Runs!="TDNB")&(df.Runs!="absent")&(df.Runs!="sub")]
    df=df.drop(["Ground", "Unnamed: 13", "Unnamed: 9", "Dismissal", "Mins"], axis=1)
    df["Runs"]=df["Runs"].astype(int)
    # df[["Runs", "4s", "6s", "Pos", "Inns"]]=df[["Runs",  "4s", "6s", "Pos", "Inns"]].astype(int)
    # df["SR"]=df["SR"].astype(float)
    df=df.reset_index()
    return df

def get_batting_innings_dict(player):
    url = "https://stats.espncricinfo.com/ci/engine/player/" + str(
        player.player_id) + ".html?class=1;template=results;type=batting;view=innings"
    df = pd.read_html(url, match='Opposition')[0]
    df["Not out"] = df.Runs.apply(lambda x: 1 if "*" in x else 0)
    df.Runs = df.Runs.str.replace("*", "", regex=False)
    df = df[(df.Runs != "DNB") & (df.Runs != "TDNB") & (df.Runs != "absent") & (df.Runs != "sub")]
    df = df.drop(["Ground", "Unnamed: 13", "Unnamed: 9", "Dismissal", "Mins", "4s", "6s", "Pos", "Inns", "SR", "BF", "Opposition", "Start Date"], axis=1)
    df["Runs"] = df["Runs"].astype(int)
    df = df.reset_index()
    innings_dict=df.to_dict("records")
    return innings_dict

sanga=get_batting_innings_dict(find_player("sangakkara"))
print(sanga[23]["Runs"])

def get_bowling_innings_table(player):
    url = "https://stats.espncricinfo.com/ci/engine/player/" + str(
        player.player_id) + ".html?class=1;template=results;type=bowling;view=innings"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    matches = soup.find_all("a", attrs={"title": "view the scorecard for this row"})
    match_ids = []
    for match in matches:
        match_id = match["href"].split("/")[-1][:-5]
        match_ids.append(match_id)
    df = pd.read_html(url, match='Opposition')[0]
    df["Match_ID"]=match_ids
    df = df[(df.Overs != "DNB") & (df.Overs != "TDNB") & (df.Overs != "absent") & (df.Overs != "sub")]
    df["Overs"]=df["Overs"].astype(str)
    df["Overs"]=df.Overs.str.split(".")
    df["Balls"]=df.Overs.apply(lambda x: 6*int(x[0])+int(x[1]))
    # df = df.drop(["Mdns", "Pos", "Unnamed: 7", "Unnamed: 11", "Ground", "Start Date", "Econ"], axis=1)
    df["IDX"]=range(len(df))
    df[["Runs", "Wkts"]]=df[["Runs",  "Wkts"]].astype(int)
    df = df.reset_index()
    return df

def get_bowling_matches(innings):
    matches=innings.groupby("Match_ID").sum()
    matches=matches.sort_values("IDX")
    return matches


def get_200_wicket_club():
    response=requests.get("https://stats.espncricinfo.com/ci/content/records/93276.html")
    soup=BeautifulSoup(response.content, "html.parser")
    best_bowlers_as_lst=[]
    best_bowlers_as_objects=[]
    for row in soup.tbody.find_all("tr"):
        data=row.find_all("td")[0]
        player_name=data.a.get_text()
        player_id=int(data.a["href"].split("/")[-1][:-5])
        bowler=Player(player_id, player_name)
        best_bowlers_as_objects.append(bowler)
        best_bowlers_as_lst.append([player_name, player_id])
    return best_bowlers_as_lst, best_bowlers_as_objects

best_bowlers=get_200_wicket_club()[1]
"""
RangeIndex: 208778 entries, 0 to 208777
Data columns (total 28 columns):

RangeIndex: 233 entries, 0 to 232
Data columns (total 11 columns):

and most doubles

something like main but for the record functions. 

and longest streak sustaining an average above x? sounds harder

most important probably to try and get the innings table via BS instead of read html to make it smaller and faster?

"""

