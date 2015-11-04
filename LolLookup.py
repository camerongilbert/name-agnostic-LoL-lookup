import json, time, requests

api_key = 'YOUR KEY HERE'

with open('players.json') as infile:
    MasterData = json.load(infile)
	
with open('playerIDs.json') as infile:
    playerIDs = json.load(infile)
	
def playerLookup(SumName,region='kr'):
    if SumName not in playerIDs.keys():
        sumparts = SumName.split(' ')
        SumSpaceless = ''
        for part in sumparts:
            SumSpaceless = SumSpaceless+part.lower()
        getIDreq = 'https://{}.api.pvp.net/api/lol/{}/v1.4/summoner/by-name/{}?api_key={}'.format(region,region,SumName,api_key)
        IDreq = requests.get(getIDreq)
        playerID = str(IDreq.json()[SumSpaceless]['id'])
        playerIDs[SumName] = playerID
        time.sleep(5)
    else:
        playerID = playerIDs[SumName]
    getLeagueReq = 'https://{}.api.pvp.net/api/lol/{}/v2.5/league/by-summoner/{}?api_key={}'.format(region,region,playerID,api_key)
    leagueReq = requests.get(getLeagueReq)
    time.sleep(5)
    soloQ = leagueReq.json()[playerID][0]
    playertier = soloQ['tier']
    CurrentName = SumName
    for thingy in soloQ['entries']:
        if thingy['playerOrTeamId']==playerID:
            SoloQData = thingy
    if playerID in MasterData.keys():
        currentAltNames = MasterData[playerID]['Alternate IDs']
    else:
        currentAltNames = ''
    if SoloQData['playerOrTeamName'] != SumName:
        CurrentName = SoloQData['playerOrTeamName']
        if playerID in MasterData.keys():
            currentAltNames = MasterData[playerID]['Alternate IDs']
            if SumName not in currentAltNames:
                currentAltNames = MasterData[playerID]['Alternate IDs']+SumName
    playerDiv = SoloQData['division']
    playerLP = SoloQData['leaguePoints']
    LastUpdated = str(datetime.date.today())
    playerData = {"Name":CurrentName, "Player ID":playerID, "Alternate IDs":currentAltNames,"Tier":playertier,"Division":playerDiv,"playerLP":playerLP, "Last Updated":LastUpdated}
    MasterData[playerID] = playerData
    return playerData

def LocalCheck(*args):
    for arg in args:
        if arg in MasterData:
            print(MasterData[arg])
        else:
            playID = playerIDs[arg]
            print(MasterData[playID])

def saveData():
    with open('players.json', 'wt') as outfile:
        json.dump(MasterData, outfile)
    with open('playerIDs.json','wt') as outfile:
        json.dump(playerIDs,outfile)

def batchQuery(region,*args):
    for arg in args:
        if type(arg)==list:
            for item in list:
                playerLookup(item,region)
        else:
            playerLookup(arg,region)
			
			
def massUpdate(region = 'kr'):
    for key in MasterData:
        playerID = key
        getLeagueReq = 'https://{}.api.pvp.net/api/lol/{}/v2.5/league/by-summoner/{}?api_key={}'.format(region,region,playerID,api_key)
        leagueReq = requests.get(getLeagueReq)
        time.sleep(5)
        soloQ = leagueReq.json()[playerID][0]
        playertier = soloQ['tier']
        SumName = MasterData[playerID]['Name']
        CurrentName = SumName
        for thingy in soloQ['entries']:
            if thingy['playerOrTeamId']==playerID:
                SoloQData = thingy
        currentAltNames = MasterData[playerID]['Alternate IDs']
        if SoloQData['playerOrTeamName'] != SumName:
            CurrentName = SoloQData['playerOrTeamName']
            if SumName not in currentAltNames:
                currentAltNames = MasterData[playerID]['Alternate IDs']+SumName
        playerDiv = SoloQData['division']
        playerLP = SoloQData['leaguePoints']
        LastUpdated = str(datetime.date.today())
        playerData = {"Name":CurrentName, "Player ID":playerID, "Alternate IDs":currentAltNames,"Tier":playertier,"Division":playerDiv,"playerLP":playerLP, "Last Updated":LastUpdated}
        MasterData[playerID] = playerData
    return MasterData