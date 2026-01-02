import json
import os
patchVersion = "135"
fName = patchVersion + "-LegendaryReleaseEvent-Formatted.json"
with open('lr_event.json', 'r') as file:
    lre_dat = json.load(file)

with open('units.json', 'r') as file:
    units = json.load(file)

with open('npcs.json', 'r') as file:
    npc_dat = json.load(file)
    
with open('common_values.json', 'r') as file:
    common_values = json.load(file)




lreFormatted = {}
lreFormatted["Expired"] = {}
lreFormatted["Active"] = {}
def formatLegendaryReleaseEvent():
    for event in lre_dat:
        if lre_dat[event]["trackingEventNumber"] = 3:
            unitName = units[lre_dat[event]["trackingFeaturedHero"]]["name"]
            lreFormatted["Expired"][unitName] = lre_dat[event]
        else:
            unitName = units[lre_dat[event]["trackingFeaturedHero"]]["name"]
            lreFormatted["Active"][unitName] = lre_dat[event]
    

formatLegendaryReleaseEvent()   
with open(fName, 'w') as w:
    json.dump(lreFormatted, w, indent=4)
lre_13 = {}
for track in lre_dat:
    print(track)
    enemy = {}
    wave_enemy = {}
    round_num = 0
    for lre_round in lre_dat[track]:
        print(lre_round)
        enemy_count = 0
        round_num += 1
        wave_list = []
        for wave in lre_round["waves"]:
            enemy_count += len(wave["army"])
            wave_list.append(wave["army"])
        enemy[round_num] = enemy_count
        wave_enemy[round_num] = wave_list
    if track == "legendary_event_13_lane_1":
        if not "alpha" in lre_13:
            lre_13["alpha"] = {}
        lre_13["alpha"]["count"] = enemy
        lre_13["alpha"]["enemy_list"] = wave_enemy
    if track == "legendary_event_13_lane_2":
        if not "beta" in lre_13:
            lre_13["beta"] = {}
        lre_13["beta"]["count"] = enemy
        lre_13["beta"]["enemy_list"] = wave_enemy
    if track == "legendary_event_13_lane_3":
        if not "gamma" in lre_13:
            lre_13["gamma"] = {}
        lre_13["gamma"]["count"] = enemy
        lre_13["gamma"]["enemy_list"] = wave_enemy
    
print("Alpha: " + str(lre_13["alpha"]))
print("Beta: " + str(lre_13["beta"]))
print("Gamma: " + str(lre_13["gamma"]))
points = {}
track_points = {}

def unit_check(ed):
    new_ed = {}
    for npc in ed:
        if npc == "enemy_count": continue
        new_ed[npc_dat[npc]["name"]] = []
        for stat in ed[npc]:
            npc_dict = {}
            npc_stat = {}
            #rank
            npc_stat["Rank"] = common_values["Ranks"][str(npc_dat[npc]["stats"][int(stat) - 1]["Rank"])]
            #stars
            npc_stat["Stars"] = common_values["Stars"][str(npc_dat[npc]["stats"][int(stat) - 1]["StarLevel"])]
            #damage
            npc_stat["Damage"] = npc_dat[npc]["stats"][int(stat) - 1]["Damage"]
            #health
            npc_stat["Health"] = npc_dat[npc]["stats"][int(stat) - 1]["Health"]
            #armor
            npc_stat["Armor"] = npc_dat[npc]["stats"][int(stat) - 1]["FixedArmor"]
            npc_dict["Count"] = ed[npc][stat]
            npc_dict["Stats"] = npc_stat
            #print(stat)
            #print(ed[npc][stat])
            #print(npc_stat)
            #print(npc_dict)
            new_ed[npc_dat[npc]["name"]].append(npc_dict)
    return new_ed

for i in range (7,15):
    track_points[i] = (lre_13["alpha"]["count"][i])*2 + 34 + 70
points["alpha"] = track_points
track_points = {}

for i in range(9,14):
    track_points[i] = (lre_13["beta"]["count"][i])*2 + 26 + 65
points["beta"] = track_points
track_points = {}
for i in range(7,14):
    track_points[i] = (lre_13["gamma"]["count"][i])*2 + 17 + 105
points["gamma"] = track_points

for track in points:
    print(track)
    sum_point = 0
    for p in points[track]:
        print(str(p) + ":" + str(points[track][p]))
        sum_point += points[track][p]
    print(track + " total: " + str(sum_point))
    
os.system('cls')    
print(lre_13["alpha"]["enemy_list"][1])
lre_dict = {}

for track in lre_13:
    lre_dict[track] = {}
    for round_num in lre_13[track]["enemy_list"]:
        enemy_dict = {}
        enemy_count = 0
        for wave in lre_13[track]["enemy_list"][round_num]:
            for enemy in wave:
                splitter = enemy.split(":")
                enemy_name = splitter[0]
                enemy_data = splitter[1]
                if not enemy_name in enemy_dict:
                    enemy_dict[enemy_name] = {}
                if not enemy_data in enemy_dict[enemy_name]:
                    enemy_dict[enemy_name][enemy_data] = 1
                    enemy_count += 1
                else:
                    enemy_dict[enemy_name][enemy_data] += 1
                    enemy_count += 1
            enemy_dict["enemy_count"] = enemy_count
        lre_dict[track][round_num] = enemy_dict
    
#print(enemy_dict)
#unit_check(enemy_dict)
formatted_lre_dict = {}
for track in lre_dict:
    formatted_lre_dict[track] = {}
    for round_num in lre_dict[track]:
        formatted_lre_dict[track][round_num] = unit_check(lre_dict[track][round_num])
        
with open('lre_13_waves_formatted.json', 'w') as w:
    json.dump(formatted_lre_dict, w, indent=4)