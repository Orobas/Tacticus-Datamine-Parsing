import json
import compareData
with open('Version_1_35_2\\RawData\\units_player.json', 'r') as file:
    newDat = json.load(file)
with open('Version_1_35\\RawData\\units_player.json', 'r') as file:
    oldDat = json.load(file)
with open('135units.json', 'r') as file:
    newUDat = json.load(file)
with open('134units.json', 'r') as file:
    oldUDat = json.load(file)
changes = {}
changes = compareData.compareTwo(oldDat, newDat)
with open("compare.json", 'w') as writeFile:
    json.dump(changes, writeFile, indent = 4)