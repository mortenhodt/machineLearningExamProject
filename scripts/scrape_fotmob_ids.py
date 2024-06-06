import requests
import csv
from tqdm import tqdm

league_ids = {"Premier League (ENG)": 47, 
              "Bundesliga (GER)": 54, 
              "Serie A (ITA)": 55, 
              "La Liga (SPA)": 87, 
              "Ligue 1 (FRA)": 53, 
              "Championship (ENG)": 48,
              "Eredivisie (HOL)": 57,
              "Liga Portugal (POR)": 61,
              "Belgian Pro League (BEL)": 40,
              "Brazilian Serie A (BRA)": 268,
              "Swiss Super League (SWI)": 69,
              "Turkish Süper Lig (TUR)": 71,
              "Russian Premier League (RUS)": 63,
              "Superligaen (DEN)": 46,
              "MLS (USA)": 130,
              "Austrian Bundesliga (AUS)": 38,
              "La Liga 2 (SPA)": 140,
              "Ekstraklasa (POL)": 196,
            #   "Primera División (ARG)": 112,
              "2. Bundesliga (GER)": 146,
              "HNL (CRO)": 252,
              "Liga MX (MEX)": 230,
              "Cypriot First Division (CYP)": 136,
              "Allsvenskan (SWE)": 67,
              "J1 League (JAP)": 223,
              "K-League 1 (KOR)": 9080,
              "Saudi Pro League (SAU)": 536,
              "Israeli Premier League (ISR)": 127,
              "Liga 1 (ROM)": 189,
              "Eliteserien (NOR)": 59,
              "Czech Liga (CZE)": 122,
              "Primera A (COL)": 274,
              "Division Profesional (PAR)": 199,
              "Primara A (ECU)": 246,
              "Serie B (BRA)": 8814,
              "Serie B (ITA)": 86,
              "Primera División (URU)": 161,
              "Segunda Liga (POR)": 185,
              "Ligue 2 (FRA)": 110,
              "Super Liga (SVK)": 176,
              "HB 1 (HUN)": 212,
              "Primera División (CHI)": 273,
              "3. Liga (GER)": 208,
              "League One (ENG)": 108,
              "League Two (ENG)": 109,
              "Super Liga (SRB)": 182,
              "Primera Division (CRI)": 121,
              "Premijer Liga (BOS)": 267,
              "First League (BUL)": 270,
              "A-League (AUS)": 113,

              }

# Function to fetch team ids from a league
def fetch_team_ids(league_id):
    try:
        response = requests.get(f'https://www.fotmob.com/api/leagues?id={league_id}')
        data = response.json()
        # Extract team IDs from the 'teamForm' dictionary keys
        team_ids = list(data["table"][0]["teamForm"].keys())
        return team_ids
    except Exception as e:
        print(f"Failed to fetch team IDs for league {league_id}: {e}")
        return []  # Return an empty list if there's an error

def fetch_player_details(team_id):
    try:
        response = requests.get(f'https://www.fotmob.com/api/teams?id={team_id}')
        data = response.json()
        # Extract player IDs from the 'teamForm' dictionary keys
        # players = data["squad"][4]["members"]
        midfielders = data["squad"][3]["members"]
        forwards = data["squad"][4]["members"]
        # print("TYPE: ", type(forwards))
        players = midfielders + forwards
        return [(player["id"], player["name"]) for player in players]
    except Exception as e:
        print(f"Failed to fetch player details for team {team_id}: {e}")
        return []  # Return an empty list if there's an error

filename = '../data/player_details.csv'

# Open file to write league ID, team ID, player ID, and player name
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['leagueId', 'teamId', 'playerId', 'playerName'])  # Column headers

    # Loop through each league and its teams
    for league_name, league_id in tqdm(league_ids.items(), desc='Leagues Progress', unit = 'league'):
        # try:
        team_ids = fetch_team_ids(league_id)
        for team_id in tqdm(team_ids, desc=f'Teams in {league_name}', leave=False, unit='team'):
            # try:
            player_details = fetch_player_details(team_id)
            for player_id, player_name in player_details:
                writer.writerow([league_id, team_id, player_id, player_name])


print(f"Data has been written to {filename}")

