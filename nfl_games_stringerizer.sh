#!/bin/bash

# Input CSV file
input_file="./out/ProcessedNFLGames.csv"

# Output CSV file
output_file="./out/NFLGamesStringified.csv"

# Use awk to process the CSV
awk -F',' 'BEGIN { OFS="," } 
NR == 1 { print $0; next } # Keep the header as is
{
    $1 = "\"" $1 "\""; # Wrap Away Team
    $2 = "\"" $2 "\""; # Wrap Home Team
    print $0
}' "$input_file" > "$output_file"

echo "Processed file saved to $output_file"

