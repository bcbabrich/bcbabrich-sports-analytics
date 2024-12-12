#!/bin/bash

# Create an output file
output_file="./out/MergedNFLGames.csv"

# Write the header only once into the output file
echo "Away Team,Home Team,Away Odds,Home Odds,Winner,Date" > "$output_file"

# Process all files
for file in ./out/NFLGames_*.csv; do
  # Skip the first line (header) for every file and remove any header line within the file
  awk 'NR > 1 && $0 != "Away Team,Home Team,Away Odds,Home Odds,Winner,Date"' "$file" >> "$output_file"
done
