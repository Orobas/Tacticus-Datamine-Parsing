import json
import os
import compareData
#Datamine real files

#Parse into base files unformatted

#load gameconfig
version = "1_35_2"
all_dir = os.listdir('.')
versionList = []
for entry in all_dir:
    if os.path.isdir(os.path.join('.', entry)):
        if "Version" in entry and entry != "Version_" + version:
            versionList.append(entry)
        
if len(versionList) > 0:    
    lastVersion = versionList[-1]
else:
    lastVersion = "None"
try:
    os.mkdir("Version_" + version)
except FileExistsError:
    pass

try:
    os.mkdir("Version_" + version + "\\RawData")
except FileExistsError:
    pass

with open('gameconfig_' + version + '.json', 'r') as gameconfig:
    gameConfigDat = json.load(gameconfig)

print("Version_" + version)

def saveFile(fName, fData):
    with open('Version_' + version + '\\' + fName + '.json', 'w') as writeFile:
        json.dump(fData, writeFile, indent=4)

def compileData(rootData, keyList):
    dataDict = {}
    for key in keyList:
        dataDict[key] = rootData[key]
    return dataDict

def compileDataConditional(rootData, conditional):
    dataDictConditional = {}
    for data in rootData:
        if conditional in data:
            dataDictConditional[data] = rootData[data]
    return dataDictConditional
    
#Player data
saveFile("RawData\\player", gameConfigDat["clientGameConfig"]["player"])

#Loot data
saveFile("RawData\\loot", gameConfigDat["clientGameConfig"]["loot"])

#Loot-tieredProgressRewards data
saveFile("RawData\\loot_tieredProgressRewards", gameConfigDat["clientGameConfig"]["loot"]["tieredProgressRewards"])

#Loot-dropTables data
saveFile("RawData\\loot_dropTables", gameConfigDat["clientGameConfig"]["loot"]["dropTables"])

#Loot-chests data
saveFile("RawData\\loot_chests", gameConfigDat["clientGameConfig"]["loot"]["chests"])

#Units data
saveFile("RawData\\units", gameConfigDat["clientGameConfig"]["units"])

#Units-hero data (Player characters)
dataList = ["lineup", "factions", "abilities", "abilityUpgradeCosts", "abilityUpgradeCostsMoW", "heroProgressionSteps", "heroConversion", "heroProgressionStepsMoW", "heroConversionMoW", "xpLevels", "upgradeSlots", "abilityPowerCurve"]
dataPlayer = compileData(gameConfigDat["clientGameConfig"]["units"], dataList)
saveFile("RawData\\units_player", dataPlayer)

#Units-npc data
saveFile("RawData\\units_npc", gameConfigDat["clientGameConfig"]["units"]["npc"])

#Units-damage data
saveFile("RawData\\units_damage", gameConfigDat["clientGameConfig"]["units"]["damageProfiles"])

#Units-summons
saveFile("RawData\\units_summons", gameConfigDat["clientGameConfig"]["units"]["summons"])

#Battles data
saveFile("RawData\\battles", gameConfigDat["clientGameConfig"]["battles"])

#Battles-waves (Onslaught) data
saveFile("RawData\\battles_onslaught", gameConfigDat["clientGameConfig"]["battles"]["waves"])

#Battles-battlesets (LRE waves) data
dataLREWaves = compileDataConditional(gameConfigDat["clientGameConfig"]["battles"]["battleSets"], "legendary_event_")
saveFile("RawData\\battles_lre", dataLREWaves)

#Battles-battlesets (Survival waves) data
dataSurvivalWaves = compileDataConditional(gameConfigDat["clientGameConfig"]["battles"]["battleSets"], "survival_")
saveFile("RawData\\battle_survival", dataSurvivalWaves)

#Battles-campaign data
saveFile("RawData\\battle_campaign", gameConfigDat["clientGameConfig"]["battles"]["campaigns"])

#Battles-treasureBeach (Salvage Run) data
saveFile("RawData\\battle_salvagerun", gameConfigDat["clientGameConfig"]["battles"]["treasureBeach"])

#GlobalValues data
saveFile("RawData\\globalvalues", gameConfigDat["clientGameConfig"]["globalValues"])

#Quests data
saveFile("RawData\\quests", gameConfigDat["clientGameConfig"]["quests"])

#Shop data
saveFile("RawData\\shop", gameConfigDat["clientGameConfig"]["shop"])

#Shop-realMoneyProducts data
saveFile("RawData\\shop_realmoneyproducts", gameConfigDat["clientGameConfig"]["shop"]["realMoneyProducts"])

#Shop-products data
saveFile("RawData\\shop_products", gameConfigDat["clientGameConfig"]["shop"]["products"])

#Shop-offers data
saveFile("RawData\\shop_offers", gameConfigDat["clientGameConfig"]["shop"]["offers"])

#OnlineFeatures data
saveFile("RawData\\onlinefeatures", gameConfigDat["clientGameConfig"]["onlineFeatures"])

#Views data
saveFile("RawData\\views", gameConfigDat["clientGameConfig"]["views"])

#Filters data
saveFile("RawData\\filters", gameConfigDat["clientGameConfig"]["filters"])

#Upgrades data
saveFile("RawData\\upgrades", gameConfigDat["clientGameConfig"]["upgrades"])

#Avatars data
saveFile("RawData\\avatars", gameConfigDat["clientGameConfig"]["avatars"])

#Dialogues data
saveFile("RawData\\dialogues", gameConfigDat["clientGameConfig"]["dialogues"])

#BoardsToInclude data
saveFile("RawData\\boardsToInclude", gameConfigDat["clientGameConfig"]["boardsToInclude"])

#Items data
saveFile("RawData\\items", gameConfigDat["clientGameConfig"]["items"])

#Achievements data
saveFile("RawData\\achievements", gameConfigDat["clientGameConfig"]["achievements"])

#AIUtilities data
saveFile("RawData\\aiutilities", gameConfigDat["clientGameConfig"]["aiUtilities"])

#Leaderboards data
saveFile("RawData\\leaderboards", gameConfigDat["clientGameConfig"]["leaderboards"])

#SummoningPortal data
saveFile("RawData\\summoningportal", gameConfigDat["clientGameConfig"]["summoningPortal"])

#Loyalty data
saveFile("RawData\\loyalty", gameConfigDat["clientGameConfig"]["loyalty"])

#Subscriptions data
saveFile("RawData\\subscriptions", gameConfigDat["clientGameConfig"]["subscriptions"])

#Consumables data
saveFile("RawData\\consumables", gameConfigDat["clientGameConfig"]["consumables"])

#ItemStatCapMultipliers data
saveFile("RawData\\itemstatcapmultipliers", gameConfigDat["clientGameConfig"]["itemStatCapMultipliers"])

#FeatureIntros data
saveFile("RawData\\featureintros", gameConfigDat["clientGameConfig"]["featureIntros"])

#ItemsConfigs data
saveFile("RawData\\itemConfigs", gameConfigDat["clientGameConfig"]["itemsConfig"])

#LiveEvents data
saveFile("RawData\\liveevents", gameConfigDat["clientGameConfig"]["liveEvents"])

#Tips data
saveFile("RawData\\tips", gameConfigDat["clientGameConfig"]["tips"])

#Guilds data
saveFile("RawData\\guilds", gameConfigDat["clientGameConfig"]["guilds"])

#TimedReminders data
saveFile("RawData\\timedreminders", gameConfigDat["clientGameConfig"]["timedReminders"])

#DefeatTips data
saveFile("RawData\\defeattips", gameConfigDat["clientGameConfig"]["defeatTips"])

#ResourceCrafting data
saveFile("RawData\\resourcecrafting", gameConfigDat["clientGameConfig"]["resourceCrafting"])

#ResourceCrafting-AscensionOrbs
dataAscensionOrbs = compileDataConditional(gameConfigDat["clientGameConfig"]["resourceCrafting"]["recipes"], "heroAscensionOrb")
saveFile("RawData\\resoucecrafting_ascensionorbs", dataAscensionOrbs)

#ResourceCrafting-AbilityTokens
dataAbilityTokens = compileDataConditional(gameConfigDat["clientGameConfig"]["resourceCrafting"]["recipes"], "abilityToken")
saveFile("RawData\\resoucecrafting_abilitytokens", dataAbilityTokens)

#ResourceCrafting-ItemAscension
dataItemAscension = compileDataConditional(gameConfigDat["clientGameConfig"]["resourceCrafting"]["recipes"], "itemAscension")
saveFile("RawData\\resoucecrafting_itemascension", dataItemAscension)

#Compare to last version
def compare():
    if not lastVersion == "None":
        lastRawData = os.path.join(lastVersion, 'RawData')
        latestRawData = os.path.join('Version_' + version, 'RawData')
        if os.path.isdir(lastRawData):
            for file in os.listdir(latestRawData):
                filePath = os.path.join(latestRawData, file)
                if os.path.isfile(filePath):
                    oldFileExist = False
                    if os.path.exists(lastRawData + "\\" + file):      
                        with open(lastRawData + "\\" + file, 'r') as oldFile:
                            oldFileData = json.load(oldFile)
                            oldFileExist = True
                    else:
                        print(lastRawData + "\\" + file + " does not exist")
                    with open(latestRawData + "\\" + file, 'r') as newFile:
                        newFileData = json.load(newFile)
                    if oldFileExist:
                        changesData = compareData.compareTwo(oldFileData, newFileData)
                    else:
                        changesData = {}
                        changesData["added"] = newFileData
                    try:
                        os.mkdir("Version_" + version + "\\Changes")
                    except FileExistsError:
                        pass
                    if len(changesData) > 0:
                        print(file + " - changes")
                        with open("Version_" + version + "\\Changes\\" + file, 'w') as changesFile:
                            json.dump(changesData, changesFile, indent=4)
                    else:
                        print(file + " - no changes")
    else:
        print("No old version to compare")

compare()