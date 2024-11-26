import pandas as pd

# Read data from a local CSV file
# Ensure the CSV file has the columns 'away', 'home', and 'winner' as shown in your example
df = pd.read_csv('/home/chase/Projects/Scraper/out/odds.csv')

# Determine the underdog for each matchup
df['underdog_odds'] = df[['away', 'home']].max(axis=1)
df['underdog'] = df[['away', 'home']].idxmax(axis=1)

# Determine if the underdog won
df['underdog_won'] = ((df['underdog'] == 'home') & (df['winner'] == 0)) | \
                     ((df['underdog'] == 'away') & (df['winner'] == 1))

# Calculate returns for betting $10 on the underdog
def calculate_return(odds, won):
    if won:
        if odds < 0:  # Negative odds
            return 10 * 100 / abs(odds) + 10
        else:  # Positive odds
            return 10 * odds / 100 + 10
    else:
        return -10  # Lost the bet

df['bet_return'] = df.apply(lambda row: calculate_return(row['underdog_odds'], row['underdog_won']), axis=1)

# Calculate total profit or loss
total_profit_loss = df['bet_return'].sum()

# Display the results
print(df[['away', 'home', 'underdog', 'underdog_odds', 'underdog_won', 'bet_return']])
print(f"\nTotal Profit/Loss: ${total_profit_loss:.2f}")