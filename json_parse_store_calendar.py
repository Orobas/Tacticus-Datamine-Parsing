import json
import os
patchVersion = "135"
fName = patchVersion + "-StoreCalendar-Formatted.json"
with open('shop.json', 'r') as file:
    store_dat = json.load(file)
with open('common_values.json', 'r') as file:
    common_values = json.load(file)
    
calendarList = []
for offer in store_dat["offers"]:
    if "_day_" in offer and not "warhammer_day" in offer and not "closed" in offer and not "expired" in offer:
        calendarList.append(offer)

calendarDict = {}
for c in calendarList:
    event = c.split("_day_")
    day = event[1].split("_")[0]
    after_day = '_'.join(event[1].split("_")[1:])
    if not event[0] in calendarDict:
        calendarDict[event[0]] = {}
    if not day in calendarDict[event[0]]:
        calendarDict[event[0]][day] = []
    calendarDict[event[0]][day].append(after_day)
for d in calendarDict:
    print(d)
    print(calendarDict[d])
    print("\n")