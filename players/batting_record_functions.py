from get_player_and_innings import get_batting_innings_table
from batting_functions import best_innings_streak
from batting_functions import best_century_streak
from batting_functions import best_ave_streak
import pandas as pd
from player_id_python_files import three_thousander_dict

def record_run_streak(players, n):
    highest=0
    holder=0
    hundreds=0
    as_dict={}
    count=0
    for player in players:
        all_innings = get_batting_innings_table(player)
        player_name=three_thousander_dict[player]
        player_best_streak, player_hundreds, player_ave=best_innings_streak(n, all_innings)
        as_dict[count]=[player_name, player_best_streak]
        count+=1
        if player_best_streak>highest:
            highest=player_best_streak
            holder=player_name
            hundreds=player_hundreds
    df=pd.DataFrame.from_dict(as_dict, orient='index', columns=["Name", "Runs"])
    top_5=df.nlargest(5, "Runs")
    print(f"{holder.upper()} holds the record! He scored {highest} runs in {n} innings, and made {hundreds} hundreds in this period.")
    print("\nThe top 5 are:\n", top_5.to_string(index=False))

def record_century_streak(players, n):
    highest=0
    holder=0
    runs=0
    as_dict={}
    count=0
    for player in players:
        all_innings = get_batting_innings_table(player)
        player_name=three_thousander_dict[player]
        player_best_streak, player_runs, player_ave=best_century_streak(n, all_innings)
        as_dict[count]=[player_name, player_best_streak]
        count+=1
        if player_best_streak>highest:
            highest=player_best_streak
            holder=player_name
            runs=player_runs
    df=pd.DataFrame.from_dict(as_dict, orient='index', columns=["Name", "Hundreds scored"])
    top_5=df.nlargest(5, "Hundreds scored")
    print(f"{holder.upper()} holds the record! He scored {highest} hundreds in {n} innings, while scoring {runs} runs in this period.")
    print("\nThe top 5 are:\n", top_5.to_string(index=False))

def record_average_streak(players, n):
    highest=0
    holder=0
    runs=0
    hundreds=0
    as_dict={}
    count=0
    for player in players:
        all_innings = get_batting_innings_table(player)
        player_name=three_thousander_dict[player]
        player_best_ave, player_runs, player_hundreds=best_ave_streak(n, all_innings)
        as_dict[count]=[player_name, round(player_best_ave,2)]
        count+=1
        if player_best_ave>highest:
            highest=player_best_ave
            holder=player_name
            runs=player_runs
            hundreds=player_hundreds
    df=pd.DataFrame.from_dict(as_dict, orient='index', columns=["Name", "Average"])
    top_5=df.nlargest(5, "Average")
    print(f"{holder.upper()} holds the record! He has a maximum average of {highest} over {n} innings, while scoring {runs} runs and making {hundreds} hundreds in this period.")
    print("\nThe top 5 are:")
    print(top_5.to_string(index=False))