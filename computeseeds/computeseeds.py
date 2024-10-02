import os

#capture all team file names
team_files = []
for filename in os.listdir('../fetchteamdata/teamdata'):
    if filename.endswith(".csv"):
        team_files.append(filename)
        continue
    else:
        continue

#instantiate lists
dates = []
standings = []

#populate dates
for day in range(28,32):
    date = 'Mar '+str(day)
    dates.append(date)
for day in range(1,31):
    date = 'Apr '+str(day)
    dates.append(date)
for day in range(1,32):
    date = 'May '+str(day)
    dates.append(date)
for day in range(1,31):
    date = 'Jun '+str(day)
    dates.append(date)
for day in range(1,32):
    date = 'Jul '+str(day)
    dates.append(date)
for day in range(1,32):
    date = 'Aug '+str(day)
    dates.append(date)
for day in range(1,31):
    date = 'Sep '+str(day)
    dates.append(date)

def get_date_value(date):
    result = date.replace('Mar ', '2').replace('Apr ','3').replace('May ','4') \
                 .replace('Jun ','5').replace('Jul ','6').replace('Aug ','7') \
                 .replace('Sep ','8')
    result = result[0]+'0'+result[1] if len(result) < 3 else result
    result = int(result)
    return result

def get_select_winpct_on_date(team, date, opps):
    dateVal = get_date_value(date)
    location = '../fetchteamdata/teamdata/'+team+'.csv'
    selectrecord = [0,0]
    with open(location, 'r') as doc:
        first_line = True
        for line in doc:
            #skip header line
            if first_line:
                first_line = False
                continue

            #check date is not past input date
            curDate = ' '.join(line.split(',')[1].replace(' (1)','').replace(' (2)','').split(' ')[1:])
            curDateVal = get_date_value(curDate)
            if curDateVal > dateVal:
                break

            #update intradivision matchup record if applicable
            opp = line.split(',')[5]
            if opp in opps:
                result = line.split(',')[6][0]
                if result == 'W' or result == 'W-wo':
                    selectrecord[0] += 1
                else:
                    selectrecord[1] += 1

    #update win percentage for current team
    wins = float(selectrecord[0])
    total = wins + float(selectrecord[1])
    try:
        return wins / total
    except:
        return -1

def get_winpct_on_date(team, date):
    result = []
    team_name = team.replace('.csv','')
    location = '../fetchteamdata/teamdata/'+team
    with open(location, 'r') as doc:
        closest_date = 0
        closest_winpct = -1
        first_line = True
        for line in doc:
            #find win % on correct date
            if first_line:
                first_line = False
                continue

            try:
                curDate = ' '.join(line.split(',')[1].replace(' (1)','').replace(' (2)','').split(' ')[1:])
                curWs = int(line.split(',')[10].split('-')[0])
                curLs = int(line.split(',')[10].split('-')[1])
                curWinPct = float(curWs) / float(curWs + curLs)
                if get_date_value(curDate) > get_date_value(date):
                    return [team_name, closest_winpct]
                else:
                    closest_date = curDate
                    closest_winpct = curWinPct
            except:
                continue
        return [team_name, closest_winpct]

#populate standings by date
for date in dates:
    result = {}
    #find win % of each team
    for team in team_files:
        resArr = get_winpct_on_date(team, date)
        result[resArr[0]] = resArr[1]
    standings.append(result)

#define divisions
al = [['rays','yankees','bluejays','orioles','redsox'],
      ['twins','whitesox','guardians','royals','tigers'],
      ['athletics','astros','mariners','angels','rangers']]
nl = [['braves','marlins','phillies','mets','nationals'],
      ['cubs','cardinals','reds','brewers','pirates'],
      ['dodgers','padres','giants','rockies','diamondbacks']]
teams = [al] + [nl]
teamabbreviations = {
    'diamondbacks':'ARI',
    'braves':'ATL',
    'orioles':'BAL',
    'redsox':'BOS',
    'cubs':'CHC',
    'whitesox':'CHW',
    'reds':'CIN',
    'guardians':'CLE',
    'rockies':'COL',
    'tigers':'DET',
    'astros':'HOU',
    'royals':'KCR',
    'angels':'LAA',
    'dodgers':'LAD',
    'marlins':'MIA',
    'brewers':'MIL',
    'twins':'MIN',
    'mets':'NYM',
    'yankees':'NYY',
    'athletics':'OAK',
    'phillies':'PHI',
    'pirates':'PIT',
    'padres':'SDP',
    'giants':'SFG',
    'mariners':'SEA',
    'cardinals':'STL',
    'rays':'TBR',
    'rangers':'TEX',
    'bluejays':'TOR',
    'nationals':'WSN'
}
filetext = ['', '']
longfiletext = ['', '']

def get_divopps_abr(team):
    divopps = []
    #for each league
    for l in range(2):
        #for each division
        for d in range(3):
            #if team is in division
            if team in teams[l][d]:
                #for each team in same division
                for t in teams[l][d]:
                    #if not same team
                    if not t==team:
                        divopps.append(teamabbreviations[t])
                break

    return divopps

def get_interdivopps_abr(team):
    interdivopps = []
    alflat = [ t for division in al for t in division ]
    nlflat = [ t for division in nl for t in division ]
    if team in alflat:
        for div in al:
            if not team in div:
                for t in div:
                    interdivopps.append(teamabbreviations[t])
    else:
        for div in nl:
            if not team in div:
                for t in div:
                    interdivopps.append(teamabbreviations[t])
    return interdivopps

def get_leagueopps_abr(team):
    leagueopps = []
    #for each league
    for league in teams:
        #flatten team names
        leagueteams = [ t for division in league for t in division ]
        if team in leagueteams:
            for leagueteam in leagueteams:
                if not team==leagueteam:
                    leagueopps.append(teamabbreviations[leagueteam])
    
    return leagueopps

def matchup_by_last_n(date, team1, team2, gamelimit):
    tempteams = [team1, team2]
    winpct = [-1, -1]
    dateVal = get_date_value(date)
    for i in range(2):
        location = '../fetchteamdata/teamdata/'+tempteams[i]+'.csv'
        divopps = get_divopps_abr(tempteams[i])
        divhistory = []
        with open(location, 'r') as doc:
            first_line = True
            for line in doc:
                #skip header line
                if first_line:
                    first_line = False
                    continue

                #check date is not past input date
                curDate = ' '.join(line.split(',')[1].replace(' (1)','').replace(' (2)','').split(' ')[1:])
                curDateVal = get_date_value(curDate)
                if curDateVal > dateVal:
                    break

                #update intradivision matchup record if applicable
                opp = line.split(',')[5]
                if opp in divopps:
                    result = line.split(',')[6][0]
                    if result == 'W':
                        divhistory.append([1,0])
                    else:
                        divhistory.append([0,1])

        #update winpct for current team
        wins = sum([entry[0] for entry in divhistory[-gamelimit:]])
        losses = sum([entry[1] for entry in divhistory[-gamelimit:]])
        try:
            winpct[i] = float(wins) / float(wins + losses)
        except:
            winpct[i] = -1

    #return team with better latest intradivision record
    if winpct[0] < winpct[1]:
        return team2
    elif winpct[0] == winpct[1]:
        if gamelimit < 25:
            return matchup_by_last_n(date, team1, team2, gamelimit+1)
        else:
            return team2
    else:
        return team1

def matchup_by_interdiv_record(date, team1, team2):
    winpct = [-1, -1]
    winpct[0] = get_select_winpct_on_date(team1, date, get_interdivopps_abr(team1))
    winpct[1] = get_select_winpct_on_date(team2, date, get_interdivopps_abr(team2))

    # return team with better interdivision (but intraleague) win percentage
    if winpct[0] < winpct[1]:
        print("Scoring as " + team2 + " then " + team1)
        return team2
    elif winpct[0] == winpct[1]:
        print("No team with better interdivision. Continuing to last half of intraleague games.")
        print("Nevermind, we're bailing. Unbroken 2-way tie. Scoring as " + team1 + " then " + team2)
        return team1
    else:
        print("Scoring as " + team1 + " then " + team2)
        return team1

def matchup_by_div_record(date, team1, team2):
    winpct = [-1, -1]
    winpct[0] = get_select_winpct_on_date(team1, date, get_divopps_abr(team1))
    winpct[1] = get_select_winpct_on_date(team2, date, get_divopps_abr(team2))

    #return team with better intradivision win percentage
    if winpct[0] < winpct[1]:
        print("Scoring as " + team2 + " then " + team1)
        return team2
    elif winpct[0] == winpct[1]:
        print("No team with better intradivision. Continuing to interdivision record.")
        return matchup_by_interdiv_record(date, team1, team2)
    else:
        print("Scoring as " + team1 + " then " + team2)
        return team1

def matchup(date, team1, team2):
    print("Evaluating 2-way tie between " + team1 + " and " + team2 + " on " + date)
    record = [0,0]
    dateVal = get_date_value(date)
    location = '../fetchteamdata/teamdata/'+team1+'.csv'
    with open(location, 'r') as doc:
        first_line = True
        for line in doc:
            #skip header line
            if first_line:
                first_line = False
                continue
            
            #check date is not past input date
            curDate = ' '.join(line.split(',')[1].replace(' (1)','').replace(' (2)','').split(' ')[1:])
            curDateVal = get_date_value(curDate)
            if curDateVal > dateVal:
                break

            #update matchup record if applicable
            opp = line.split(',')[5]
            if teamabbreviations[team2] == opp:
                result = line.split(',')[6][0]
                if result == 'W' or result == 'W-wo':
                    record[0] += 1
                else:
                    record[1] += 1

    #return team with better head-to-head record
    if record[0] < record[1]: 
        print("Scoring as " + team2 + " then " + team1)
        return team2
    elif record[0] == record[1]:
        print("No better head-to-head record found. Continuing to intradivision record.")
        return matchup_by_div_record(date, team1, team2)
    else:
        print("Scoring as " + team1 + " then " + team2)
        return team1

def matchup_3way(date, team1, team2, team3):
    # find record against each other club
    print("Evaluating 3-way tie between " + team1 + ", " + team2 + ", and " + team3 + " on " + date)
    records = [ \
    { "teamName": team1, "teamAbbr": teamabbreviations[team1], \
    teamabbreviations[team2]: { "wins": 0, "losses": 0, "winpct": -1 }, \
    teamabbreviations[team3]: { "wins": 0, "losses": 0, "winpct": -1 } }, \
    { "teamName": team2, "teamAbbr": teamabbreviations[team2], \
    teamabbreviations[team1]: { "wins": 0, "losses": 0, "winpct": -1 }, \
    teamabbreviations[team3]: { "wins": 0, "losses": 0, "winpct": -1 } }, \
    { "teamName": team3, "teamAbbr": teamabbreviations[team3], \
    teamabbreviations[team1]: { "wins": 0, "losses": 0, "winpct": -1 }, \
    teamabbreviations[team2]: { "wins": 0, "losses": 0, "winpct": -1 } }]

    #calculate individual head-to-head
    dateVal = get_date_value(date)
    tiedopps = [teamabbreviations[team1],teamabbreviations[team2],teamabbreviations[team3]]
    for teamIndex in range(3):
        location = '../fetchteamdata/teamdata/'+records[teamIndex]["teamName"]+'.csv'
        with open(location, 'r') as doc:
            first_line = True
            for line in doc:
                #skip header line
                if first_line:
                    first_line = False
                    continue
                
                #check date is not past input date
                curDate = ' '.join(line.split(',')[1].replace(' (1)','').replace(' (2)','').split(' ')[1:])
                curDateVal = get_date_value(curDate)
                if curDateVal > dateVal:
                    break

                #update matchup record if applicable
                opp = line.split(',')[5]
                if opp in records[teamIndex]:
                    result = line.split(',')[6][0]
                    if result == 'W' or result == 'W-wo':
                        records[teamIndex][opp]["wins"] += 1
                    else:
                        records[teamIndex][opp]["losses"] += 1
        #calc win pct
        oppAbbreviations = list(records[teamIndex].keys())[2:4]
        for opp in oppAbbreviations:
            wins = float(records[teamIndex][opp]["wins"])
            losses = float(records[teamIndex][opp]["losses"])
            try:
                records[teamIndex][opp]["winpct"] = wins / (wins + losses)
            except:
                records[teamIndex][opp]["winpct"] = -1

    #individual head-to-head (Rule III.a)
    if list(records[0].values())[2]["winpct"] > 0.5 and list(records[0].values())[3]["winpct"] > 0.5:
        # 1 wins, 2v3 matchup
        winner2v3 = matchup(date, team2, team3)
        loser2v3 = team2 if winner2v3 == team3 else team3
        print("Scored as " + team1 + ", " + winner2v3 + ", then " + loser2v3)
        return [team1, winner2v3, loser2v3]
    elif list(records[1].values())[2]["winpct"] > 0.5 and list(records[1].values())[3]["winpct"] > 0.5:
        # 2 wins, 1v3 matchup
        winner1v3 = matchup(date, team1, team3)
        loser1v3 = team1 if winner1v3 == team3 else team3
        print("Scored as " + team2 + ", " + winner1v3 + ", then " + loser1v3)
        return [team2, winner1v3, loser1v3]
    elif list(records[2].values())[2]["winpct"] > 0.5 and list(records[2].values())[3]["winpct"] > 0.5:
        # 3 wins, 1v2 matchup
        winner1v2 = matchup(date, team1, team2)
        loser1v2 = team1 if winner1v2 == team2 else team2
        print("Scored as " + team3 + ", " + winner1v2 + ", then " + loser1v2)
        return [team3, winner1v2, loser1v2]
    else:
        print("No team had a better individual head-to-head against the other 2 teams. Continuing to combined head-to-head.")

    #calculate combined head-to-head winpct
    for team in records:
        totalH2HWins = float(list(team.values())[2]["wins"]) + float(list(team.values())[3]["wins"])
        totalH2HLosses = float(list(team.values())[2]["losses"]) + float(list(team.values())[3]["losses"])
        try:
            team["h2hwinpct"] = totalH2HWins / (totalH2HWins + totalH2HLosses)
        except:
            team["h2hwinpct"] = -1
    
    #combined head-to-head (Rule III.b.1)
    if records[0]["h2hwinpct"] > records[1]["h2hwinpct"] and records[0]["h2hwinpct"] > records[2]["h2hwinpct"]:
        # 1 wins, 2v3 matchup
        winner2v3 = matchup(date, team2, team3)
        loser2v3 = team2 if winner2v3 == team3 else team3
        print("Scored as " + team1 + ", " + winner2v3 + ", then " + loser2v3)
        return [team1, winner2v3, loser2v3]
    elif records[1]["h2hwinpct"] > records[0]["h2hwinpct"] and records[1]["h2hwinpct"] > records[2]["h2hwinpct"]:
        # 2 wins, 1v3 matchup
        winner1v3 = matchup(date, team1, team3)
        loser1v3 = team1 if winner1v3 == team3 else team3
        print("Scored as " + team2 + ", " + winner1v3 + ", then " + loser1v3)
        return [team2, winner1v3, loser1v3]
    elif records[2]["h2hwinpct"] > records[0]["h2hwinpct"] and records[2]["h2hwinpct"] > records[1]["h2hwinpct"]:
        # 3 wins, 1v2 matchup
        winner1v2 = matchup(date, team1, team2)
        loser1v2 = team1 if winner1v2 == team2 else team2
        print("Scored as " + team3 + ", " + winner1v2 + ", then " + loser1v2)
        return [team3, winner1v2, loser1v2]
    elif records[0]["h2hwinpct"] == records[1]["h2hwinpct"] and records[0]["h2hwinpct"] > records[2]["h2hwinpct"]:
        # 1v2 matchup, 3 loses
        winner1v2 = matchup(date, team1, team2)
        loser1v2 = team1 if winner1v2 == team2 else team2
        print("Scored as " + winner1v2 + ", " + loser1v2 + ", then " + team3)
        return [winner1v2, loser1v2, team3]
    elif records[0]["h2hwinpct"] == records[2]["h2hwinpct"] and records[0]["h2hwinpct"] > records[1]["h2hwinpct"]:
        # 1v3 matchup, 2 loses
        winner1v3 = matchup(date, team1, team3)
        loser1v3 = team1 if winner1v3 == team3 else team3
        print("Scored as " + winner1v3 + ", " + loser1v3 + ", then " + team2)
        return [winner1v3, loser1v3, team2]
    elif records[1]["h2hwinpct"] == records[2]["h2hwinpct"] and records[1]["h2hwinpct"] > records[0]["h2hwinpct"]:
        # 2v3 matchup, 1 loses
        winner2v3 = matchup(date, team2, team3)
        loser2v3 = team2 if winner2v3 == team3 else team3
        print("Scored as " + winner2v3 + ", " + loser2v3 + ", then " + team1)
        return [winner2v3, loser2v3, team1]
    else:
        print("No team had a best combined head-to-head against the other 2 teams. Continuing to combined intradivision.")
    
    #calculate combined intradivision winpct
    for team in records:
        opps = get_divopps_abr(team["teamName"])
        team["divwinpct"] = get_select_winpct_on_date(team["teamName"], date, opps)

    #combined intradivision
    for teamIndex in range(len(records)):
        oppIndex1 = (teamIndex + 1) % 3
        oppIndex2 = (teamIndex + 2) % 3
        teamName = records[teamIndex]["teamName"]
        oppName1 = records[oppIndex1]["teamName"]
        oppName2 = records[oppIndex2]["teamName"]
        if records[teamIndex]["divwinpct"] > records[oppIndex1]["divwinpct"] and records[teamIndex]["divwinpct"] > records[oppIndex2]["divwinpct"]:
            # A wins, BvC matchup
            winner = matchup(date, oppName1, oppName2)
            loser = oppName1 if winner == oppName2 else oppName2
            print("Scored as " + teamName + ", " + winner + ", then " + loser)
            return [teamName, winner, loser]
    print("No team had a best intradivision record compared to the other 2 teams. Continuing to combined intraleague.")

    #calculate combined intraleague winpct
    for team in records:
        opps = get_leagueopps_abr(team["teamName"])
        team["leaguewinpct"] = get_select_winpct_on_date(team["teamName"], date, opps)

    #combined intraleague
    for teamIndex in range(len(records)):
        oppIndex1 = (teamIndex + 1) % 3
        oppIndex2 = (teamIndex + 2) % 3
        teamName = records[teamIndex]["teamName"]
        oppName1 = records[oppIndex1]["teamName"]
        oppName2 = records[oppIndex2]["teamName"]
        if records[teamIndex]["leaguewinpct"] > records[oppIndex1]["leaguewinpct"] and records[teamIndex]["leaguewinpct"] > records[oppIndex2]["leaguewinpct"]:
            # A wins, BvC matchup
            winner = matchup(date, oppName1, oppName2)
            loser = oppName1 if winner == oppName2 else oppName2
            print("Scored as " + teamName + ", " + winner + ", then " + loser)
            return [teamName, winner, loser]
    print("No team had a best intraleague record compared to the other 2 teams. Continuing to last half of intraleague games.")
    print("Nevermind, we're bailing. Unbroken 3-way tie. Scoring as " + team1 + ", " + team2 + ", then " + team3)
    return [team1, team2, team3]

def matchup_4way(date, team1, team2, team3, team4):
    #idk
    pass

#get playoff seed from standings by date
for dateIndex in range(len(dates)):
    date = dates[dateIndex]
    stands = standings[dateIndex] #ex. [ ["phillies", 0.555], ["bluejays", 0.650], ... ]
    seeds = [[], []]
    longseeds = [[], []]

    for leagueIndex in range(2):
        
        #determine ranks within each division
        divisionleaders = []
        leaguewildcard = []
        for divisionIndex in range(3):
            divtoday = [[team, stands[team]] for team in teams[leagueIndex][divisionIndex]]
            divtoday.sort(key = lambda x: x[1], reverse=True)

            #resolve 3-way ties for 1st place
            if divtoday[0][1] == divtoday[1][1] and divtoday[0][1] == divtoday[2][1]:
                result = matchup_3way(date, divtoday[0][0], divtoday[1][0], divtoday[2][0])
                top3 = {}
                for i in range(3):
                    top3[divtoday[i][0]] = divtoday[i][1]
                result = [[team_name, top3[team_name]] for team_name in result]
                for i in range(3):
                    divtoday[i] = result[i]
            #resolve 2-way ties for 1st place
            elif divtoday[0][1] == divtoday[1][1]:
                winner = matchup(date, divtoday[0][0], divtoday[1][0])
                if winner == divtoday[1][0]:
                    [divtoday[0], divtoday[1]] = [divtoday[1], divtoday[0]]

            #save this division leader and runner up to list with the rest
            divisionleaders.append(divtoday[0])
            leaguewildcard += divtoday[1:]

        #determine seeds 1-3 of league
        divisionleaders.sort(key = lambda x: x[1], reverse=True)

        #resolve 3-way ties for 1st seed
        if divisionleaders[0][1] == divisionleaders[1][1] and divisionleaders[0][1] == divisionleaders[2][1]:
            result = matchup_3way(date, divisionleaders[0][0], divisionleaders[1][0], divisionleaders[2][0])
            top3 = {}
            for i in range(3):
                top3[divisionleaders[i][0]] = divisionleaders[i][1]
            result = [[team_name, top3[team_name]] for team_name in result]
            for i in range(3):
                divisionleaders[i] = result[i]
        #resolve 2-way ties for 1st seed
        elif divisionleaders[0][1] == divisionleaders[1][1]:
            winner = matchup(date, divisionleaders[0][0], divisionleaders[1][0])
            if winner == divisionleaders[1][0]:
                [divisionleaders[0], divisionleaders[1]] = [divisionleaders[1], divisionleaders[0]]

        #resolve ties for 2nd seed (only 3 divleaders, so cannot be 3-way tie for 2nd)
        if divisionleaders[1][1] == divisionleaders[2][1]:
            winner = matchup(date, divisionleaders[1][0], divisionleaders[2][0])
            if winner == divisionleaders[2][0]:
                [divisionleaders[1], divisionleaders[2]] = [divisionleaders[2], divisionleaders[1]]

        #SEEDS 1-3 COMPLETE

        #determine 3 wild card + 2 next-out of league
        leaguewildcard.sort(key = lambda x: x[1], reverse=True)

        #resolve 3-way ties for 4th seed
        if leaguewildcard[0][1] == leaguewildcard[1][1] and leaguewildcard[0][1] == leaguewildcard[2][1]:
            result = matchup_3way(date, leaguewildcard[0][0], leaguewildcard[1][0], leaguewildcard[2][0])
            top3 = {}
            for i in range(3):
                top3[leaguewildcard[i][0]] = leaguewildcard[i][1]
            result = [[team_name, top3[team_name]] for team_name in result]
            for i in range(3):
                leaguewildcard[i] = result[i]
        #resolve 2-way ties for 4th seed
        elif leaguewildcard[0][1] == leaguewildcard[1][1]:
            winner = matchup(date, leaguewildcard[0][0], leaguewildcard[1][0])
            if winner == leaguewildcard[1][0]:
                [leaguewildcard[0], leaguewildcard[1]] = [leaguewildcard[1], leaguewildcard[0]]

        #resolve 3-way ties for 5th seed
        if leaguewildcard[1][1] == leaguewildcard[2][1] and leaguewildcard[1][1] == leaguewildcard[3][1]:
            result = matchup_3way(date, leaguewildcard[1][0], leaguewildcard[2][0], leaguewildcard[3][0])
            top3 = {}
            for i in range(1,4):
                top3[leaguewildcard[i][0]] = leaguewildcard[i][1]
            result = [[team_name, top3[team_name]] for team_name in result]
            for i in range(1,4):
                leaguewildcard[i] = result[i-1]
        #resolve 2-way ties for 5th seed
        elif leaguewildcard[1][1] == leaguewildcard[2][1]:
            winner = matchup(date, leaguewildcard[1][0], leaguewildcard[2][0])
            if winner == leaguewildcard[2][0]:
                [leaguewildcard[1], leaguewildcard[2]] = [leaguewildcard[2], leaguewildcard[1]]
        
        #resolve 3-way ties for 6th seed
        if leaguewildcard[2][1] == leaguewildcard[3][1] and leaguewildcard[2][1] == leaguewildcard[4][1]:
            result = matchup_3way(date, leaguewildcard[2][0], leaguewildcard[3][0], leaguewildcard[4][0])
            top3 = {}
            for i in range(2,5):
                top3[leaguewildcard[i][0]] = leaguewildcard[i][1]
            result = [[team_name, top3[team_name]] for team_name in result]
            for i in range(2,5):
                leaguewildcard[i] = result[i-2]
        #resolve 2-way ties for 6th seed
        elif leaguewildcard[2][1] == leaguewildcard[3][1]:
            winner = matchup(date, leaguewildcard[2][0], leaguewildcard[3][0])
            if winner == leaguewildcard[3][0]:
                [leaguewildcard[2], leaguewildcard[3]] = [leaguewildcard[3], leaguewildcard[2]]

        
        #resolve 3-way ties for 7th seed
        if leaguewildcard[3][1] == leaguewildcard[4][1] and leaguewildcard[3][1] == leaguewildcard[5][1]:
            result = matchup_3way(date, leaguewildcard[3][0], leaguewildcard[4][0], leaguewildcard[5][0])
            top3 = {}
            for i in range(3,6):
                top3[leaguewildcard[i][0]] = leaguewildcard[i][1]
            result = [[team_name, top3[team_name]] for team_name in result]
            for i in range(3,6):
                leaguewildcard[i] = result[i-3]
        #resolve 2-way ties for 7th seed
        elif leaguewildcard[3][1] == leaguewildcard[4][1]:
            winner = matchup(date, leaguewildcard[3][0], leaguewildcard[4][0])
            if winner == leaguewildcard[4][0]:
                [leaguewildcard[3], leaguewildcard[4]] = [leaguewildcard[4], leaguewildcard[3]]    
        
        #add seeds to combined list
        seeds[leagueIndex] = divisionleaders + leaguewildcard
        #append final seeds to league
        longseeds[leagueIndex] = seeds[leagueIndex]

        #save seeds to filetext
        seedtext = date
        for seed in seeds[leagueIndex]:
            name = seed[0]
            winpct = seed[1]
            seedtext += ',' + name + ',' + str(winpct)
        seedtext += '\n'
        filetext[leagueIndex] += seedtext

        #save seeds to longfiletext
        seedtext = date
        for seed in longseeds[leagueIndex]:
            name = seed[0]
            winpct = seed[1]
            seedtext += ',' + name + ',' + str(winpct)
        seedtext += '\n'
        longfiletext[leagueIndex] += seedtext

#save collected seed data to file
with open('alseeddata.csv', 'w+') as doc:
    doc.write(filetext[0])
with open('nlseeddata.csv', 'w+') as doc:
    doc.write(filetext[1])

#save long seed data to file
with open('allongseeddata.csv', 'w+') as doc:
    doc.write(longfiletext[0])
with open('nllongseeddata.csv', 'w+') as doc:
    doc.write(longfiletext[1])

print("complete")
