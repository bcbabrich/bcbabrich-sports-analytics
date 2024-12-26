import pandas as pd
import matplotlib.pyplot as plt
import random
import os
from datetime import date
import numpy as np

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

# Set a range of dates to find local maxima in
upperDate = pd.Timestamp(year=2024, month=12, day=22)
lowerDate = pd.Timestamp(year=2024, month=12, day=20)

# Data looks like:
# Away Team,Home Team,Away Odds,Home Odds,Winner,Date
# "AFC","NFC",+114,-137,1,08 Feb 2009
# "Pittsburgh Steelers","Arizona Cardinals",-244,+202,0,01 Feb 2009
# "Pittsburgh Steelers","Baltimore Ravens",-256,+218,0,18 Jan 2009
# "Arizona Cardinals","Philadelphia Eagles",+149,-182,0,18 Jan 2009
# "Pittsburgh Steelers","Los Angeles Chargers",-303,+243,0,11 Jan 2009
# "New York Giants","Philadelphia Eagles",-222,+177,1,11 Jan 2009
df = pd.read_csv('./in/ProcessedNFLGames.csv').astype({
    'Away Team': 'string',
    'Home Team': 'string',
    'Away Odds': 'int',
    'Home Odds': 'int',
    'Date': 'datetime64[s]'
}).sort_values(by='Date')

plt.figure(figsize=(15, 10))
plt.axhline(initial_bankroll, color='red', linestyle='--', label='Initial Bankroll')

for team in NFLTeams:

    print("+++")
    print(f"Processing team '{team}' in range {lowerDate} to {upperDate}")
    print("+++")

    bankroll = initial_bankroll
    bankroll_history = np.array([])
    dates = []
    prevbankroll = 0
    localprofits = []

    for index, row in df.iterrows():

        print("...")

        # --------------------------------------------------------------
        # Apply date,team filter and get the odds
        date = row['Date']
        print(f"Date is {date}")
        if not (lowerDate < date and date < upperDate):
            print(f"Date is not in range {lowerDate} to {upperDate}")
            continue
        else:
            if row['Away Team'] == team:
                odds = int(row['Away Odds'])
            elif row['Home Team'] == team:
                print(f"Date is in range {lowerDate} to {upperDate} and {team} played this game at home")
                odds = int(row['Home Odds'])
            else:
                continue
            print(f"Processing odds {odds}")
            dates.append(date)

        # --------------------------------------------------------------
        # Bet 10 dollars every time and update the bankroll history
        bet = 10
        bankroll -= bet
        betreturn = calculate_return(odds, bool(row['Winner']), bet)
        bankroll += betreturn
        print(f"Bankroll is {bankroll}")
        bankroll_history = np.append(bankroll_history, [bankroll])

        # --------------------------------------------------------------
        # Current rate of change must be greater than zero to indicate a local profit
        print(f"Prev bankroll is {prevbankroll}")
        print(f"Bet return is {betreturn}")
        curLocProf = 0 < prevbankroll and 0 < betreturn
        print(f"Current local profit is {curLocProf}")
        localprofits.append(curLocProf)
        prevbankroll = betreturn

    # --------------------------------------------------------------
    # Use localprofits as a mask for the bankroll history and plot the graph
    # Remember that a mask says "whether a value is valid or not"
    # Therefore, apply the "green" mask to the inverse of the local profits
    print(f"applying local profits mask, length of local profits is {len(localprofits)}")
    winning_bankroll_history = np.ma.array(bankroll_history, mask=np.logical_not(localprofits))
    losing_bankroll_history = np.ma.array(bankroll_history, mask=localprofits)
    plt.plot(dates, winning_bankroll_history, 'og', dates, losing_bankroll_history, 'or')

# Finalize plot
plt.xlabel('Date')
plt.ylabel('Bankroll ($)')
plt.title(f"Bankroll over range {lowerDate} to {upperDate} for all teams")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Ensure output directory exists
output_dir = './out/'
os.makedirs(output_dir, exist_ok=True)
file_name = f"all_teams_over_{lowerDate}_{upperDate}_colorizes_wins_losses.png"
output_path = os.path.join(output_dir, file_name)
print(f"Saving plot to {output_path}")

# Save the plot
plt.savefig(output_path)
