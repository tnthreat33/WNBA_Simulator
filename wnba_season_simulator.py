import pandas as pd
import numpy as np
import random

wnba_teams = pd.read_csv("wnba_team_stats.csv")

team_records_overall = {team: {"Total Wins": 0, "Total Losses": 0} for team in wnba_teams["Team"]}

def simulate_game(team1, team2, home_team):
    """
    Simulates a game 100 times and returns the most frequent winner.
    Home team gets a small advantage.
    """
    print(f"Simulating game: {team1} vs {team2} (Home: {home_team})") 

    if team1 not in wnba_teams["Team"].values or team2 not in wnba_teams["Team"].values:
        print(f"Error: {team1} or {team2} not found in dataset!")
        return None

    team1_stats = wnba_teams[wnba_teams["Team"] == team1].iloc[0]
    team2_stats = wnba_teams[wnba_teams["Team"] == team2].iloc[0]

    team1_wins = 0
    team2_wins = 0

    for _ in range(100):  
        team1_score = np.random.normal(team1_stats["PTS"], 5)
        team2_score = np.random.normal(team2_stats["PTS"], 5)

        if home_team == team1:
            team1_score += 2  
        elif home_team == team2:
            team2_score += 2

        if team1_score > team2_score:
            team1_wins += 1
        else:
            team2_wins += 1

    return team1 if team1_wins > team2_wins else team2

season_schedule = []
teams = list(wnba_teams["Team"])

for team1 in teams:
    for team2 in teams:
        if team1 != team2:
            season_schedule.append((team1, team2, team1))  
            season_schedule.append((team2, team1, team2))  

num_seasons = 100

print(f"Starting season simulations: {num_seasons} seasons...")

for season in range(num_seasons):
    if season % 100 == 0:  
        print(f"Simulating season {season + 1}/{num_seasons}...")

    team_records = {team: {"Wins": 0, "Losses": 0} for team in teams}

    for game in season_schedule:
        team1, team2, home_team = game
        winner = simulate_game(team1, team2, home_team)

        if winner:
            team_records[winner]["Wins"] += 1
            team_records[team1 if winner != team1 else team2]["Losses"] += 1

    for team in teams:
        team_records_overall[team]["Total Wins"] += team_records[team]["Wins"]
        team_records_overall[team]["Total Losses"] += team_records[team]["Losses"]

print("Simulation complete! Processing final standings...")

final_standings = pd.DataFrame.from_dict(team_records_overall, orient="index")
final_standings["Avg Wins"] = final_standings["Total Wins"] / num_seasons
final_standings["Avg Losses"] = final_standings["Total Losses"] / num_seasons

final_standings = final_standings.sort_values(by="Avg Wins", ascending=False)

print(final_standings[["Avg Wins", "Avg Losses"]])
