# fetch_euler_stats.py
import requests
from bs4 import BeautifulSoup
import json
import sys

USERNAME = "Matteo_G"  # <-- Make sure this matches your Project Euler username exactly
URL = f"https://projecteuler.net/profile/{USERNAME}"

try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()  # raises exception for HTTP errors
except requests.RequestException as e:
    print(f"Failed to fetch profile: {e}")
    sys.exit(1)

soup = BeautifulSoup(response.text, "html.parser")

# Try to find the solved count in a robust way
solved_count = None
for row in soup.select("table.profile tr"):
    cells = row.find_all("td")
    if len(cells) >= 2 and cells[0].get_text(strip=True) == "Solved:":
        try:
            solved_count = int(cells[1].get_text(strip=True))
        except ValueError:
            print("Could not parse solved count as integer.")
            sys.exit(1)
        break

if solved_count is None:
    print("Could not find 'Solved:' count on profile page.")
    sys.exit(1)

# Save JSON
with open("euler_stats.json", "w") as f:
    json.dump({"solved": solved_count}, f)

print(f"Solved problems: {solved_count}")
