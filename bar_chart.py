import pandas as pd
import matplotlib.pyplot as plt
import os

# Function to calculate returns
def calculate_return(odds, Winner, bet_amount):

    odds = int(odds)

    if Winner:
        if odds < 0:
            # Moneyline calculator for negative odds
            return (100 / abs(odds)) * bet_amount
        else:
            # Moneyline calculator for positive odds
            return (odds / 100) * bet_amount
    else:
        return -bet_amount  # Lost the bet

# List of NFL teams
NFLTeams = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills",
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns",
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers",
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs",
    "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
    "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants",
    "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers",
    "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"
]

# Initialize bankroll
initial_bankroll = 100  # Starting amount

# Set experiment parameters
dataset = './out/NFLGamesStringified.csv'

# Load the data
df = pd.read_csv(dataset)

# Count how many times each team appears in the dataset
team_bet_counts = {team: 0 for team in NFLTeams}

for _, row in df.iterrows():
    if row['Away Team'] in team_bet_counts:
        team_bet_counts[row['Away Team']] += 1
    if row['Home Team'] in team_bet_counts:
        team_bet_counts[row['Home Team']] += 1

# Visualize the counts
plt.figure(figsize=(15, 8))
teams = list(team_bet_counts.keys())
counts = list(team_bet_counts.values())

plt.bar(teams, counts, color='skyblue')
plt.xticks(rotation=90)
plt.xlabel('NFL Teams')
plt.ylabel('Number of Bets')
plt.title('Number of Bets on Each NFL Team')
plt.tight_layout()

# Ensure output directory exists
output_dir = './out'
os.makedirs(output_dir, exist_ok=True)
output_path_bets = os.path.join(output_dir, 'team_bet_counts.png')

# Save the bar chart
plt.savefig(output_path_bets)
print(f"Bar chart saved to {output_path_bets}")

plt.show()

