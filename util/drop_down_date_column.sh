#!/bin/bash

# Input and output file
input_file="./out/MergedNFLGames.csv"
output_file="./out/ProcessedNFLGames.csv"

# Use awk to process the file
awk -F, '
BEGIN { OFS = "," }  # Set output field separator to a comma
{
    # Check if the last field is a valid date (not "_")
    if ($6 ~ /^[0-9]{2} [A-Za-z]{3} [0-9]{4}$/) {
        last_date = $6  # Save the most recently seen date
    }
    # If the last field is "_", replace it with the most recently seen date
    else if ($6 == "_") {
        $6 = last_date
    }
    print $0  # Print the updated line
}
' "$input_file" > "$output_file"

echo "Processing complete. Output written to $output_file."
