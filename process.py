import os
import sys
import json

# config
ignore_institution = False
ignore_zero_solve = True
# Urumqi (2017) is ignored due to contest time adjustment and many teams had quited or changed team member
ignore_contest = ["Urumqi"]
max_contest = 3
# ~config

team_count = {}
year = sys.argv[1]
for fn in os.listdir(year):
    if 'json' not in fn: continue
    for con in ignore_contest:
        if con in fn:
            break
    else:
        with open(os.path.join(year, fn), "rb") as f:
            data = json.loads(f.read())
            for team in data:
                if team.get("problemsSolved", -1) == 0 and ignore_zero_solve:
                    continue
                team_id = ""
                if not ignore_institution:
                    team_id = team["institution"].strip() + "+" + team["team"].strip()
                else:
                    team_id = team["team"].strip()
                s = team_count.get(team_id, set())
                s.add('{},solve{}'.format(fn[:-5], team.get("problemsSolved", "unknown")))
                team_count[team_id] = s

print(*[(team, team_count[team]) for team in team_count if len(team_count[team]) >= max_contest], sep = '\n')