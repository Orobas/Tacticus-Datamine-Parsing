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
with open('upgrades.json', 'r') as file:
    upgrades_dat = json.load(file)

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
        elif bd == "loot":
            battleFormatted[bd] = battle[bd]
            chanceOf = battle[bd]["chanceOf"]
            chanceOfSplit = chanceOf.split("%")
            chanceOfName = upgrades_dat[chanceOfSplit[0]]["name"]
            chanceOfPercent = "{:.2f}".format(int(chanceOfSplit[1].split("/")[0]) / int(chanceOfSplit[1].split("/")[1]) * 100) + "%"
            battleFormatted[bd]["chanceOf"] = chanceOfName + "-" + chanceOfPercent
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
    return(lheFormatted)    

lheFormatted = formatLinearHeroEvent()
with open(fName, 'w') as w:
        json.dump(lheFormatted, w, indent=4)

arch_loot = {}        
for tiers in lheFormatted["Archimatos Quest"]["tiers"]:
    for battle in lheFormatted["Archimatos Quest"]["tiers"][tiers]:
        arch_loot[tiers + " " + battle] = lheFormatted["Archimatos Quest"]["tiers"][tiers][battle]["loot"]["chanceOf"]
for arch in arch_loot:
    print(arch + ":" + arch_loot[arch])