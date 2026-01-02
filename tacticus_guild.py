import requests
import json
from datetime import datetime, timedelta
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout
arena_regen_minutes = 160
onslaught_regen_minutes = 960
salvage_regen_minutes = 720
raid_regen_minutes = 960
energy_regen_minutes = 5
arena_cap = 15
onslaught_cap = 3
salvage_cap = 2
raid_cap = 3
energy_cap = 142
seasonNum = "90"
api_url = "https://api.tacticusgame.com/api/v1/guildRaid/" + seasonNum 

headers = {'accept': 'application/json', 'X-API-KEY': '136af88a-a7c3-4a8a-89d8-991d9091484c'}
try:
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
except HTTPError as e:
    print(e)
data = response.json()
print(data)
		