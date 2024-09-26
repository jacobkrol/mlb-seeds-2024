
for file in ['./allongseeddata.csv', './nllongseeddata.csv']:
    json = '['
    with open(file, 'r') as doc:
        for line in doc:
            date = line.split(",")[0]
            seeds = line.split(",")[1:]
            json += '{"date":"'+date+'","seeds":['
            for seed in range(15):
                team = seeds[seed*2]
                json += '"'+team+'",'
            json = json[:-1]
            json += "]},"
    json = json[:-1]
    json += ']'

    with open(file.replace('.csv','.json'), 'w') as doc:
        doc.write(json)

print("complete")
'''

teamsdict = {
    'diamondbacks':'ARI',
    'braves':'ATL',
    'orioles':'BTL',
    'redsox':'BOS',
    'cubs':'CHC',
    'whitesox':'CHW',
    'reds':'CIN',
    'indians':'CLE',
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
    'nationals':'WAS'
}


json = '['
teams = list(teamsdict.keys())
for i in range(len(teams)):
    json += '{"id":'+str(i+1)+',"src":"./src/images/'+teams[i]+'.png","title":"'+teams[i]+'"},'
json = json[:-1]
json += ']'
print(json)


text = ''
teams = list(teamsdict.keys())
for i in range(len(teams)):
    #text += 'import '+teams[i]+' from "./'+teams[i]+'.png";\n'
    text += '"'+teams[i]+'":'+teams[i]+',\n'
print(text)
'''
