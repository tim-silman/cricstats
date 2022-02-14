from django.db import models
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from .player_id_python_files import three_thousander_dict
# Create your models here.

def find_player(search_term):
    endpoint = "https://search.espncricinfo.com/ci/content/site/search.html"
    params = {"search": search_term}
    response = requests.get(endpoint, params=params)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find("ul", attrs={"class": re.compile("player-list")})
    while results == None:
        search_term = input("Player not found. Please enter another player name")
        params = {"search": search_term}
        response = requests.get(endpoint, params=params)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find("ul", attrs={"class": re.compile("player-list")})
    player_names = []
    player_ids = []
    for player in results.find_all("li"):
        link = player.a["href"]
        full_name = player.p.get_text()
        initialised = player.h3.get_text()
        country = player.find("p", attrs={"class": re.compile("country")}).string
        player_names.append(f"{full_name} ({initialised}; {country})")
        player_ids.append(re.search("/\d*\.", link).group()[1:-1])
    if len(player_names) == 1:
        id = player_ids[0]
    else:
        n = len(player_names)
        print(f"\n{n} results found:")
        for i in range(n):
            print(i + 1, player_names[i])
        selection = int(input(f"\nPlease select by entering a number between 1 and {n}:"))
        id = player_ids[selection - 1]
    return Player.objects.get(player_id=id)

class Player(models.Model):
    player_name=models.CharField(max_length=50)
    player_id=models.CharField(max_length=10)

    def __str__(self):
        return f"{self.player_name} (ID: {self.player_id})"

    def get_batting_innings_table(self):
        url = "https://stats.espncricinfo.com/ci/engine/player/" + str(
            self.player_id) + ".html?class=1;template=results;type=batting;view=innings"
        df = pd.read_html(url, match='Opposition')[0]
        df["Not out"] = df.Runs.apply(lambda x: 1 if "*" in x else 0)
        df.Runs = df.Runs.str.replace("*", "", regex=False)
        df = df[(df.Runs != "DNB") & (df.Runs != "TDNB") & (df.Runs != "absent") & (df.Runs != "sub")]
        df = df.drop(["Ground", "Unnamed: 13", "Unnamed: 9", "Dismissal", "Mins", "4s", "6s", "Pos", "Inns", "SR", "BF",
                      "Opposition", "Start Date"], axis=1)
        df["Runs"] = df["Runs"].astype(int)
        df = df.reset_index()
        innings_list = df.to_dict("records")
        for innings in innings_list:
            var_name="inns" + str(innings["index"])
            var_name=batting_innings(player=self, runs=innings["Runs"], not_out=innings["Not out"])
            var_name.save()

    def get_bowling_innings_table(self):
        url = "https://stats.espncricinfo.com/ci/engine/player/" + str(
        self.player_id) + ".html?class=1;template=results;type=bowling;view=innings"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        matches = soup.find_all("a", attrs={"title": "view the scorecard for this row"})
        match_ids = []
        for match in matches:
            match_id = match["href"].split("/")[-1][:-5]
            match_ids.append(match_id)
        df = pd.read_html(url, match='Opposition')[0]
        df["Match_ID"] = match_ids
        df = df[(df.Overs != "DNB") & (df.Overs != "TDNB") & (df.Overs != "absent") & (df.Overs != "sub")]
        df["Overs"] = df["Overs"].astype(str)
        df["Overs"] = df.Overs.str.split(".")
        df["Balls"] = df.Overs.apply(lambda x: 6 * int(x[0]) + int(x[1]))
        df = df.drop(["Mdns", "Pos", "Unnamed: 7", "Unnamed: 11", "Ground", "Start Date", "Econ"], axis=1)
        df["IDX"] = range(len(df))
        df[["Runs", "Wkts"]] = df[["Runs", "Wkts"]].astype(int)
        df = df.reset_index()
        return df

    def best_innings_streak(self, n):
        qset=batting_innings.objects.filter(player=self)
        all_innings=pd.DataFrame.from_records(qset.values())
        career = len(all_innings)
        if n > career:
            return None
        else:
            max = 0
            tons_in_best_streak = 0
            ave_in_best_streak = 0
            for i in range(career - n):
                df = all_innings.iloc[i:i + n]
                tot = df.runs.sum()
                if tot > max:
                    max = tot
                    tons_in_best_streak = len(df[df.runs >= 100])
                    ave_in_best_streak = round(df.runs.sum() / (df.runs.count() - df["not_out"].sum()), 2)
        return max, tons_in_best_streak, ave_in_best_streak

class batting_innings(models.Model):
    player=models.ForeignKey(Player, on_delete=models.CASCADE)
    runs=models.PositiveIntegerField()
    not_out=models.BooleanField()

def record_run_streak(n):
    highest=0
    holder=0
    hundreds=0
    as_dict={}
    count=0
    players=three_thousander_dict
    for indiv in players:
        batsman=Player.objects.get(player_id=int(indiv))
        if len(batting_innings.objects.filter(player=batsman))>=n:
            player_best_streak, player_hundreds, player_ave=batsman.best_innings_streak(n)
            as_dict[count]=[batsman.player_name, player_best_streak, player_hundreds, player_ave]
            count+=1
            if player_best_streak>highest:
                highest=player_best_streak
                holder=batsman.player_name
                hundreds=player_hundreds
    df=pd.DataFrame.from_dict(as_dict, orient='index', columns=["Name", "Runs", "100", "Ave"])
    top_5=df.nlargest(5, "Runs")
    top_5_dict=top_5.to_dict("records")
    # print(f"{holder.upper()} holds the record! He scored {highest} runs in {n} innings, and made {hundreds} hundreds in this period.")
    # print("\nThe top 5 are:\n", top_5.to_string(index=False))
    return top_5_dict

