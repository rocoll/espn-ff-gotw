# SAC FF GAME OF THE WEEK
#   ___   __   _  _  ____     __  ____    ____  _  _  ____    _  _  ____  ____  __ _ 
#  / __) / _\ ( \/ )(  __)   /  \(  __)  (_  _)/ )( \(  __)  / )( \(  __)(  __)(  / )
# ( (_ \/    \/ \/ \ ) _)   (  O )) _)     )(  ) __ ( ) _)   \ /\ / ) _)  ) _)  )  ( 
#  \___/\_/\_/\_)(_/(____)   \__/(__)     (__) \_)(_/(____)  (_/\_)(____)(____)(__\_)
#
# ---------------------------------------------------------
#
# Determine the game of the week for most interest by 
# counting the number of fantasy team rostered players in 
# the league for each of this week's NFL games.
# 
# Relies on the https://github.com/cwendt94/espn-api project.
#

# ---------------------------
# Configuration

# Identify your fantasy league and year of play
LEAGUE_ID=123456789
LEAGUE_YEAR=2023

# If yours is a private fantasy league, then grab the 
# cookie values from your web browser after signing in 
# to your league and save them here:
COOKIE_ESPN_S2='_put_your_cookie_value_here_'
COOKIE_SWID='_put_your_cookie_value_here_'


# ---------------------------
# Get the week number as a command-line arg, default to "1"

import sys

try:
    WEEK = sys.argv[1]
except IndexError:
    WEEK = 1


# ---------------------------
# Query this league's information from the ESPN Fantasy Football API.

from espn_api.football import League

# declare empty list
proTeamsList = []

# Access to private leagues require browser cookies: espn_s2 and swid
league = League(league_id=LEAGUE_ID, year=LEAGUE_YEAR, espn_s2=COOKIE_ESPN_S2, swid=COOKIE_SWID)

# the list of fantasy teams in the league
lteams=league.teams

# for each fantasy team in the league
for t in lteams:

    # get the roster of players
    roster = t.roster

    # for each player on this roster
    for p in roster:

        # still abbreviating Raiders as in Oakland
        if p.proTeam == "OAK":

            # ensure we match the schedule's abbrev
            actualTeam="LV"

        else:

            actualTeam=p.proTeam

        # get the proTeam of this player
        proTeamsList.append(actualTeam)
        
# declare dictionary to count the occurence of each proTeam
proTeams_dict = {}

# Get a count of how many fantasy players are playing for each pro team
# for each proTeam in the list
for t in proTeamsList:
   
    if t in proTeams_dict:

        # already exists, increment
        proTeams_dict[t] += 1

    else:       

        # first one, init
        proTeams_dict[t] = 1

# At this point, we now have a dictionary array with index named by pro team (e.g., DAL, CAR, LV)
# storing counts of their players in our fantasy league


# ---------------------------
# Get this list of NFL games for this week and add up the fantasy players in each game

import subprocess

# Define your shell command as a list of strings
shell_command = [
    'bash', '-c',
    f'''
    #!/bin/bash
    curl -fsSL "https://cdn.espn.com/core/nfl/schedule?xhr=1&year=2023&week={WEEK}" | jq . - | grep "@" | grep "shortName" | awk -F'"' '{{ print $4 }}'
    '''
]
# Returns a list of games in format "AWY @ HOM"

# Run the script and capture results
process = subprocess.Popen(shell_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

# Decode the byte output to string and split it into lines
games = stdout.decode('utf-8').splitlines()

# Look at each team for each game
for g in games:
    gteams = g.split("@")
    awayteam = gteams[0].strip()

    # Match the AWY team to the dictionary array to get count of players
    try:
        players = proTeams_dict[awayteam]        # begin count
    except KeyError:
        players = 0        # no ff players on this pro team
        print(f"{0:02d}"+" FF league players on team: "+awayteam)
    
    hometeam = gteams[1].strip()

    # Match the HOM team to the dictionary array to get count of players
    try:
        players += proTeams_dict[hometeam]       # finish count
    except KeyError:
        players += 0        # no ff players on this pro team
        print(f"{0:02d}"+" FF league players on team: "+hometeam)

    # output this week's list of games and fantasy players for each
    print(f"{players:02d}"+" FF league players in wk "+WEEK+" game: "+awayteam+" @ "+hometeam)

    # results are returned unordered - use bash sort if desired.