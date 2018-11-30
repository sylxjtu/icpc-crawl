import os
import sys
import json

# config
ignore_institution = False
# Strict mode, only teams really participated (solved problems) will be shown
strict_mode = False
# Urumqi (2017) is ignored due to contest time adjustment and many teams had quited or changed team member
ignore_contest = ["Urumqi"]
max_contest = 3
# ~config

class TeamOfContest:
    def __init__(self, name, solved):
        self.name = name
        self.solved = solved

    def __eq__(self, rhs):
        return self.name == rhs.name

    def __hash__(self):
        return self.name.__hash__()

    def __str__(self):
        return self.name + ", solved " + str(self.solved)

    def __repr__(self):
        return self.__class__.__name__ + "(" + self.name + ", " + str(self.solved) + ")"


team_count = {}
year = sys.argv[1]
for fn in os.listdir(year):
    if 'json' not in fn: continue
    for con in ignore_contest:
        if con in fn:
            break
    else:
        with open(os.path.join(year, fn), "rb") as f:
            if 'standing' in fn:
                data = json.loads(f.read())
                for team in data:
                    if team.get("problemsSolved", -1) <= 0 and strict_mode:
                        continue
                    team_id = ""
                    if not ignore_institution:
                        team_id = team["institution"].strip() + "+" + team["team"].strip()
                    else:
                        team_id = team["team"].strip()
                    s = team_count.get(team_id, set())
                    s.add(TeamOfContest(fn.split('.')[0], team.get("problemsSolved", -1)))
                    team_count[team_id] = s
            elif 'teams' in fn:
                if strict_mode: continue
                data = json.loads(f.read())
                for team in data:
                    if team.get("status", "UNKNOWN") != "ACCEPTED":
                        continue
                    team_id = ""
                    if not ignore_institution:
                        team_id = team["institution"].strip() + "+" + team["name"].strip()
                    else:
                        team_id = team["name"].strip()
                    s = team_count.get(team_id, set())
                    if TeamOfContest(fn.split('.')[0], -1) in s: continue
                    s.add(TeamOfContest(fn.split('.')[0], -1))
                    team_count[team_id] = s

print(*[(team, team_count[team]) for team in team_count if len(team_count[team]) >= max_contest], sep = '\n')