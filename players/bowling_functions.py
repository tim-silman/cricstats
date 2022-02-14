from get_player_and_innings import find_player
from get_player_and_innings import get_bowling_innings_table
from get_player_and_innings import get_bowling_matches

def best_bowling_innings_streak (n, all_innings):
    career=len(all_innings)
    if n>career:
        return None
    else:
        max=0
        fivefers_in_best_streak=0
        ave_in_best_streak=0
        for i in range(career-n):
            df=all_innings.iloc[i:i+n]
            tot=df.Wkts.sum()
            if tot>max:
                max=tot
                fivefers_in_best_streak=len(df[df.Wkts>=5])
                ave_in_best_streak = round(df.Runs.sum() / (df.Wkts.sum()),2)
    return max, fivefers_in_best_streak, ave_in_best_streak

def best_bowling_matches_streak (n, matches):
    career=len(matches)
    if n>career:
        return None
    else:
        max=0
        ave_in_best_streak=0
        for i in range(career-n):
            df=matches.iloc[i:i+n]
            tot=df.Wkts.sum()
            if tot>max:
                max=tot
                ave_in_best_streak = round(df.Runs.sum() / (df.Wkts.sum()),2)
    return max, ave_in_best_streak

def best_fivefer_streak (n, all_innings):
    career=len(all_innings)
    if n>career:
        return None
    else:
        max=0
        wickets_in_best_streak=0
        ave_in_best_streak=0
        for i in range(career-n):
            df=all_innings.iloc[i:i+n]
            tot=len(df[df.Wkts>=5])
            if tot>max:
                max=tot
                wickets_in_best_streak=df.Wkts.sum()
                ave_in_best_streak = round(df.Runs.sum() / (df.Wkts.sum()),2)
    return max, wickets_in_best_streak, ave_in_best_streak

def best_bowling_ave_streak_inns (n, all_innings):
    career = len(all_innings)
    if n > career:
        return None
    else:
        min_ave = 1000
        wickets_in_best_streak = 0
        fivefers_in_best_streak = 0
        for i in range(career - n):
            df = all_innings.iloc[i:i + n]
            ave = df.Runs.sum() / df.Wkts.sum()
            if ave < min_ave:
                min_ave = round(ave,2)
                wickets_in_best_streak = df.Wkts.sum()
                fivefers_in_best_streak = len(df[df.Wkts>=5])
    return min_ave, wickets_in_best_streak, fivefers_in_best_streak

def best_bowling_ave_streak_match (n, matches):
    career = len(matches)
    if n > career:
        return None
    else:
        min_ave = 1000
        wickets_in_best_streak = 0
        for i in range(career - n):
            df = matches.iloc[i:i + n]
            ave = df.Runs.sum() / df.Wkts.sum()
            if ave < min_ave:
                min_ave = round(ave,2)
                wickets_in_best_streak = df.Wkts.sum()

    return min_ave, wickets_in_best_streak

def bowling_summary(all_innings):
    no_innings=len(all_innings)
    matches=get_bowling_matches(all_innings)
    no_matches=len(matches)
    average=round(all_innings.Runs.sum()/(all_innings.Wkts.sum()),2)
    most_wkts=all_innings[all_innings.Wkts==all_innings.Wkts.max()]
    BBI=str(all_innings.Wkts.max())+"/"+str(most_wkts.Runs.min())
    fivefers=len(all_innings[all_innings.Wkts>=5])
    fourfers=len(all_innings[all_innings.Wkts>=4])
    tenfers=len(matches[matches.Wkts>=10])
    econ=round(all_innings.Runs.sum()/(all_innings.Balls.sum()/6), 2)
    summary_string=f"\tMatches: {no_matches}\n\tInnings bowled: {no_innings}\n\tAverage: {average}\n\tBest innings bowling: {BBI}\n\t4 fors: {fourfers}\n\t5 fors: {fivefers}\n\t10 fers: {tenfers}\n\tEconomy rate: {econ}"
    return summary_string

def main():
    search_term=input("Enter a player name")
    player=find_player(search_term)
    all_innings=get_bowling_innings_table(player)
    matches=get_bowling_matches(all_innings)
    print("\nBowling stats for "+player.player_name+":")
    print(bowling_summary(all_innings))
    n=int(input("\nEnter a value for 'n' to see their best streak of wickets taken in 'n' innings, or 0 to skip."))
    if n==0:
        print("")
    else:
        max_wickets, fivefers_in_best_streak, ave_in_best_streak=best_bowling_innings_streak(n, all_innings)
        print(f"{player.player_name} has a best streak of {max_wickets} wickets in {n} innings. He took {fivefers_in_best_streak} 5 wicket hauls in this period, averaging {ave_in_best_streak}.")
    j = int(input("\nEnter a value for 'n' to see their best streak of wickets taken in 'n' matches, or 0 to skip."))
    if j == 0:
        print("")
    else:
        max_wickets_m, ave_in_best_streak_m = best_bowling_matches_streak(j, matches)
        print(
            f"{player.player_name} has a best streak of {max_wickets_m} wickets in {j} matches. He averaged {ave_in_best_streak_m} in this period.")
    l = int(
        input("\nEnter a value for n to see their lowest bowling average for a streak of 'n' innings, or 0 to skip."))
    if l == 0:
        print("")
    else:
        best_ave_i, wickets_for_best_ave_i, fivefers_for_best_ave = best_bowling_ave_streak_inns(l, all_innings)
        print(
            f"{player.player_name} has a lowest average of {best_ave_i} over {l} innings. He took {wickets_for_best_ave_i} wickets in this period, including {fivefers_for_best_ave} 5 wicket hauls.")
    m = int(
        input("\nEnter a value for n to see their lowest bowling average for a streak of 'n' matches, or 0 to skip."))
    if m == 0:
        print("")
    else:
        best_ave_m, wickets_for_best_ave_m = best_bowling_ave_streak_match(m, matches)
        print(
            f"{player.player_name} has a lowest average of {best_ave_m} over {m} matches. He took {wickets_for_best_ave_m} wickets in this period.")
    k=int(input("\nEnter a value for n to see their best streak of 5 wicket hauls in 'n' innings, or 0 to skip."))
    if k==0:
        print("")
    else:
        max_fivefers,  wickets_in_max_fivefers, ave_in_max_fivefers_ = best_fivefer_streak(k, all_innings)
        print(f"{player.player_name} has a best streak of {max_fivefers} 5 wicket hauls in {k} innings. He took {wickets_in_max_fivefers} wickets in this period, averaging {ave_in_max_fivefers_}.")

