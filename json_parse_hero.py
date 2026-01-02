import json
patchVersion = "135"
fName = patchVersion + "-LinearHeroEvent-Formatted.json"
with open('hero_events.json', 'r') as file:
    heroEvent_dat = json.load(file)
with open('npcs.json', 'r') as file:
    npc_dat = json.load(file)
with open('units.json', 'r') as file:
    unit_dat = json.load(file)
with open('chests.json', 'r') as file:
    chests_dat = json.load(file)
with open('common_values.json', 'r') as file:
    common_values = json.load(file)

dataToTake = ["eventType", "eventName", "trackingAdditionalData", "trackingFeaturedFaction", "trackingFeaturedHero", "unitId", "maxStamina", "staminaRegenerationTime", "staminaRegenerationAmount", "staminaRefillGemsCost", "tiers", "milestones", "offerBundleBonus", "allowedFactions", "scorePoints"]
battleDataToTake = ["spawnpoints", "deployedUnit", "lightningVictory", "loot", "enemies", "Objectives"]      
tier_list = {"0": "Common", "1": "Uncommon", "2": "Rare", "3": "Epic", "4": "Legendary", "5": "Mythic"}        
tier_num = 0

def listEnemyLinearHeroEvent(battle):
    battleFormatted = {}
    for bd in battleDataToTake:
        if bd == "spawnpoints":
            battleFormatted["unitsDeployed"] = battle[bd]
        elif bd == "enemies":
            enemyCount = len(battle[bd])
            enemyList = {}
            enemyCounts = {}
            for enemy in battle[bd]:
                if "powup" in enemy:
                    enemyCount += -1
                    continue
                enemySplit = enemy.split(":")
                enemyId = enemySplit[0]
                enemyData = enemySplit[1]
                enemyName = npc_dat[enemyId]["name"]
                if not enemyName in enemyCounts: 
                    enemyCounts[enemyName] = 1
                    enemyList[enemyName] = {}
                else: enemyCounts[enemyName] += 1
                if not enemyData in enemyList[enemyName]:
                    enemyList[enemyName][enemyData] = {}
                    enemyList[enemyName][enemyData]["Count"] = 1
                    enemyList[enemyName][enemyData]["Stats"] = {}
                    enemyList[enemyName][enemyData]["Rank"] = common_values["Ranks"][str(npc_dat[enemyId]["stats"][int(enemyData) -1]["Rank"])]
                    enemyList[enemyName][enemyData]["Stars"] = common_values["Stars"][str(npc_dat[enemyId]["stats"][int(enemyData) -1]["StarLevel"])]
                    enemyList[enemyName][enemyData]["Stats"]["Damage"] = npc_dat[enemyId]["stats"][int(enemyData) -1]["Damage"]
                    enemyList[enemyName][enemyData]["Stats"]["Health"] = npc_dat[enemyId]["stats"][int(enemyData) -1]["Health"]
                    if not "FixedArmor" in npc_dat[enemyId]["stats"][int(enemyData) -1]: enemyList[enemyName][enemyData]["Stats"]["Armor"] = 0
                    else: enemyList[enemyName][enemyData]["Stats"]["Armor"] = npc_dat[enemyId]["stats"][int(enemyData) -1]["FixedArmor"]
                else:
                    enemyList[enemyName][enemyData]["Count"] += 1 
                
            battleFormatted["enemyCounts"] = enemyCounts
            battleFormatted["enemyData"] = enemyList
        else:    
            battleFormatted[bd] = battle[bd]
    return battleFormatted, enemyCount

def formatLinearHeroEvent():
    lheFormatted = {}
    for lhe in heroEvent_dat:
        uName = heroEvent_dat[lhe]["unitId"]
        if uName in unit_dat:
            lheName = unit_dat[uName]["name"] + " Quest"
        else:
            lheName = npc_dat[uName]["name"] + " Quest"
        lheFormatted[lheName] = {}
        for d in dataToTake:
            if d == "tiers":
                lheFormatted[lheName][d] = {}
                for t in heroEvent_dat[lhe][d]:
                    tier_name = tier_list[str(t["index"])]
                    lheFormatted[lheName][d][tier_name] = {}
                    bnum = 0
                    for b in t["battles"]:
                        bnum += 1
                        bf, ec = listEnemyLinearHeroEvent(b)
                        lheFormatted[lheName][d][tier_name][str(bnum)] = {}
                        lheFormatted[lheName][d][tier_name][str(bnum)]["enemyCount"] = ec
                        for bf_dict in bf:
                            lheFormatted[lheName][d][tier_name][str(bnum)][bf_dict] = bf[bf_dict]
                        
            elif d == "milestones":
                lheFormatted[lheName][d] = {}
                for m in heroEvent_dat[lhe][d]:
                    lheFormatted[lheName][d][str(m["scorePoints"])] = chests_dat[m["chestId"]][0]["rewards"]
            else:
                lheFormatted[lheName][d] = heroEvent_dat[lhe][d]
    with open(fName, 'w') as w:
        json.dump(lheFormatted, w, indent=4)     

formatLinearHeroEvent()
enemy_list = {}


for tiers in heroEvent_dat[1]["tiers"]:
    battle_num = 1
    enemy_list[tier_list[str(tier_num)]] = {}
    for battle in tiers["battles"]:
        enemy_list[tier_list[str(tier_num)]][battle_num] = battle["enemies"]
        battle_num += 1
    tier_num += 1    
#print(enemy_list)

enemy_dict = {}
for t in enemy_list:
    enemy_dict[t] = {}
    for b in enemy_list[t]:
        e_list = {}
        for enemy in enemy_list[t][b]:
            enemy_split = enemy.split(":")
            enemy_name_lookup = enemy_split[0]
            if "powup" in enemy_name_lookup:
                continue
            enemy_name = npc_dat[enemy_name_lookup]["name"]
            enemy_rank = enemy_split[1]
            if enemy_name in e_list:
                e_list[enemy_name] += 1
            else:
                e_list[enemy_name] = 1
        enemy_dict[t][b] = e_list
        
with open(fName, 'w') as w:
    json.dump(lheFormatted, w, indent=4) 
 
print(enemy_dict)
squig_list = {}
#for t in enemy_dict:
#    for b in enemy_dict[t]:
 #       for e in enemy_dict[t][b]:
 #           if e == "orksNpc7Squig"