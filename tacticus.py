import requests
import json
from datetime import datetime, timedelta
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

api_url = "https://api.tacticusgame.com/api/v1/player"
headers = {'accept': 'application/json', 'X-API-KEY': '88017ac1-c16c-480d-876e-b2a3371c5bb3'}
response = requests.get(api_url, headers=headers)
response.raise_for_status()
data = response.json()
print(data["player"]["progress"]["arena"])
print(data["player"]["progress"]["onslaught"])
print(data["player"]["progress"]["guildRaid"])
print(data["player"]["progress"]["salvageRun"])
def date_when_cap(stock, cap, next_stock, regen_time):
	print("Stock: " + str(stock))
	print("Cap: " + str(cap))
	refill = cap - stock
	if refill == 1:
		print(next_stock)
		return datetime.now() + timedelta(seconds=next_stock)
	else:
		print("Next stock: " + str(next_stock))
		print("Regen time: " + str(regen_time))
		cap_seconds = timedelta(seconds=(next_stock + ((refill-1)*regen_time)))
		print(cap_seconds)
		return datetime.now() + cap_seconds
	
def stock_at_date(stock, next_stock, regen_time, end_date):
	seconds = int((end_date - datetime.now()).total_seconds())
	end_stock = stock
	if seconds < next_stock:
		return end_stock, seconds, seconds
	else:
		secs = seconds - next_stock
		end_stock += 1
		while (secs / regen_time) > 1:
			secs += -regen_time
			end_stock += 1
		return end_stock, secs, seconds
	
a_tokens = data["player"]["progress"]["arena"]["tokens"]["current"]
a_tokens_max = data["player"]["progress"]["arena"]["tokens"]["max"]
a_next = data["player"]["progress"]["arena"]["tokens"]["nextTokenInSeconds"]
a_regen = data["player"]["progress"]["arena"]["tokens"]["regenDelayInSeconds"]
	
o_tokens = data["player"]["progress"]["onslaught"]["tokens"]["current"]
o_tokens_max = data["player"]["progress"]["onslaught"]["tokens"]["max"]
o_next = data["player"]["progress"]["onslaught"]["tokens"]["nextTokenInSeconds"]	
o_regen = data["player"]["progress"]["onslaught"]["tokens"]["regenDelayInSeconds"]
	
r_tokens = data["player"]["progress"]["guildRaid"]["tokens"]["current"]
r_tokens_max = data["player"]["progress"]["guildRaid"]["tokens"]["max"]
r_next = data["player"]["progress"]["guildRaid"]["tokens"]["nextTokenInSeconds"]
r_regen = data["player"]["progress"]["guildRaid"]["tokens"]["regenDelayInSeconds"]
	
s_tokens = data["player"]["progress"]["salvageRun"]["tokens"]["current"]
s_tokens_max = data["player"]["progress"]["salvageRun"]["tokens"]["max"]
s_next = data["player"]["progress"]["salvageRun"]["tokens"]["nextTokenInSeconds"]
s_regen = data["player"]["progress"]["salvageRun"]["tokens"]["regenDelayInSeconds"]

print("Arena")	
a_date = date_when_cap(int(a_tokens), int(a_tokens_max), int(a_next), int(a_regen))	
print("Onslaught")
o_date = date_when_cap(int(o_tokens), int(o_tokens_max), int(o_next), int(o_regen))
print("Raid")
r_date = date_when_cap(int(r_tokens), int(r_tokens_max), int(r_next), int(r_regen))	
print("Salvage")
s_date = date_when_cap(int(s_tokens), int(s_tokens_max), int(s_next), int(s_regen))	

print("Arena max date: " + a_date.strftime("%c"))
print("Onslaught max date: " + o_date.strftime("%c"))
print("Salvage max date: " + s_date.strftime("%c"))
print("Raid max date: " + r_date.strftime("%c"))

#end_date_string = input("Enter the end date (20251213 1900):")
end_date_string = "20260104 0400"
end_date_year = int(end_date_string[0:4])
end_date_month = int(end_date_string[4:6])
end_date_day = int(end_date_string[6:8])
end_date_hour = int(end_date_string[9:11])
end_date_minute = int(end_date_string[11:13])
end_date = datetime(end_date_year, end_date_month, end_date_day, hour=end_date_hour, minute=end_date_minute)

print("----\n")
a_end_stock, a_end_next_stock, a_total_seconds = stock_at_date(int(a_tokens), int(a_next), int(a_regen), end_date)
o_end_stock, o_end_next_stock, o_total_seconds = stock_at_date(int(o_tokens), int(o_next), int(o_regen), end_date)
r_end_stock, r_end_next_stock, r_total_seconds = stock_at_date(int(r_tokens), int(r_next), int(r_regen), end_date)
s_end_stock, s_end_next_stock, s_total_seconds = stock_at_date(int(s_tokens), int(s_next), int(s_regen), end_date)


print("Current datetime: " + datetime.now().strftime("%c"))
print("End datetime: " + end_date.strftime("%c"))
print("Total seconds between now and enddate: " + str(a_total_seconds))
print("Arena at end datetime (ignore cap): " + str(a_end_stock))
print("Time to next stock (seconds): " + str(a_end_next_stock)) 
print("Onslaught at end datetime (ignore cap): " + str(o_end_stock))
print("Time to next stock (seconds): " + str(o_end_next_stock)) 
print("Guild raid at end datetime (ignore cap): " + str(r_end_stock))
print("Time to next stock (seconds): " + str(r_end_next_stock)) 
print("Salvage run at end datetime (ignore cap): " + str(s_end_stock))
print("Time to next stock (seconds): " + str(s_end_next_stock)) 
		
        
with open('player_data.json', 'w') as file:
    json.dump(data, file, indent=4)