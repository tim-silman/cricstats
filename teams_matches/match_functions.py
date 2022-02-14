import requests
import re
from get_matches import matches
import Match
from get_matches import get_match_id
from itertools import groupby

def get_response_and_teams (matchid):
    endpoint = "https://site.api.espn.com/apis/site/v2/sports/cricket/19430/summary"
    params = {"event": matchid}
    response = requests.get(endpoint, params=params).json()
    team0name=response["rosters"][0]["team"]["displayName"]
    team1name=response["rosters"][1]["team"]["displayName"]
    return (response, team0name, team1name)

def toss_and_innings_decision(response, team0name, team1name):
    global team0_bat_inn, team1_bat_inn
    team0roster = response["rosters"][0]["roster"]
    team1roster = response["rosters"][1]["roster"]
    toss=response["notes"][5]["text"]
    tosswinner=toss.split()[0]
    tossdecision="bat" if "bat" in toss else "field"
    if (tosswinner==team0name and tossdecision=="bat") or (tosswinner==team1name and tossdecision=="field"):
        team0_bat_inn=[1,3]
        team1_bat_inn=[2,4]
    if (tosswinner==team1name and tossdecision=="bat") or (tosswinner==team0name and tossdecision=="field"):
        team0_bat_inn=[2,4]
        team1_bat_inn=[1,3]

    print(f"{tosswinner} won the toss and chose to {tossdecision}.  Therefore, {team0name} batted in innings {team0_bat_inn[0]} and {team0_bat_inn[1]}. {team1name} batted in innings {team1_bat_inn[0]} and {team1_bat_inn[1]} ")
    input_bat_team=input(f"Do you want to see the card for {team0name} or {team1name}?")
    input_innings=int(input("And which innings number?"))
    innings=input_innings-1
    roster=team0roster if input_bat_team==team0name else team1roster
    # need to add in  a prompt etc. if either input field is invalid
    return roster, innings

def player_by_player(roster, innings):
    century_makers = []
    highest_scorer = "blank"
    highest_score=0
    for i in range(11):
        player_name=(roster[i]["athlete"]["lastName"]).upper()
        try:
            runs=roster[i]["linescores"][innings]["linescores"][0]["statistics"]["categories"][0]["stats"][17]["value"]
        except:
            print(f"{player_name} did not bat\n")
        try:
            shorttext=re.sub("&dagger;", "", roster[i]["linescores"][innings]["linescores"][0]["statistics"]["batting"]["outDetails"]["shortText"])
        except:
            print(f"{player_name} did not bat\n")
        if runs>100:
            century_makers.append(player_name)
        if runs>highest_score:
            highest_score=runs
            highest_scorer=player_name
        if shorttext!="not out":
            text=roster[i]["linescores"][innings]["linescores"][0]["statistics"]["batting"]["outDetails"]["details"]["text"]
        how_out = f"{player_name} was {shorttext} for {runs}!\nDescription: {text}"
        if shorttext=="not out":
            print(f"{player_name} finished not out for {runs}\n")
        else:
            print(how_out, "\n")
    return highest_scorer, highest_score, century_makers

def high_scorers (highest_scorer, highest_score, century_makers):
    centurystrtolast=", ".join(century_makers[:-1])
    highest_scorer=highest_scorer
    #  may need editing cos can have euqal top scorers
    if len(century_makers)==0:
        century_string=f"Nobody made a century.  {highest_scorer} top scored with {highest_score}."
    elif len(century_makers)==1:
        century_string=f"{highest_scorer} made a century and top scored with {highest_score}."
    else:
        century_string=f"{centurystrtolast} and {century_makers[-1]} made centuries. {highest_scorer} top scored with {highest_score}"

    print(century_string)

def main():
    matchid=input("Enter the match ID")
    response, team0name, team1name=get_response_and_teams(matchid)
    roster, innings=toss_and_innings_decision(response, team0name, team1name)
    highest_scorer, highest_score, century_makers=player_by_player(roster, innings)
    high_scorers(highest_scorer, highest_score, century_makers)

def most_consecutive_match_up_wins(team, opposition):
    match_ups=[]
    for match in matches:
        if (match.home==team or match.home==opposition) and (match.away==team or match.away==opposition):
            match_ups.append(match)
    groups=[]
    for k, g in groupby(match_ups, lambda x: x.winner):
        groups.append(list(g))
    longest_streak=0
    longest_group=0
    for group in groups:
        if group[0].winner==team and len(group)>longest_streak:
            longest_streak=len(group)
            longest_group=group
    return longest_streak, longest_group[0].date, longest_group[-1].date

def get_team_match_streaks(team):
    team_matches = []
    for match in matches:
        if match.home == team or match.away == team:
            team_matches.append(match)
    groups = []
    for k, g in groupby(team_matches, lambda x: x.winner):
        groups.append(list(g))
    return groups

def most_consecutive_wins(team):
    team_streaks=get_team_match_streaks(team)
    longest_streak = 0
    longest_streak_groupby = 0
    for streak in team_streaks:
        if streak[0].winner == team and len(streak) > longest_streak:
            longest_streak = len(streak)
            longest_streak_groupby = streak
    return longest_streak, longest_streak_groupby[0].date, longest_streak_groupby[-1].date

def most_consecutive_defeats(team):
    team_streaks = get_team_match_streaks(team)
    longest_streak = 0
    longest_streak_groupby = 0
    for streak in team_streaks:
        # may be better way of writing this...defeat is where the other team has won, i.e. winner is home and team is away or vice versa
        if ((streak[0].winner == streak[0].home and streak[0].away==team) or (streak[0].winner == streak[0].away and streak[0].home==team))  and len(streak) > longest_streak:
            longest_streak = len(streak)
            longest_streak_groupby= streak
    return longest_streak, longest_streak_groupby[0].date, longest_streak_groupby[-1].date


