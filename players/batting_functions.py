from get_player_and_innings import find_player
from get_player_and_innings import get_batting_innings_table


def best_innings_streak (n, all_innings):
    career=len(all_innings)
    if n>career:
        return None
    else:
        max=0
        tons_in_best_streak=0
        ave_in_best_streak=0
        for i in range(career-n):
            df=all_innings.iloc[i:i+n]
            tot=df.Runs.sum()
            if tot>max:
                max=tot
                tons_in_best_streak=len(df[df.Runs>=100])
                ave_in_best_streak = round(df.Runs.sum() / (df.Runs.count() - df["Not out"].sum()),2)
    return max, tons_in_best_streak, ave_in_best_streak

def best_century_streak (n, all_innings):
    career=len(all_innings)
    if n>career:
        return None

    else:
        max=0
        runs_in_best_streak=0
        ave_in_best_streak=0
        for i in range(career-n):
            df=all_innings.iloc[i:i+n]
            tot=len(df[df.Runs>=100])
            if tot>=max:
                max=tot
                if df.Runs.sum()>runs_in_best_streak:
                    runs_in_best_streak=df.Runs.sum()
                    ave_in_best_streak=round(df.Runs.sum()/(df.Runs.count()-df["Not out"].sum()),2)
    return max,  runs_in_best_streak, ave_in_best_streak

def best_ave_streak (n,all_innings):
    career = len(all_innings)
    if n > career:
        return None

    else:
        best = 0
        runs_in_best_streak = 0
        tons_in_best_streak=0
        for i in range(career - n):
            df = all_innings.iloc[i:i + n]
            ave=df.Runs.sum()/(df.Runs.count()-df["Not out"].sum())
            if ave> best:
                best = round(ave,2)
                runs_in_best_streak = df.Runs.sum()
                tons_in_best_streak=len(df[df.Runs>=100])
    return best, runs_in_best_streak, tons_in_best_streak

def batting_summary(all_innings):
    no_innings=len(all_innings)
    average=round(all_innings.Runs.sum()/(all_innings.Runs.count()-all_innings["Not out"].sum()),2)
    highest=all_innings.Runs.max()
    median=all_innings.Runs.median()
    centuries=len(all_innings[all_innings.Runs>=100])
    doubles=len(all_innings[all_innings.Runs>=200])
    summary_string=f"\tInnings batted: {no_innings}\n\tAverage: {average}\n\tMedian score: {median}\n\tHighest score: {highest}\n\tHundreds: {centuries}\n\tDouble hundreds: {doubles}"
    return summary_string

def main():
    search_term=input("Enter a player name")
    player=find_player(search_term)
    all_innings=get_batting_innings_table(player)
    print("\nBatting stats for "+player.player_name+":")
    print(batting_summary(all_innings))
    n=int(input("\nEnter a value for 'n' to see their best streak of runs scored in 'n' innings, or 0 to skip."))
    if n==0:
        print("")
    else:
        max_runs, cents_in_max_runs, ave_in_max_runs=best_innings_streak(n, all_innings)
        print(f"{player.player_name} has a best streak of {max_runs} runs in {n} innings. He made {cents_in_max_runs} hundreds in this period, averaging {ave_in_max_runs}.")
    k=int(input("\nEnter a value for n to see their best streak of hundreds scored in 'n' innings, or 0 to skip."))
    if k==0:
        print("")
    else:
        max_cents,  runs_in_max_cents, ave_in_max_cents = best_century_streak(k, all_innings)
        print(f"{player.player_name} has a best streak of {max_cents} hundreds in {k} innings. He made {runs_in_max_cents} runs in this period, averaging {ave_in_max_cents}.")
    l=int(input("\nEnter a value for n to see their highest average for a streak of 'n' innings, or 0 to skip."))
    if l==0:
        print("")
    else:
        best_ave,  runs_for_best_ave, cents_for_best_ave = best_ave_streak(l, all_innings)
        print(f"{player.player_name} has a maximum average of {best_ave} over {l} innings. He made {runs_for_best_ave} runs and scored {cents_for_best_ave} hundreds in this period.")

main()