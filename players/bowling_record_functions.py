from get_player_and_innings import get_bowling_innings_table
from bowling_functions import best_bowling_innings_streak
from bowling_functions import best_bowling_matches_streak
from bowling_functions import best_fivefer_streak
from bowling_functions import best_bowling_ave_streak_inns
from bowling_functions import best_bowling_ave_streak_match
from get_player_and_innings import best_bowlers
from get_player_and_innings import get_bowling_matches
import pandas as pd


def record_wicket_innings_streak(players, n):
    highest=0
    holder=0
    fivefers=0
    ave=0
    as_dict={}
    count=0
    for player in players:
        all_innings = get_bowling_innings_table(player)
        if len(all_innings)>=n:
            player_name=player.player_name
            player_best_streak, player_fivefers, player_ave=best_bowling_innings_streak(n, all_innings)
            as_dict[count]=[player_name, player_best_streak]
            count+=1
            if player_best_streak>highest:
                highest=player_best_streak
                holder=player_name
                fivefers=player_fivefers
                ave=player_ave
    df=pd.DataFrame.from_dict(as_dict, orient='index', columns=["Name", "Wickets"])
    top_5=df.nlargest(5, "Runs")
    print(f"{holder.upper()} holds the record! He took {highest} wickets in {n} innings, and made {fivefers} fivefers in this period, averaging {ave}.")
    print("\nThe top 5 are:\n", top_5.to_string(index=False))

def record_wicket_match_streak(players, n):
    highest=0
    holder=0
    ave=0
    as_dict={}
    count=0
    for player in players:
        all_innings = get_bowling_innings_table(player)
        matches=get_bowling_matches(all_innings)
        player_name=player.player_name
        if len(matches)>=n:
            player_best_streak, player_ave=best_bowling_matches_streak(n, matches)
            as_dict[count]=[player_name, player_best_streak]
            count+=1
            if player_best_streak>highest:
                highest=player_best_streak
                holder=player_name
                ave=player_ave
    df=pd.DataFrame.from_dict(as_dict, orient='index', columns=["Name", "Wickets"])
    top_5=df.nlargest(5, "Wickets")
    print(f"{holder.upper()} holds the record! He took {highest} wickets in {n} matches, while averaging {ave}.")
    print("\nThe top 5 are:\n", top_5.to_string(index=False))

def record_bowling_ave_streak_inns(players, n):
    lowest = 100
    holder = 0
    wickets = 0
    fivefers = 0
    as_dict = {}
    count = 0
    for player in players:
        all_innings = get_bowling_innings_table(player)
        if len(all_innings)>=n:
            player_name = player.player_name
            player_best_ave, player_wickets, player_fivefers = best_bowling_ave_streak_inns(n, all_innings)
            as_dict[count] = [player_name, round(player_best_ave, 2)]
            count += 1
            if player_best_ave <lowest:
                 lowest = player_best_ave
                holder = player_name
                wickets=player_wickets
                fivefers=player_fivefers
    df = pd.DataFrame.from_dict(as_dict, orient='index', columns=["Name", "Average"])
    top_5 = df.nsmallest(5, "Average")
    print(
        f"{holder.upper()} holds the record! He has a lowest average of {lowest} over {n} innings. He took taking {wickets} wickets  inlcuding {fivefers} 5 wicket hauls in this period.")
    print("\nThe top 5 are:")
    print(top_5.to_string(index=False))

def record_bowling_ave_streak_match(players, n):
    lowest = 100
    holder = 0
    wickets = 0
    as_dict = {}
    count = 0
    for player in players:
        all_innings = get_bowling_innings_table(player)
        matches=get_bowling_matches(all_innings)
        player_name = player.player_name
        if len(matches)>=n:
            player_best_ave, player_wickets = best_bowling_ave_streak_match(n, matches)
            print(player_name, player_best_ave)
            as_dict[count] = [player_name, round(player_best_ave, 2)]
            count += 1
            if player_best_ave <lowest:
                lowest = player_best_ave
                holder = player_name
                wickets=player_wickets
    df = pd.DataFrame.from_dict(as_dict, orient='index', columns=["Name", "Average"])
    top_5 = df.nsmallest(5, "Average")
    print(
        f"{holder.upper()} holds the record! He has a lowest average of {lowest} over {n} matches, and took {wickets} wickets  in this period.")
    print("\nThe top 5 are:")
    print(top_5.to_string(index=False))

record_bowling_ave_streak_match(best_bowlers, 50)