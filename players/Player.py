import pandas as pd

class Player:
    def __init__(self, player_id, player_name):
        self.player_name=player_name
        self.player_id=player_id

    def __repr__(self):
        return f"{self.player_name} (ID: {self.player_id})"

    def get_innings(self):
        url = "https://stats.espncricinfo.com/ci/engine/player/" + str(
            self.player_id) + ".html?class=1;template=results;type=batting;view=innings"
        df = pd.read_html(url, match='Opposition')[0]
        df["Not out"] = df.Runs.apply(lambda x: 1 if "*" in x else 0)
        df.Runs = df.Runs.str.replace("*", "", regex=False)
        df = df[(df.Runs != "DNB") & (df.Runs != "TDNB") & (df.Runs != "absent") & (df.Runs != "sub")]
        df = df.drop(["Ground", "Unnamed: 13", "Unnamed: 9", "Dismissal", "Mins"], axis=1)
        df["Runs"] = df["Runs"].astype(int)
        # df[["Runs", "4s", "6s", "Pos", "Inns"]]=df[["Runs",  "4s", "6s", "Pos", "Inns"]].astype(int)
        # df["SR"]=df["SR"].astype(float)
        df = df.reset_index()
        return df