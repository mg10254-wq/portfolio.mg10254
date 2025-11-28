# fetch_euler_stats.py
import requests
from bs4 import BeautifulSoup
import json

USERNAME = "Matteo_G"  # your Project Euler username
URL = f"https://projecteuler.net/profile/{USERNAME}"

response = requests.get(URL)
if response.status_code != 200:
    raise Exception("Failed to fetch profile")

soup = BeautifulSoup(response.text, "html.parser")

solved_count = None
for td in soup.find_all("td"):
    if td.get_text(strip=True) == "Solved:":
        solved_count = int(td.find_next_sibling("td").get_text(strip=True))
        break

if solved_count is None:
    raise Exception("Could not find solved count on page")

# Save JSON
with open("euler_stats.json", "w") as f:
    json.dump({"solved": solved_count}, f)

print(f"Solved problems: {solved_count}")
