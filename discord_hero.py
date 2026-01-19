import json
with open ('135-LinearHeroEvent-Formatted.json', 'r') as file:
    dat = json.load(file)
    
with open('common_values.json', 'r') as file:
    common_values = json.load(file)
    
with open('units.json', 'r') as file:
    units = json.load(file)
    
with open('upgrades.json', 'r') as file:
    upgrades = json.load(file)


def checkString(msg):
    if "shards" in msg:
        msgSplit = msg.split("_")
        unitId = msgSplit[1]
        unitName = units[unitId]["name"]
        return unitName + " shard"
    elif msg in common_values["stringSwap"]:
        return common_values["stringSwap"][msg]
    else:
        return msg
    

def discordWrite(quest):    
    with open('discord_' + quest + '.txt', 'w') as hero_file:
        hero_file.write("```\n")
        hero_file.write(quest + "\n")
        hero_file.write("Allowed Factions:\n")
        for faction in dat[quest]["allowedFactions"]:
            hero_file.write("\t" + faction + "\n")
        hero_file.write("Rewards:\n")
        for tier in dat[quest]["tiers"]:
            if tier == "Rare":
                hero_file.write("```\n")
                hero_file.write("\n")
                hero_file.write("\n")
                hero_file.write("\n```\n")
            if tier == "Legendary":
                hero_file.write("```\n")
                hero_file.write("\n")
                hero_file.write("\n")
                hero_file.write("\n```\n")
            for battle in dat[quest]["tiers"][tier]:
                hero_file.write("\t" + tier + " " + battle + ":\n")
                hero_file.write("\t\tBase: " + str(dat[quest]["tiers"][tier][battle]["loot"]["base"]) + "\n")
                hero_file.write("\t\t1 Star: " + checkString(dat[quest]["tiers"][tier][battle]["loot"]["star1"]) + "\n")
                hero_file.write("\t\t2 Star: " + checkString(dat[quest]["tiers"][tier][battle]["loot"]["star2"]) + "\n")
                hero_file.write("\t\t3 Star: " + checkString(dat[quest]["tiers"][tier][battle]["loot"]["star3"]) + "\n")
                hero_file.write("\t\tChance Of: " + checkString(dat[quest]["tiers"][tier][battle]["loot"]["chanceOf"]) + "\n")
        hero_file.write("```\n")
        hero_file.write("\n")
        hero_file.write("\n")
        hero_file.write("\n```\n")
        hero_file.write("Battle Info:\n")
        for tier in dat[quest]["tiers"]:
            if tier == "Rare":
                hero_file.write("```\n")
                hero_file.write("\n")
                hero_file.write("\n")
                hero_file.write("\n```\n")
            if tier == "Legendary":
                hero_file.write("```\n")
                hero_file.write("\n")
                hero_file.write("\n")
                hero_file.write("\n```\n")
            for battle in dat[quest]["tiers"][tier]:
                hero_file.write("\t" + tier + " " + battle + ":\n")
                hero_file.write("\t\tUnits Deployed: " + str(dat[quest]["tiers"][tier][battle]["unitsDeployed"]) + "\n")
                hero_file.write("\t\tLightning Victory: " + str(dat[quest]["tiers"][tier][battle]["lightningVictory"]) + " turns\n")
                hero_file.write("\t\tObjectives: \n")
                for objective in dat[quest]["tiers"][tier][battle]["Objectives"]:
                    if "objectiveTarget" in objective:
                        hero_file.write("\t\t\t" + objective["ObjectiveType"] + ":" + objective["ObjectiveTarget"] + ", score: " + str(objective["Score"]) + "\n")
                    else:
                        hero_file.write("\t\t\t" + objective["ObjectiveType"] + ", score: " + str(objective["Score"]) + "\n")
                hero_file.write("\t\tEnemy Count: " + str(dat[quest]["tiers"][tier][battle]["enemyCount"]) + "\n")
                hero_file.write("\t\tEnemy List: \n")
                for enemy in dat[quest]["tiers"][tier][battle]["enemyCounts"]:
                    hero_file.write("\t\t\t" + enemy + ": " + str(dat[quest]["tiers"][tier][battle]["enemyCounts"][enemy]) + "\n")
        hero_file.write("```\n")
        hero_file.write("\n")
        hero_file.write("\n")
        hero_file.write("\n```\n")
        hero_file.write("Milestones:\n")
        for milestone in dat[quest]["milestones"]:
            hero_file.write("\t" + milestone + "\n")
            for milestoneThing in dat[quest]["milestones"][milestone]:
                if ":" in milestoneThing:
                    milestoneSplit = milestoneThing.split(":")
                    thing = checkString(milestoneSplit[0])
                    number = milestoneSplit[1]
                    hero_file.write("\t\t" + number + " " + thing + "\n")
                else:
                    hero_file.write("\t\t" + checkString(milestoneThing) + "\n")
        hero_file.write("```\n")
 
discordWrite("Archimatos Quest")
discordWrite("Baldr Quest") 