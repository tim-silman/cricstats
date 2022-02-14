from itertools import groupby
from get_matches import matches

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

