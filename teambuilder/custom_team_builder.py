from poke_env.teambuilder import Teambuilder

class CustomTeamBuilder(Teambuilder):
    def __init__(self, team):
        self.team = self.join_team(self.parse_showdown_team(team))

    def yield_team(self):
        return self.team