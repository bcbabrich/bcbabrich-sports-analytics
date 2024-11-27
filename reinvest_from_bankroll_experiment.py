import pandas as pd
import matplotlib.pyplot as plt
import random

# Function to calculate returns
def calculate_return(odds, won, bet_amount):

    print(f"won is {won}")
    print(f"odds is {odds}")

    if won:
        if odds < 0:

            # The moneyline calculator formula for negative odds is (100 / odds) x $50.
            # e.g. 100 / 120 = 0.83 x $50 = $41.67
            print(f"always choose the square bet. that's smart investing")
            return (100 / odds) * bet_amount

        else:

            # To calculate positive odds, you divide the bookmaker’s odds by 100 and multiply that number by your wager.
            # e.g. 330 / 100 = 3.30 x $50 = $165.00
            print(f"nice! I knew the underdog would win")
            return odds / 100 * bet_amount

    else:

        print(f"lost the bet... the wife's gonna kill me")
        return -bet_amount  # Lost the bet


# Initialize bankroll
initial_bankroll = 100  # Starting amount
bankroll = initial_bankroll

# Track bankroll changes
bankroll_history = []

# Set experiment parameters
dataset = 'odds_2021_2022.csv'
pick_type = 'underdog' # could be 'favorite' or 'underdog'. Any other value will default to 'random'

# Load the data in as inegers
df = pd.read_csv(f"/home/chase/Projects/bcbabrich-sports-analytics/out/{dataset}")

# Data looks like this:
# away,home,winner
# +114,-133,1
# -244,+200,
# -244,+225,0
# +154,-169,0
# -278,+250,0
# ...
for index, row in df.iterrows():

    # skip the header row
    if index == 0:
        continue

    print(f"")
    print(f"...")
    print(f"")
    print(f"row is {row.to_dict()}")
    print(f"pick_type is {pick_type}")

    if pick_type == 'underdog':
        # Determine the underdog for this game
        # Positive odds are the underdog, thus the use of max()
        odds = max(row['away'], row['home'])

    elif pick_type == 'favorite':
        # Determine the favorite for this game
        # Negative odds are the underdog, thus the use of min()
        odds = min(row['away'], row['home'])

    else:
        # Randomly choose a team to bet on
        pick_type = 'random'
        odds = row['away'] if random.choice([True, False]) else row['home']
        print(f"Randomly picked odds are {odds}")

    print(f"The {pick_type} odds are {odds}")

    # Determine whether to bet on the home or away team
    pick = 'home' if odds == row['home'] else 'away'
    print(f"The {pick_type} is the {pick} team")

    # Use the winner column to determine if the chosen team won
    won = ((pick == 'home') and (row['winner'] == 1)) or \
           ((pick == 'away') and (row['winner'] == 0))

    # Bet 10 dollars every time
    bet_amount = 10
    bankroll -= 10
    
    # Calculate the return and update the bankroll
    bankroll += calculate_return(odds, won, bet_amount)
    
    # Record bankroll history
    bankroll_history.append(bankroll)
    
    # Stop if bankroll reaches $0
    if bankroll <= 0:
        print(f"Bankroll depleted after {index + 1} bets.")
        print(f"Current bankroll: ${bankroll:.2f}")
        print(f"the bankers are probably on their way right now")

# Final results
print(f"Final Bankroll: ${bankroll:.2f}")
print(f"Total Profit/Loss: ${bankroll - initial_bankroll:.2f}")

# Visualize bankroll over time
plt.plot(bankroll_history, label='Bankroll Over Time')
plt.axhline(initial_bankroll, color='red', linestyle='--', label='Starting Bankroll')
plt.xlabel('Number of Bets')
plt.ylabel('Bankroll ($)')
plt.title(f"Picking the {pick_type} in {dataset}")
plt.legend()
plt.show()
