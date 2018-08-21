import requests, json
 
# leagueId=9 is for worlds, change at will
urlTournament="http://api.lolesports.com/api/v1/scheduleItems?leagueId=9"
r  = requests.get(urlTournament)
data = json.loads(r.text)
 
tournamentId = data['highlanderTournaments'][2]["id"]
 
brackets = data['highlanderTournaments'][2]["brackets"]
 
matches = []
games = {}
 
#Get the list of matches and each of their games
for bracketId in brackets:
    print("Bracket : "+bracketId)
    bracket = brackets[bracketId]
   
    for matchId in bracket["matches"]:
       
        match = bracket["matches"][matchId]
        for gameId in match['games']:
           
            game = match['games'][gameId]
           
            if 'gameId' in game:
                matches.append(matchId)
                games[gameId] = {"matchHistoryId":game['gameId']}
               
#Call each match to get the game hash    
baseMatchUrl = "http://api.lolesports.com/api/v2/highlanderMatchDetails?tournamentId="+tournamentId+"&matchId="
for matchId in matches:
    r  = requests.get(baseMatchUrl + matchId)
    print('id', matchId)
    dataMatch = json.loads(r.text)
    for i in dataMatch["gameIdMappings"]:
        games[i["id"]]["hash"] = i["gameHash"]
       
#At last get the full game data
baseMatchHistoryUrl = "https://acs.leagueoflegends.com/v1/stats/game/TRLH1/"
 
for gameId in games:
    r  = requests.get(baseMatchHistoryUrl + games[gameId]["matchHistoryId"] + "?gameHash=" + games[gameId]["hash"])
    dataGame = json.loads(r.text)
   
    r  = requests.get(baseMatchHistoryUrl + games[gameId]["matchHistoryId"] + "/timeline?gameHash=" + games[gameId]["hash"])
    dataGame['timeline'] = json.loads(r.text)
   
    print(dataGame)
   
    break
