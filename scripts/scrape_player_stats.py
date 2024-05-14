import requests
import csv
from tqdm import tqdm

# Function to fetch player profile
def fetch_player_profile(player_id):
    response = requests.get(f'https://www.fotmob.com/api/playerData?id={player_id}')
    profile_data = response.json()
    
    # def get_stat_by_title(items, title):
    #     for item in items:
    #         if item.get("translationKey") == title:
    #             return item.get("statValue", 0)
    #     return 0
    
    # def get_player_info_by_key(player_info_list, search_key, data_type = 'number', data_key='numberValue'):
    #     for info in player_info_list:
    #         if info.get('translationKey', '') == search_key:
    #             # Navigate to 'value' then to 'numberValue' or another specified key
    #             return info.get('value', {}).get(data_key, 0)
    #     return 0  # Return a default value if not found

    def get_player_info_by_key(player_info_list, search_key, data_key='numberValue', title_key='translationKey', nested = 0):
        for info in player_info_list:
            if info.get(title_key, '') == search_key:
                # Navigate to 'value' then to 'numberValue' or another specified key
                if nested == 0:
                    return info.get('value', {}).get(data_key, 0)
                elif nested == 1:
                    return info.get(data_key, 0)
        return 0  # Return a default value if not found
    

    return {
        'name': profile_data["name"],
        'playerId': profile_data["id"],
        # 'marketValueEUR': profile_data["playerInformation"][5]["value"]["numberValue"],
        'marketValueEUR': get_player_info_by_key(profile_data["playerInformation"], "transfer_value"),
        'country': get_player_info_by_key(profile_data["playerInformation"], "country_sentencecase", data_key='fallback'),
        # 'country': profile_data["playerInformation"][4]["value"]["fallback"],
        'birthDate': profile_data["birthDate"]["utcTime"],
        # 'age':profile_data["playerInformation"][2]["value"]["numberValue"],
        'teamName': profile_data["primaryTeam"]["teamName"],
        'teamId': profile_data["primaryTeam"]["teamId"],
        'leagueName': profile_data["mainLeague"]["leagueName"],
        'leagueId': profile_data["mainLeague"]["leagueId"],
        'onLoan': profile_data["primaryTeam"]["onLoan"],
        # 'height': profile_data["playerInformation"][0]["value"]["numberValue"],
        'height': get_player_info_by_key(profile_data["playerInformation"], "height_sentencecase"),
        # 'preferredfoot': profile_data["playerInformation"][3]["value"]["fallback"],
        'preferredFoot': get_player_info_by_key(profile_data["playerInformation"], "preferred_foot", data_key='fallback'),
        # 'goals': profile_data["mainLeague"]["stats"][0]["value"],
        'goals': get_player_info_by_key(profile_data["mainLeague"]["stats"], "goals",data_key= "value", title_key="localizedTitleId", nested = 1),
        # 'assists': profile_data["mainLeague"]["stats"][1]["value"],
        'assists': get_player_info_by_key(profile_data["mainLeague"]["stats"], "assists",data_key= "value", title_key="localizedTitleId", nested = 1),
        # 'games': profile_data["mainLeague"]["stats"][3]["value"],
        'games': get_player_info_by_key(profile_data["mainLeague"]["stats"], "matches_uppercase",data_key= "value", title_key="localizedTitleId", nested = 1),
        # 'startedGames': profile_data["mainLeague"]["stats"][2]["value"],
        'startedGames': get_player_info_by_key(profile_data["mainLeague"]["stats"], "started",data_key= "value", title_key="localizedTitleId", nested = 1),
        # 'minutesPlayed': profile_data["mainLeague"]["stats"][4]["value"],
        'minutesPlayed': get_player_info_by_key(profile_data["mainLeague"]["stats"], "minutes_played",data_key= "value", title_key="localizedTitleId", nested = 1),
        # 'avgRating': profile_data["mainLeague"]["stats"][5]["value"],
        'avgRating': get_player_info_by_key(profile_data["mainLeague"]["stats"], "rating",data_key= "value", title_key="localizedTitleId", nested = 1),
        # 'yellowCards': profile_data["mainLeague"]["stats"][6]["value"],
        'yellowCards': get_player_info_by_key(profile_data["mainLeague"]["stats"], "yellow_cards",data_key= "value", title_key="localizedTitleId", nested = 1),
        # 'redCards': profile_data["mainLeague"]["stats"][7]["value"],
        'redCards': get_player_info_by_key(profile_data["mainLeague"]["stats"], "red_cards",data_key= "value", title_key="localizedTitleId", nested = 1)
        
    }

# Function to fetch player statistics
def fetch_player_stats(player_id, league_id):
    response = requests.get(f'https://www.fotmob.com/api/playerStats?playerId={player_id}&seasonId=2023%2F2024-{league_id}')
    stats_data = response.json()
    
    def get_stat_by_title(items, title):
        for item in items:
            if item.get("localizedTitleId") == title:
                return item.get("statValue", 0)
        return 0
    
    stats = {
        'xG': get_stat_by_title(stats_data["statsSection"]["items"][0]["items"], "expected_goals"),
        'xGOT': get_stat_by_title(stats_data["statsSection"]["items"][0]["items"], "expected_goals_on_target"),
        'penaltyGoals': get_stat_by_title(stats_data["statsSection"]["items"][0]["items"], "goals_subtitle"),
        'xG_nonPenalty': get_stat_by_title(stats_data["statsSection"]["items"][0]["items"], "non_penalty_xg"),
        'shots': get_stat_by_title(stats_data["statsSection"]["items"][0]["items"], "shots"),
        'shotsOnTarget': get_stat_by_title(stats_data["statsSection"]["items"][0]["items"], "ShotsOnTarget"),
        'xA': get_stat_by_title(stats_data["statsSection"]["items"][1]["items"], "expected_assists"),
        'accuratePasses': get_stat_by_title(stats_data["statsSection"]["items"][1]["items"], "successful_passes"),
        'passAccuracy': get_stat_by_title(stats_data["statsSection"]["items"][1]["items"], "successful_passes_accuracy"),
        'accurateLongBalls': get_stat_by_title(stats_data["statsSection"]["items"][1]["items"], "long_balls_accurate"),
        'longBallAccuracy': get_stat_by_title(stats_data["statsSection"]["items"][1]["items"], "long_ball_succeeeded_accuracy"),
        'chancesCreated': get_stat_by_title(stats_data["statsSection"]["items"][1]["items"], "chances_created"),
        'successfulCrosses': get_stat_by_title(stats_data["statsSection"]["items"][1]["items"], "crosses_succeeeded"),
        'crossAccuracy': get_stat_by_title(stats_data["statsSection"]["items"][1]["items"], "crosses_succeeeded_accuracy"),
        'dribbles': get_stat_by_title(stats_data["statsSection"]["items"][2]["items"], "dribbles_succeeded"),
        'dribblesSuccessRate': get_stat_by_title(stats_data["statsSection"]["items"][2]["items"], "won_contest_subtitle"),
        'touches': get_stat_by_title(stats_data["statsSection"]["items"][2]["items"], "touches"),
        'touchesOppositionBox': get_stat_by_title(stats_data["statsSection"]["items"][2]["items"], "touches_opp_box"),
        'dispossesed': get_stat_by_title(stats_data["statsSection"]["items"][2]["items"], "dispossessed"),
        'foulsWon': get_stat_by_title(stats_data["statsSection"]["items"][2]["items"], "fouls_won"),
        'aerialsWon': get_stat_by_title(stats_data["statsSection"]["items"][3]["items"], "aerials_won"),
        'aerialsWonPct': get_stat_by_title(stats_data["statsSection"]["items"][3]["items"], "aerials_won_percent"),
        'foulsComitted': get_stat_by_title(stats_data["statsSection"]["items"][3]["items"], "fouls"),
        'possessionWonFinal3rd': get_stat_by_title(stats_data["statsSection"]["items"][3]["items"], "poss_won_att_3rd_team_title")
    }

    return stats
    

# Combine data for a single player
def combine_player_data(player_id, league_id):
    profile = fetch_player_profile(player_id)
    stats = fetch_player_stats(player_id, league_id)
    profile.update(stats)  # Merge profile and stats dictionaries
    return profile

input_filename = '../data/player_details.csv'
output_filename = '../data/player_stats.csv'

# Open the input CSV file to read player IDs and league IDs
with open(input_filename, mode='r', newline='') as infile, \
     open(output_filename, mode='w', newline='') as outfile:

    # Prepare to read from input and write to output
    reader = csv.DictReader(infile)
    fieldnames = ['name','playerId', 'marketValueEUR', 'country', 'birthDate', 'teamName', 'teamId', 'leagueName',
                  'leagueId', 'onLoan', 'height', 'preferredFoot', 'goals', 'assists', 'games',
                  'startedGames', 'minutesPlayed', 'avgRating', 'yellowCards', 'redCards',
                  'xG', 'xGOT', 'penaltyGoals', 'xG_nonPenalty', 'shots', 'shotsOnTarget', 'xA',
                  'accuratePasses', 'passAccuracy', 'accurateLongBalls', 'longBallAccuracy',
                  'chancesCreated', 'successfulCrosses', 'crossAccuracy', 'dribbles', 'dribblesSuccessRate',
                  'touches', 'touchesOppositionBox', 'dispossesed', 'foulsWon', 'aerialsWon', 'aerialsWonPct',
                  'foulsComitted', 'possessionWonFinal3rd']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each row in the input CSV file
    for row in tqdm(reader, desc="Processing players"):
        player_id = row['playerId']
        league_id = row['leagueId']
        
        try:
            player_data = combine_player_data(player_id, league_id)
            writer.writerow(player_data)
        except Exception as e:
            print(f"Failed to fetch data for player ID {player_id}: {e}")

print(f"Data has been written to {output_filename}")
