# --------------------------------------------------------------
# Imports
# --------------------------------------------------------------
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
geckodriver_path = "/home/chase/Projects/Scraper/geckodriver"
service = Service(geckodriver_path)

# --------------------------------------------------------------
# Choose path to write output to
output_path = "/home/chase/Projects/Scraper/out"
save_htmls = False

# --------------------------------------------------------------
# Loop over urls like `https://www.oddsportal.com/american-football/usa/nfl/results/#/page/2/`
# starting at 1 until the html contains this text
# "Unfortunately, no matches can be displayed because there are no odds available from your selected bookmakers"
for i in range(1, 100):

    # --------------------------------------------------------------
    # Initialize a fresh instance of the FF browswer
    # Open a try block to catch any exceptions
    driver = webdriver.Firefox(service=service, options=options)
    try:

        # --------------------------------------------------------------
        # Load a parameterized URL, wait for it to load,
        # then scroll up and down to yield the lazy-loaded content
        year = "nfl-2008-2009/" # use an empty string for the current season
        url = f"https://www.oddsportal.com/american-football/usa/{year}results/#/page/{i}"
        print(f"Loading page {i} at {url}")
        driver.get(url)
        print(f"Waiting for page {i} to load, this will take 20 seconds")
        time.sleep(20)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Waiting for page {i} to load, this will take 5 seconds")
        time.sleep(5)  # Allow lazy-loaded content to load
        driver.execute_script("window.scrollTo(0, 0);")
        print(f"Waiting for page {i} to load, this will take 3 seconds")
        time.sleep(3)

        # --------------------------------------------------------------
        # Get the fully rendered HTML
        htmlFull = driver.page_source
        
    except:
        htmlFull = ""
        driver.quit()

    # --------------------------------------------------------------
    # Check if the page is empty
    # break condition for the loop
    if "Unfortunately, no matches can be displayed because there are no odds available from your selected bookmakers" in htmlFull:
        print(f"Page {i} is empty")
        break

    if save_htmls:
        # --------------------------------------------------------------
        # write the html out to a versioned file
        # creates the file if it doesn't exist
        with open(f"{output_path}/{i}.html", "w") as f:
            f.write(htmlFull)
            print(f"HTML {i} successfully saved!")

    # --------------------------------------------------------------
    # Use regex to extract the paragraph tags containing the odds
    # print the number of matches found
    pattern = r"<p\b[^>]*?>[-+]?\d+<\/p>"
    matches = re.findall(pattern, htmlFull, flags=re.DOTALL)
    print(f"Found {len(matches)} matches")

    # --------------------------------------------------------------
    # Regex to extract the inner value of the paragraph tags
    # these are the actual odds themselves
    inner_value_pattern = r">([^<]+)<"

    # --------------------------------------------------------------
    # Determine winner and loser of each game
    # prepare a row to be written out to CSV
    rows = []
    for j in range(0, len(matches), 2):

        # --------------------------------------------------------------
        # Luckily we can identify the winner by a unique string in its tag
        # once found, put the odds and which is the winner in a list and print it
        pair = matches[j:j+2]
        inner_values = [re.search(inner_value_pattern, p).group(1) for p in pair]
        w = "0" if ' gradient-green ' in pair[0] else "1"
        l = [inner_values[0], inner_values[1], w]
        rows.append(l)

    # --------------------------------------------------------------
    # Write out the rows to a CSV file
    with open(f"{output_path}/odds.csv", "a") as f:
        for row in rows:
            f.write(",".join(row) + "\n")
        print(f"Rows for {i} successfully saved!")

    driver.quit()
