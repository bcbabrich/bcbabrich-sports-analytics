import pandas as pd
import matplotlib.pyplot as plt
import random
import os
from datetime import date

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
 "Carolina Panthers"
]

# Initialize bankroll
initial_bankroll = 100  # Starting amount

# Set a range of dates to find local maxima in
upperDate = pd.Timestamp(year=2015, month=2, day=1)
lowerDate = pd.Timestamp(year=2014, month=8, day=3)

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
    bankroll_history = []
    dates = []

    for index, row in df.iterrows():

        print("...")

        # --------------------------------------------------------------
        # Apply date filter and get the odds
        date = row['Date']
        print(f"Date is {date}")
        if not (lowerDate < date and date < upperDate):
            print(f"Date is not in range {lowerDate} to {upperDate}")
            continue
        else:
            print(f"Date is in range {lowerDate} to {upperDate}. Lenth of dates is {len(dates)}")
            if row['Away Team'] == team:
                odds = int(row['Away Odds'])
            elif row['Home Team'] == team:
                odds = int(row['Home Odds'])
            else:
                continue
            print(f"Processing odds {odds}")
            dates.append(date)

        # --------------------------------------------------------------
        # Get 10 dollars every time and update the bankroll history
        bankroll -= 10
        bankroll += calculate_return(odds, bool(row['Winner']), 10)
        print(f"Bankroll is {bankroll}")
        bankroll_history.append(bankroll)

    # Plot bankroll history for the team
    plt.plot(dates, bankroll_history)

# Finalize plot
plt.xlabel('Date')
plt.ylabel('Bankroll ($)')
plt.title(f"Bankroll over range {lowerDate} to {upperDate} for team '{team}'")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Ensure output directory exists
output_dir = './out/individual/'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"{team}_over_{lowerDate}_{upperDate}.png")
print(f"Saving plot to {output_path}")

# Save the plot
plt.savefig(output_path)
