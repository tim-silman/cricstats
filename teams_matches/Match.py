from datetime import datetime
class Match:
    def __init__(self, match_ID, home, away, date, ground, winner, margin):
        self.matchID=match_ID
        self.home=home
        self.away=away
        self.date=date
        self.ground=ground
        self.winner=winner
        self.margin=margin

    def __repr__(self):
        return f"{self.home} vs {self.away} at {self.ground} ("+datetime.strftime(self.date, "%b %Y")+")"


