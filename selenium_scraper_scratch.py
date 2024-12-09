# --------------------------------------------------------------
# Imports
# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service  # Use Firefox Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# --------------------------------------------------------------
# Set up an instance of the Firefox browser using Selenium
# the gecko driver is set to my local path
options = webdriver.FirefoxOptions()
options.binary_location = "/usr/bin/firefox"
options.add_argument("--headless")
geckodriver_path = "/home/chase/Projects/bcbabrich-sports-analytics/geckodriver"
service = Service(geckodriver_path)

# --------------------------------------------------------------
# Parameters
output_path = "/home/chase/Projects/bcbabrich-sports-analytics/out"
input_path = "/home/chase/Projects/bcbabrich-sports-analytics/in"
useSelenium = False
print(f"output_path is {output_path}")
print(f"input_path is {input_path}")
print(f"useSelenium is {useSelenium}")

# Open a try block to catch any exceptions
if useSelenium:
    driver = webdriver.Firefox(service=service, options=options)
    try:

        # --------------------------------------------------------------
        # Load a parameterized URL scroll up and down to yield the lazy-loaded content
        url = f"https://www.oddsportal.com/american-football/usa/nfl/results/#/page/1"
        print(f"Loading page 1 at {url}")
        driver.get(url)
        print(f"Waiting for page 1 to load, this will take 20 seconds")
        time.sleep(20)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Waiting for page 1 to load, this will take 5 seconds")
        time.sleep(5)  # Allow lazy-loaded content to load
        driver.execute_script("window.scrollTo(0, 0);")
        print(f"Waiting for page 1 to load, this will take 3 seconds")
        time.sleep(3)
        
    except Exception as e:
        print(f"Error: {e}")
        htmlFull = ""
        driver.quit()

    # --------------------------------------------------------------
    # Jump over from Selenium to Beautiful Soup 4
    # Leverage a CSS selector that will not change too much
    # Parse the div of all the games info from Selenium to BS4
    # https://selenium-python.readthedocs.io/locating-elements.html#locating-by-xpath
    element = driver.find_element(By.CSS_SELECTOR, ".min-h-\[206px\]")
    toSoup = element.get_attribute('innerHTML')
    soup = BeautifulSoup(toSoup, 'html.parser')

    # --------------------------------------------------------------
    # Save the partially rendered HTML
    with open(f"{input_path}/beautifulSoupBackup.html", "w") as f:
        f.write(toSoup)
        print(f"HTML backup successfully saved!")

else:     

    # Read in the HTML from {output_path}/toSoup.html instead of Selenium
    print(f"Reading in the HTML from {input_path}/beautifulSoupBackup..html")
    with open(f"{input_path}/beautifulSoupBackup.html", "r") as f:
        toSoup = f.read()
        soup = BeautifulSoup(toSoup, 'html.parser')

# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
# Write soup to a file
print(f"printing soup to a file")
with open(f"{output_path}/soupPrettify.html", "w") as f:
    f.write(soup.prettify())

# --------------------------------------------------------------
# One layer deeper from the parsed HTML is a list of divs.
# The outter divs are containers for inner "game info" divs.
# The soup object updates its position in the tree based on tag name
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigating-using-tag-names 
soup.div

# --------------------------------------------------------------
# Print soup.div to a file
print(f"Writing soup.div to {output_path}/soupDiv.html")
with open(f"{output_path}/soupDiv.html", "w") as f:
    f.write(soup.div.prettify())

# --------------------------------------------------------------
# Find all the game divs inside this container div which themselves are container divs
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children
outterDivs = soup.div.contents

# --------------------------------------------------------------
# Print length of outterDivs to the console
print(f"Found {len(outterDivs)} number of outterDivs")

# --------------------------------------------------------------
# At this point outterDivs is a list of python objects we can loop over
i = 0

# Begin a list of strings that will be written to a CSV file
csvRows = ["Away Team,Home Team,Away Odds,Home Odds,Winner,Date"]

for outterDiv in outterDivs:
    i += 1
    print(f"Processing outterDiv {i}")

    # --------------------------------------------------------------
    # Some of the outterDivs are newline characters
    if isinstance(outterDiv, str):
        print("outterDiv is a string")
        outterDivStr = outterDiv
        if outterDivStr == "\n" or outterDivStr == "" or outterDivStr == " ":
            print("outterDiv is '{outterDivStr}', skipping")
            continue
    else:
        print("outterDiv is a BS4 object")
        outterDivStr = outterDiv.prettify()

    # --------------------------------------------------------------
    print(f"Writing outterDiv to {output_path}/outterDiv_{i}.html")
    with open(f"{output_path}/outterDiv_{i}.html", "w") as f:
        f.write(outterDivStr)

    # --------------------------------------------------------------
    # Use regex to extract the paragraph tags containing the team names
    teamParagraphRegex = r'<p class="participant-name truncate" data-v-a4e7076e="">\s*(.*?)\s*</p>'
    teamParagraphMatches = re.findall(teamParagraphRegex, outterDivStr, flags=re.DOTALL)
    print(f"Found {len(teamParagraphMatches)} team paragraph matches")
    awayTeam = teamParagraphMatches[0]
    homeTeam = teamParagraphMatches[1]
        
    # --------------------------------------------------------------
    # Use regex to extract the paragraph tags containing the date information
    # Presumably there is only one
    yesterDayPattern = r"Yesterday, \d{1,2} [A-Za-z]+"
    todayDayPattern = r"Today, \d{1,2} [A-Za-z]+"
    anyDayPattern = r"\d{1,2} [A-Za-z]+ \d{4}"
    datePatterns = [yesterDayPattern, todayDayPattern, anyDayPattern]
    for datePattern in datePatterns:
        dateMatches = re.findall(datePattern, outterDivStr, flags=re.DOTALL)
        if len(dateMatches) > 0:
            print(f"Found matches for pattern `{datePattern}`, all matches are {' '.join(dateMatches)}")
            break
    if len(dateMatches) == 0:
        print(f"Could not find a date match")
        date = "_"
    else:
        date = dateMatches[0]
        print(f"Found date {date}")

    # --------------------------------------------------------------
    # Use regex to extract the paragraph tags containing the odds
    # In this case there are only two matches and it is already a pair
    # print the number of matches found
    oddsPattern = r"<p\s[^>]*>\s*[-+]?\d+\s*<\/p>"
    matches = re.findall(oddsPattern, outterDivStr, flags=re.DOTALL)
    inner_value_pattern = r">([^<]+)<"
    odds = [re.search(inner_value_pattern, p).group(1) for p in matches]
    w = "0" if ' gradient-green ' in matches[0] else "1"
    awayTeamOdds = "".join(odds[0].split())
    homeTeamOdds = "".join(odds[1].split())

    # --------------------------------------------------------------
    # Create and append the row to the CSV list
    csvRow = f"{awayTeam},{homeTeam},{awayTeamOdds},{homeTeamOdds},{w},{date}"
    print(f"Appending row {csvRow}")
    csvRows.append(csvRow)

# --------------------------------------------------------------
# Write the CSV list to a file
with open(f"{output_path}/NFLGames.csv", "w") as f:
    for row in csvRows:
        f.write(f"{row}\n")
