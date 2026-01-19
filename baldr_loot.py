import json
from fractions import Fraction
with open('baldr_loot.json', 'r') as file:
    dat = json.load(file)
    
with open('upgrades.json', 'r') as file:
    up_dat = json.load(file)
    
with open('common_values.json', 'r') as file:
    common_dat = json.load(file)
    
with open('units.json', 'r') as file:
    unit_dat = json.load(file)
    
new_dict = {}
for tier in dat:
    if not tier in new_dict: new_dict[tier] = {}
    for battle in dat[tier]:
        new_dict[tier][battle] = {}
        for loot in dat[tier][battle]:
            if "shards" in dat[tier][battle][loot]:
                new_dict[tier][battle][loot] = "Baldr Shard"
            elif loot == "chanceOf":
                up = dat[tier][battle]["chanceOf"]
                upSplit = up.split("%")
                upCode = upSplit[0]
                upPer = upSplit[1]
                upName = up_dat[upCode]["name"]
                upPer = float(Fraction(upPer)) * 100
                new_dict[tier][battle]["chanceOf"] = upName + " " + f"{upPer:.2f}" + "%"
            else:
                new_dict[tier][battle][loot] = common_dat["stringSwap"][dat[tier][battle][loot]]
                
print(new_dict)
with open ('temp_output.json', 'w') as file:
    for tier in new_dict:
        for battle in new_dict[tier]:
            file.write(tier + " " + battle + ":\n")
            for loot in new_dict[tier][battle]:
                file.write("\t" + loot + ": " + new_dict[tier][battle][loot] + "\n")
    
