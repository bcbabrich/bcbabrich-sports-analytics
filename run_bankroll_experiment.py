import pandas as pd
import matplotlib.pyplot as plt
import random
import os

# Function to calculate returns
def calculate_return(odds, Winner, bet_amount):

    print(f"Winner is {Winner}")
    print(f"odds is {odds}")

    odds = int(odds)

    if Winner:
        if odds < 0:

            # The moneyline calculator formula for negative odds is (100 / odds) x bet_amount.
            print(f"always choose the square bet. that's smart investing")
            return (100 / abs(odds)) * bet_amount

        else:

            # To calculate positive odds, you divide the bookmaker’s odds by 100 and multiply that number by your wager.
            print(f"nice! I knew the underdog would win")
            return (odds / 100) * bet_amount

    else:

        print(f"lost the bet... the wife's gonna kill me")
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

# Data looks like:
# Away Team,Home Team,Away Odds,Home Odds,Winner,Date
# "AFC","NFC",+114,-137,1,08 Feb 2009
# "Pittsburgh Steelers","Arizona Cardinals",-244,+202,0,01 Feb 2009
# "Pittsburgh Steelers","Baltimore Ravens",-256,+218,0,18 Jan 2009
# "Arizona Cardinals","Philadelphia Eagles",+149,-182,0,18 Jan 2009
# "Pittsburgh Steelers","Los Angeles Chargers",-303,+243,0,11 Jan 2009
# "New York Giants","Philadelphia Eagles",-222,+177,1,11 Jan 2009
df = pd.read_csv('./out/ProcessedNFLGames.csv').astype({
    'Away Team': 'string',
    'Home Team': 'string',
    'Away Odds': 'int',
    'Home Odds': 'int',
    'Date': 'datetime64[s]'
}).sort_values(by='Date')

plt.figure(figsize=(15, 10))
plt.axhline(initial_bankroll, color='red', linestyle='--', label='Initial Bankroll')

for team in NFLTeams:

    print(f"Processing team: {team}")

    bankroll = initial_bankroll
    bankroll_history = []
    dates = []

    for index, row in df.iterrows():

        if row['Away Team'] == team:
            odds = int(row['Away Odds'])
        elif row['Home Team'] == team:
            odds = int(row['Home Odds'])
        else:
            continue

        # Bet 10 dollars every time
        bet_amount = 10
        bankroll -= 10
        
        # Calculate the return and update the bankroll
        bankroll += calculate_return(odds, bool(row['Winner']), bet_amount)
        
        # Record bankroll history
        print(f"Bankroll is {bankroll}")
        bankroll_history.append(bankroll)

        # Record date
        print(f"Date is {row['Date']}")
        dates.append(row['Date'])

    # Plot bankroll history for the team
    plt.plot(dates, bankroll_history)

# Finalize plot
plt.xlabel('Date')
plt.ylabel('Bankroll ($)')
plt.title(f"Bankroll Over Time (All Teams)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Ensure output directory exists
output_dir = './out/individual/'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"all_teams_bankroll_history.png")
print(f"Saving plot to {output_path}")

# Save the plot
plt.savefig(output_path)
