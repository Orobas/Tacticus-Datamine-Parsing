import json
patchVersion = "135"
fName = patchVersion + "-MechEnemies-Formatted.json"
with open('npcs.json', 'r') as file:
    npcs_dat = json.load(file)
with open('campaign.json', 'r') as file:
    campaign_dat = json.load(file)
with open('common_values.json', 'r') as file:
    common_values = json.load(file)
with open('upgrades.json', 'r') as file:
    upgrades_dat = json.load(file)
    
traitSelected = "Mechanical"
campaign_list = {}
campaign_data_formatted = {}

for campaign_type in campaign_dat:
    for campaign in campaign_dat[campaign_type]:
        campaign_name = common_values["Campaigns"][campaign["id"]]
        campaign_list[campaign_name] = {}
        campaign_data_formatted[campaign_name] = {}
        for battle in campaign["battles"]:
            #print(battle)
            if not "staminaCost" in battle: continue
            campaign_data_formatted[campaign_name][battle["battleId"]] = {}
            enemy_count = 0
            for team in battle["units"]:
                for unit in team:
                    if unit == '': continue
                    if "powup" in unit: continue
                    unit_split = unit.split(":")
                    unit_id = unit_split[0]
                    unit_data = unit_split[1]
                    unit_name = npcs_dat[unit_id]["name"]
                    enemy_count += 1
            if enemy_count > 0:
                if enemy_count not in campaign_list[campaign_name]: 
                    campaign_list[campaign_name][enemy_count] = []
                campaign_list[campaign_name][enemy_count].append(battle["battleId"])
            campaign_data_formatted[campaign_name][battle["battleId"]]["energy"] = battle["staminaCost"]
            campaign_data_formatted[campaign_name][battle["battleId"]]["triesPerDay"] = battle["maxAttempts"]
            if "chanceOf" in battle["loot"]:
                campaign_data_formatted[campaign_name][battle["battleId"]]["reward"] = battle["loot"]["chanceOf"]
            else:
                campaign_data_formatted[campaign_name][battle["battleId"]]["reward"] = "None"
print(campaign_list)
'''

for campaign_type in campaign_dat:
    for campaign in campaign_dat[campaign_type]:
        campaign_name = common_values["Campaigns"][campaign["id"]]
        campaign_list_with_trait[campaign_name] = {}
        campaign_data_formatted[campaign_name] = {}
        for battle in campaign["battles"]:
            #print(battle)
            if not "staminaCost" in battle: continue
            campaign_data_formatted[campaign_name][battle["battleId"]] = {}
            enemy_count_with_trait = 0
            for team in battle["units"]:
                for unit in team:
                    if unit == '': continue
                    if "powup" in unit: continue
                    unit_split = unit.split(":")
                    unit_id = unit_split[0]
                    unit_data = unit_split[1]
                    if not traitSelected in npcs_dat[unit_id]["traits"]: continue
                    unit_name = npcs_dat[unit_id]["name"]
                    enemy_count_with_trait += 1
            if enemy_count_with_trait > 0:
                if enemy_count_with_trait not in campaign_list_with_trait[campaign_name]: 
                    campaign_list_with_trait[campaign_name][enemy_count_with_trait] = []
                campaign_list_with_trait[campaign_name][enemy_count_with_trait].append(battle["battleId"])
            campaign_data_formatted[campaign_name][battle["battleId"]]["energy"] = battle["staminaCost"]
            campaign_data_formatted[campaign_name][battle["battleId"]]["triesPerDay"] = battle["maxAttempts"]
            if "chanceOf" in battle["loot"]:
                campaign_data_formatted[campaign_name][battle["battleId"]]["reward"] = battle["loot"]["chanceOf"]
            else:
                campaign_data_formatted[campaign_name][battle["battleId"]]["reward"] = "None"
#print(campaign_list_with_trait)
#print(campaign_data_formatted)
reformat_campaign_list_with_trait = {}
for campaign in campaign_list_with_trait:
    for enemyNum in campaign_list_with_trait[campaign]:
        #print(enemyNum)
        if not enemyNum in reformat_campaign_list_with_trait:
            reformat_campaign_list_with_trait[enemyNum] = {}
        if not campaign in reformat_campaign_list_with_trait[enemyNum]:
            reformat_campaign_list_with_trait[enemyNum][campaign] = []
        reformat_campaign_list_with_trait[enemyNum][campaign].append(campaign_list_with_trait[campaign][enemyNum])
#print(reformat_campaign_list_with_trait)
sorted_campaign_list_with_trait = dict(sorted(reformat_campaign_list_with_trait.items(), reverse=True))
#print(sorted_campaign_list_with_trait)   
ppt_list = {}
for enemy_count in sorted_campaign_list_with_trait:
    #print(enemy_count)
    for campaign in sorted_campaign_list_with_trait[enemy_count]:
        for battles in sorted_campaign_list_with_trait[enemy_count][campaign]:
            for battle in battles:
                #print(str(campaign) + ": " + str(sorted_campaign_list_with_trait[enemy_count][campaign]))
                ppt = "{:.2f}".format(float(enemy_count)/float(campaign_data_formatted[campaign][battle]["energy"]))
                if not str(ppt) in ppt_list:
                    ppt_list[ppt] = {}
                if not campaign in ppt_list[ppt]:
                    ppt_list[ppt][campaign] = []
                ppt_list[ppt][campaign].append(battle)
#print(ppt_list)
ppt_list_sorted = dict(sorted(ppt_list.items(), reverse=True))
print(ppt_list_sorted)
#maxEnergy = 638
maxEnergy = 638 -180
points_with_empty_rewards = 0
points_with_no_empty_rewards = 0
eER = 0
eNER = 0
mission_list_with_empty_rewards = {}
mission_list_with_no_empty_rewards = {}
mission_ER_number = 0
mission_NER_number = 0
ppt_list_sorted_no_empty_rewards = {}
for ppt in ppt_list_sorted:
    for campaign in ppt_list_sorted[ppt]:
        for battle in ppt_list_sorted[ppt][campaign]:
            if campaign_data_formatted[campaign][battle]["reward"] == "None":
                continue
            else:
                if not ppt in ppt_list_sorted_no_empty_rewards:
                    ppt_list_sorted_no_empty_rewards[ppt] = {}
                if not campaign in ppt_list_sorted_no_empty_rewards[ppt]:
                    ppt_list_sorted_no_empty_rewards[ppt][campaign] = []
                ppt_list_sorted_no_empty_rewards[ppt][campaign].append(battle)

for ppt in ppt_list_sorted:
    for campaign in ppt_list_sorted[ppt]:
        for battle in ppt_list_sorted[ppt][campaign]:
            if campaign_data_formatted[campaign][battle]["reward"] == "None":
                energy = campaign_data_formatted[campaign][battle]["energy"]
                tries = campaign_data_formatted[campaign][battle]["triesPerDay"]
                energyPerDay = energy * tries
                if energyPerDay + eER < maxEnergy:
                    eER += energyPerDay
                    points_with_empty_rewards += round(int(float(ppt)) * energyPerDay)
                    mission_ER_number += 1
                    mission_list_with_empty_rewards[mission_ER_number] = {}
                    mission_list_with_empty_rewards[mission_ER_number]["campaign"] = campaign
                    mission_list_with_empty_rewards[mission_ER_number]["battle"] = battle
                    mission_list_with_empty_rewards[mission_ER_number]["tries"] = tries
                    mission_list_with_empty_rewards[mission_ER_number]["energy"] = energyPerDay
                else:
                    if maxEnergy - eER - energy <= 0:
                        continue
                    else:
                        rTimes = (maxEnergy - eER) // energy
                        newEnergy = energy * rTimes
                        eER += newEnergy
                        points_with_empty_rewards += round(int(float(ppt)) * newEnergy)
                        mission_ER_number += 1
                        mission_list_with_empty_rewards[mission_ER_number] = {}
                        mission_list_with_empty_rewards[mission_ER_number]["campaign"] = campaign
                        mission_list_with_empty_rewards[mission_ER_number]["battle"] = battle
                        mission_list_with_empty_rewards[mission_ER_number]["tries"] = rTimes
                        mission_list_with_empty_rewards[mission_ER_number]["energy"] = newEnergy
            else:
                energy = campaign_data_formatted[campaign][battle]["energy"]
                tries = campaign_data_formatted[campaign][battle]["triesPerDay"]
                energyPerDay = energy * tries
                if energyPerDay + eER < maxEnergy:
                    eER += energyPerDay
                    points_with_empty_rewards += round(int(float(ppt)) * energyPerDay)
                    mission_ER_number += 1
                    mission_list_with_empty_rewards[mission_ER_number] = {}
                    mission_list_with_empty_rewards[mission_ER_number]["campaign"] = campaign
                    mission_list_with_empty_rewards[mission_ER_number]["battle"] = battle
                    mission_list_with_empty_rewards[mission_ER_number]["tries"] = tries
                    mission_list_with_empty_rewards[mission_ER_number]["energy"] = energyPerDay
                else:
                    if not maxEnergy - eER - energy <= 0:
                        rTimes = (maxEnergy - eER) // energy 
                        newEnergy = energy * rTimes
                        eER += newEnergy
                        points_with_empty_rewards += round(int(float(ppt)) * newEnergy)
                        mission_ER_number += 1
                        mission_list_with_empty_rewards[mission_ER_number] = {}
                        mission_list_with_empty_rewards[mission_ER_number]["campaign"] = campaign
                        mission_list_with_empty_rewards[mission_ER_number]["battle"] = battle
                        mission_list_with_empty_rewards[mission_ER_number]["tries"] = rTimes
                        mission_list_with_empty_rewards[mission_ER_number]["energy"] = newEnergy
                if energyPerDay + eNER < maxEnergy:
                    eNER += energyPerDay
                    points_with_no_empty_rewards += round(int(float(ppt)) * energyPerDay)
                    mission_NER_number += 1
                    mission_list_with_no_empty_rewards[mission_NER_number] = {}
                    mission_list_with_no_empty_rewards[mission_NER_number]["campaign"] = campaign
                    mission_list_with_no_empty_rewards[mission_NER_number]["battle"] = battle
                    mission_list_with_no_empty_rewards[mission_NER_number]["tries"] = tries
                    mission_list_with_no_empty_rewards[mission_NER_number]["energy"] = energyPerDay
                else:
                    if maxEnergy - eNER - energy <= 0:
                        continue
                    else:
                        rTimes = (maxEnergy - eNER) // energy
                        newEnergy = energy * rTimes
                        eNER += newEnergy
                        points_with_no_empty_rewards += round(int(float(ppt)) * newEnergy)
                        mission_NER_number += 1
                        mission_list_with_no_empty_rewards[mission_NER_number] = {}
                        mission_list_with_no_empty_rewards[mission_NER_number]["campaign"] = campaign
                        mission_list_with_no_empty_rewards[mission_NER_number]["battle"] = battle
                        mission_list_with_no_empty_rewards[mission_NER_number]["tries"] = rTimes
                        mission_list_with_no_empty_rewards[mission_NER_number]["energy"] = newEnergy
#print(campaign_data_formatted) 
                     
print("Points with empty rewards:" + str(points_with_empty_rewards))
print("Points with no empty rewards:" + str(points_with_no_empty_rewards))
print("Energy with empty rewards:" + str(eER))
print("Energy with no empty rewards:" + str(eNER))
print("Empty reward mission list")
print(mission_list_with_empty_rewards)
print("No Empty reward mission list")
print(mission_list_with_no_empty_rewards)
print("--------------")        
print(ppt_list_sorted_no_empty_rewards)
print(campaign_data_formatted["Indomitus"]["45"])
for missions in ppt_list_sorted_no_empty_rewards["2.00"]["Indomitus"]:
    rewardSplit = campaign_data_formatted["Indomitus"][missions]["reward"].split("%")
    if "shards_" in rewardSplit[0]:
        rewardName = rewardSplit[0]
    else:
        rewardName = upgrades_dat[rewardSplit[0]]["name"]
    print(missions + ": " + rewardName)
'''