# --------------------------------------------------------------
# Imports
# --------------------------------------------------------------
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

print("Hello, world!")

# --------------------------------------------------------------
# Set up an instance of the Firefox browser using Selenium
# the gecko driver is set to my local path
options = webdriver.FirefoxOptions()
options.binary_location = "/usr/bin/firefox"
options.add_argument("--headless")
geckodriver_path = "/home/chase/Projects/bcbabrich-sports-analytics/geckodriver"
service = Service(geckodriver_path)

# --------------------------------------------------------------
# Choose path to write output to
output_path = "/home/chase/Projects/bcbabrich-sports-analytics/out"
save_htmls = False

# --------------------------------------------------------------
# Initialize a fresh instance of the FF browswer
# Open a try block to catch any exceptions
driver = webdriver.Firefox(service=service, options=options)
try:

    # --------------------------------------------------------------
    # Load a parameterized URL
    # then scroll up and down to yield the lazy-loaded content
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
element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/main/div[3]/div[4]/div[1]/div[1]')
toSoup = element.get_attribute('innerHTML')
soup = BeautifulSoup(toSoup, 'html.parser')

# --------------------------------------------------------------
# One layer deeper from the parsed HTML is a list of divs.
# The outter divs are containers for inner "game info" divs.
soup.div
outterDivs = soup.contents

# --------------------------------------------------------------
# Write soup.pretty() to a file
with open(f"{output_path}/outterDivs.html", "w") as f:
    f.write(soup.prettify())
for outterDiv in outterDivs:

    # Use regex from here on out
    outterDivStr = outterDiv.prettify()
    print(f"outterDivStr: {outterDivStr}")
    print("...")
    print("...")
    print("...")
    print("...")
    print("...")
    print("...")
    print("...")
    print("...")
    lenOutterDiv = len(list(outterDiv.contents))
    print(f"lenOutterDiv: {lenOutterDiv}")
    match lenOutterDiv:

        # --------------------------------------------------------------
        # Odds div is present only
        case 1:
            print("There is 1 div inside the outter div")

            # Extract the away team
            awayTeamPattern = r'<a\s+data-v-[a-z0-9]+=""\s+class="min-mt:!justify-end flex min-w-0 basis-\[50%\] cursor-pointer items-start justify-start gap-1 overflow-hidden"\s+title=".*?">'
            matches = re.findall(awayTeamPattern, strOutterDiv, flags=re.DOTALL)
            print(f"awayTeamPattern matches: {matches}")

        case 2:
            print("There are 2 divs inside the outter div")
        case 3:
            print("There are 3 divs inside the outter div")


driver.quit()

