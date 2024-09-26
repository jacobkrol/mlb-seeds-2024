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
    date = 'Mar'+str(day)
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
for day in range(1,30):
    date = 'Sep '+str(day)
    dates.append(date)

def get_date_value(date):
    result = date.replace('Mar ', '2').replace('Apr ','3').replace('May ','4') \
                 .replace('Jun ','5').replace('Jul ','6').replace('Aug ','7') \
                 .replace('Sep ','8')
    result = result[0]+'0'+result[1] if len(result) < 3 else result
    result = int(result)
    return result

def get_div_winpct_on_date(team, date):
    dateVal = get_date_value(date)
    location = '../fetchteamdata/teamdata/'+team+'.csv'
    divopps = get_divopps_abr(team)
    divrecord = [0,0]
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
                    divrecord[0] = divrecord[0]+1
                else:
                    divrecord[1] = divrecord[1]+1

    #update win percentage for current team
    wins = float(divrecord[0])
    total = wins + float(divrecord[1])
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

def matchup_by_div_record(date, team1, team2):
    tempteams = [team1, team2]
    winpct = [-1, -1]
    winpct[0] = get_div_winpct_on_date(team1, date)
    winpct[1] = get_div_winpct_on_date(team2, date)

    #return team with better intradivision win percentage
    if winpct[0] < winpct[1]:
        return team2
    elif winpct[0] == winpct[1]:
        return matchup_by_last_n(date, team1, team2, 20)
    else:
        return team1

def matchup(date, team1, team2):
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
                if result == 'W':
                    record[0] = record[0]+1
                else:
                    record[1] = record[1]+1

    #return team with better head-to-head record
    if record[0] < record[1]: 
        return team2
    elif record[0] == record[1]:
        return matchup_by_div_record(date, team1, team2)
    else:
        return team1

def matchup_nondiv_3way(date, team1, team2, team3):
    results = [[team1, -1], [team2, -1], [team3, -1]]
    results[0][1] = get_div_winpct_on_date(team1, date)
    results[1][1] = get_div_winpct_on_date(team2, date)
    results[2][1] = get_div_winpct_on_date(team3, date)
    results.sort(key = lambda x: x[1], reverse=True)

    #return teams in order of intradivision records
    if results[0][1] == results[1][1] and results[0][1] == results[2][1]:
        print("unbroken 3-way tie outside division on",date)
        return [team1, team2, team3]
    elif results[0][1] == results[1][1]:
        winner = matchup(date, results[0][0], results[1][0])
        if winner == results[1][0]:
            [results[0], results[1]] = [results[1], results[0]]
    elif results[1][1] == results[2][1]:
        winner = matchup(date, results[1][0], results[2][0])
        if winner == results[2][0]:
            [results[1], results[2]] = [results[2], results[1]]

    return [results[0][0], results[1][0], results[2][0]]

def matchup_div_3way(date, team1, team2, team3):
    #find records of each team against the other two
    records = [[team1, [0,0]], [team2, [0,0]], [team3, [0,0]]]
    dateVal = get_date_value(date)
    tiedopps = [teamabbreviations[team1],teamabbreviations[team2],teamabbreviations[team3]]
    for t in range(3):
        location = '../fetchteamdata/teamdata/'+records[t][0]+'.csv'
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
                if opp in tiedopps:
                    result = line.split(',')[6][0]
                    if result == 'W':
                        records[t][1][0] = records[t][1][0]+1
                    else:
                        records[t][1][1] = records[t][1][1]+1

    #use records to calculate win percentage
    results = [[team1, -1], [team2, -1], [team3, -1]]
    for r in range(3):
        wins = float(records[r][1][0])
        losses = float(records[r][1][1])
        try:
            results[r][1] = wins / (wins+losses)
        except:
            results[r][1] = -1

    #return order of teams against each other
    if results[0][1] == results[1][1] and results[0][1] == results[2][1]:
        print("unbroken 3-way tie inside division on",date)
        return [team1, team2, team3]
    elif results[0][1] == results[1][1]:
        winner = matchup(date, results[0][0], results[1][0])
        if winner == results[1][0]:
            [results[0], results[1]] = [results[1], results[0]]
    elif results[1][1] == results[2][1]:
        winner = matchup(date, results[1][0], results[2][0])
        if winner == results[2][0]:
            [results[1], results[2]] = [results[2], results[1]]

    return [results[0][0], results[1][0], results[2][0]]

def matchup_3way(date, team1, team2, team3):
    for league in teams:
        for division in league:
            if team1 in division and team2 in division and team3 in division:
                return matchup_div_3way(date, team1, team2, team3)
    return matchup_nondiv_3way(date, team1, team2, team3)

#get playoff seed from standings by date
for i in range(len(dates)):
    date = dates[i]
    stands = standings[i]
    seeds = [[], []]
    longseeds = [[], []]

    for t in range(2):
        
        #determine 1 and 2 slot in each division of league
        divisionleaders = []
        divisionwildcard = []
        for i in range(3):
            divtoday = [[team, stands[team]] for team in teams[t][i]]
            divtoday.sort(key = lambda x: x[1], reverse=True)

            #resolve ties for 1st place
            if divtoday[0][1] == divtoday[1][1]:
                winner = matchup(date, divtoday[0][0], divtoday[1][0])
                if winner == divtoday[1][0]:
                    [divtoday[0], divtoday[1]] = [divtoday[1], divtoday[0]]

            #resolve ties for 2nd place
            # if divtoday[1][1] == divtoday[2][1]:
            #     winner = matchup(date, divtoday[1][0], divtoday[2][0])
            #     if winner == divtoday[2][0]:
            #         [divtoday[1], divtoday[2]] = [divtoday[2], divtoday[1]]

            #resolve 3-way ties for 1st place
            if divtoday[0][1] == divtoday[1][1] and divtoday[0][1] == divtoday[2][1]:
                result = matchup_div_3way(date, divtoday[0][0], divtoday[1][0], divtoday[2][0])
                top3 = {}
                for i in range(3):
                    top3[divtoday[i][0]] = divtoday[i][1]
                result = [[team_name, top3[team_name]] for team_name in result]
                for i in range(3):
                    divtoday[i] = result[i]
                
            #identify 3-way ties for 2nd place
            # if divtoday[1][1] == divtoday[2][1] and divtoday[1][1] == divtoday[3][1]:
            #     result = matchup_div_3way(date, divtoday[1][0], divtoday[2][0], divtoday[3][0])
            #     top3 = {}
            #     for i in range(3):
            #         top3[divtoday[i+1][0]] = divtoday[i+1][1]
            #     result = [[team_name, top3[team_name]] for team_name in result]
            #     for i in range(3):
            #         divtoday[i+1] = result[i]
                
            #save this division leader and runner up to list with the rest
            divisionleaders.append(divtoday[0])
            divisionwildcard += divtoday[1:]
        

        #determine seeds 1-3 of league
        divisionleaders.sort(key = lambda x: x[1], reverse=True)

        #resolve ties for 1st seed
        if divisionleaders[0][1] == divisionleaders[1][1]:
            winner = matchup(date, divisionleaders[0][0], divisionleaders[1][0])
            if winner == divisionleaders[1][0]:
                [divisionleaders[0], divisionleaders[1]] = [divisionleaders[1], divisionleaders[0]]

        #resolve ties for 2nd seed
        if divisionleaders[1][1] == divisionleaders[2][1]:
            winner = matchup(date, divisionleaders[1][0], divisionleaders[2][0])
            if winner == divisionleaders[2][0]:
                [divisionleaders[1], divisionleaders[2]] = [divisionleaders[2], divisionleaders[1]]

        #resolve 3-way ties for 1st seed
        if divisionleaders[0][1] == divisionleaders[1][1] and divisionleaders[0][1] == divisionleaders[2][1]:
            result = matchup_3way(date, divisionleaders[0][0], divisionleaders[1][0], divisionleaders[2][0])
            top3 = {}
            for i in range(3):
                top3[divisionleaders[i][0]] = divisionleaders[i][1]
            result = [[team_name, top3[team_name]] for team_name in result]
            for i in range(3):
                divisionleaders[i] = result[i]
        
        #determine 2 wild card + 2 next-out of league
        divisionwildcard.sort(key = lambda x: x[1], reverse=True)
        
        #resolve ties for 4th seed
        if divisionwildcard[0][1] == divisionwildcard[1][1]:
            winner = matchup(date, divisionwildcard[0][0], divisionwildcard[1][0])
            if winner == divisionwildcard[1][0]:
                [divisionwildcard[0], divisionwildcard[1]] = [divisionwildcard[1], divisionwildcard[0]]

        #resolve ties for 5th seed
        if divisionwildcard[1][1] == divisionwildcard[2][1]:
            winner = matchup(date, divisionwildcard[1][0], divisionwildcard[2][0])
            if winner == divisionwildcard[2][0]:
                [divisionwildcard[1], divisionwildcard[2]] = [divisionwildcard[2], divisionwildcard[1]]
        
        #resolve ties for 6th seed
        if divisionwildcard[2][1] == divisionwildcard[3][1]:
            winner = matchup(date, divisionwildcard[2][0], divisionwildcard[3][0])
            if winner == divisionwildcard[3][0]:
                [divisionwildcard[2], divisionwildcard[3]] = [divisionwildcard[3], divisionwildcard[2]]

        #resolve ties for 7th seed
        if divisionwildcard[3][1] == divisionwildcard[4][1]:
            winner = matchup(date, divisionwildcard[3][0], divisionwildcard[4][0])
            if winner == divisionwildcard[4][0]:
                [divisionwildcard[3], divisionwildcard[4]] = [divisionwildcard[4], divisionwildcard[3]]

        #resolve 3-way ties for 4th seed
        if divisionwildcard[0][1] == divisionwildcard[1][1] and divisionwildcard[0][1] == divisionwildcard[2][1]:
            result = matchup_3way(date, divisionwildcard[0][0], divisionwildcard[1][0], divisionwildcard[2][0])
            top3 = {}
            for i in range(3):
                top3[divisionwildcard[i][0]] = divisionwildcard[i][1]
            result = [[team_name, top3[team_name]] for team_name in result]
            for i in range(3):
                divisionwildcard[i] = result[i]
        
        #resolve 3-way ties for 5th seed
        if divisionwildcard[1][1] == divisionwildcard[2][1] and divisionwildcard[1][1] == divisionwildcard[3][1]:
            result = matchup_3way(date, divisionwildcard[1][0], divisionwildcard[2][0], divisionwildcard[3][0])
            top3 = {}
            for i in range(1,4):
                top3[divisionwildcard[i][0]] = divisionwildcard[i][1]
            result = [[team_name, top3[team_name]] for team_name in result]
            for i in range(1,4):
                divisionwildcard[i] = result[i-1]
        
        #resolve 3-way ties for 6th seed
        if divisionwildcard[2][1] == divisionwildcard[3][1] and divisionwildcard[2][1] == divisionwildcard[4][1]:
            result = matchup_3way(date, divisionwildcard[2][0], divisionwildcard[3][0], divisionwildcard[4][0])
            top3 = {}
            for i in range(2,5):
                top3[divisionwildcard[i][0]] = divisionwildcard[i][1]
            result = [[team_name, top3[team_name]] for team_name in result]
            for i in range(2,5):
                divisionwildcard[i] = result[i-2]
        
        #resolve 3-way ties for 7th seed
        if divisionwildcard[3][1] == divisionwildcard[4][1] and divisionwildcard[3][1] == divisionwildcard[5][1]:
            result = matchup_3way(date, divisionwildcard[3][0], divisionwildcard[4][0], divisionwildcard[5][0])
            top3 = {}
            for i in range(3,6):
                top3[divisionwildcard[i][0]] = divisionwildcard[i][1]
            result = [[team_name, top3[team_name]] for team_name in result]
            for i in range(3,6):
                divisionwildcard[i] = result[i-3]
        
        #add seeds to combined list
        seeds[t] = divisionleaders + divisionwildcard
        #append final seeds to league
        longseeds[t] = seeds[t]

        #save seeds to filetext
        seedtext = date
        for seed in seeds[t]:
            name = seed[0]
            winpct = seed[1]
            seedtext += ',' + name + ',' + str(winpct)
        seedtext += '\n'
        filetext[t] += seedtext

        #save seeds to longfiletext
        seedtext = date
        for seed in longseeds[t]:
            name = seed[0]
            winpct = seed[1]
            seedtext += ',' + name + ',' + str(winpct)
        seedtext += '\n'
        longfiletext[t] += seedtext

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
