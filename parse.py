import json
with open('gameconfig_1_35.json', 'r') as file:
        dat = json.load(file)
        
HSEvents = {}
warpsurge = []
squigsmash = []
mowEvent = []
battlePass = {}
heroEvents = {}
shop = {}
chests = {}
for event in dat["clientGameConfig"]["liveEvents"]["idunLiveEventConfigs"]:
    if event["eventType"] == "homeScreenEvent":
        tierSplit = event["eventName"].split("_tier_")
        if not tierSplit[0] in HSEvents:
            HSEvents[tierSplit[0]] = {}
        if len(tierSplit) > 1:
            HSEvents[tierSplit[0]][tierSplit[1]] = event
        else:
            HSEvents[tierSplit[0]]["one"] = event
        if event["eventName"] == "squig_smash_tier_high":
            squigsmash.append(event)
        if event["eventName"] == "warp_surge_tier_high":
            warpsurge.append(event)
    if event["eventType"] == "mowEvent":
        mowEvent.append(event)
    if event["eventType"] == "linearHeroEvent":
        heroEvents[event["eventName"]] = event
shop["productViewConfigs"] = {}
for pvc in dat["clientGameConfig"]["shop"]["productViewConfigs"]:
    shop["productViewConfigs"][pvc] = dat["clientGameConfig"]["shop"]["productViewConfigs"][pvc]

shop["realMoneyProducts"] = {}    
for rmp in dat["clientGameConfig"]["shop"]["realMoneyProducts"]:
    shop["realMoneyProducts"][rmp] = dat["clientGameConfig"]["shop"]["realMoneyProducts"][rmp]

shop["offers"] = {}
for offer in dat["clientGameConfig"]["shop"]["offers"]:
    shop["offers"][offer["offerId"]] = offer

for ch in dat["clientGameConfig"]["loot"]["chests"]:
    chests = dat["clientGameConfig"]["loot"]["chests"]

tpr = dat["clientGameConfig"]["loot"]["tieredProgressRewards"]
for loot in tpr:
    loot_split = loot.split('_')
    loot_n = "_".join(loot_split[:-1])
    loot_p = loot_split[-1]
    if loot_n != "battle_pass_bp_starter":
        if loot_p == "premium":
            if loot_split[-2] == "extra":
                loot_p = loot_split[-2] + "_" + loot_p 
                loot_n = loot_n[:-6]
        if "battle_pass" in loot:
            if not loot_n in battlePass:
                battlePass[loot_n] = {}
            battlePass[loot_n][loot_p] = tpr[loot]  
            

lre_data = {}
lre_data["data"] = {}
for event in dat["clientGameConfig"]["liveEvents"]["idunLiveEventConfigs"]:
    print(event["eventType"])
    if event["eventType"] == "legendaryHeroEvent":
        lre_data["data"][event["eventName"]] = event
print(lre_data)

        
lre_waves = {}
for battleset in dat["clientGameConfig"]["battles"]["battleSets"]:
    if "legendary_event" in battleset:
        legendarySplit = battleset.split("_lane_")
        if not legendarySplit[0] in lre_waves: lre_waves[legendarySplit[0]] = {}
        if legendarySplit[1] == "1":
            lre_waves[legendarySplit[0]]["Alpha"] = dat["clientGameConfig"]["battles"]["battleSets"][battleset] 
        elif legendarySplit[1] == "2":
            lre_waves[legendarySplit[0]]["Beta"] = dat["clientGameConfig"]["battles"]["battleSets"][battleset]  
        elif legendarySplit[1] == "3":
            lre_waves[legendarySplit[0]]["Gamma"] = dat["clientGameConfig"]["battles"]["battleSets"][battleset] 
lre_data["waves"] = lre_waves              
            
campaign_data = dat["clientGameConfig"]["battles"]["campaigns"]

        
lre_13 = {}
lre_13["legendary_event_13_lane_1"] = dat["clientGameConfig"]["battles"]["battleSets"]["legendary_event_13_lane_1"]
lre_13["legendary_event_13_lane_2"] = dat["clientGameConfig"]["battles"]["battleSets"]["legendary_event_13_lane_2"]
lre_13["legendary_event_13_lane_3"] = dat["clientGameConfig"]["battles"]["battleSets"]["legendary_event_13_lane_3"]

with open('units.json', 'w') as w:
    json.dump(dat["clientGameConfig"]["units"]["lineup"], w, indent=4)

with open('upgrades.json', 'w') as w:
    json.dump(dat["clientGameConfig"]["upgrades"], w, indent=4)

with open('live_events.json', 'w') as w:
    json.dump(dat["clientGameConfig"]["liveEvents"]["idunLiveEventConfigs"], w, indent=4)
    
with open('hs_events.json', 'w') as w:
    json.dump(HSEvents, w, indent=4)

with open('tiered_rewards.json', 'w') as w:
    json.dump(dat["clientGameConfig"]["loot"]["tieredProgressRewards"], w, indent=4)
    
with open('warp_surge.json', 'w') as w:
    json.dump(warpsurge, w, indent=4)

with open('squig_smash.json', 'w') as w:
    json.dump(squigsmash, w, indent=4)
    
with open('mow_event.json', 'w') as w:
    json.dump(mowEvent[0], w, indent=4)
    
with open('mow_event_1.json', 'w') as w:
    json.dump(mowEvent[0]["mows"][0]["tiers"][4], w, indent=4)
    
with open('mow_event_2.json', 'w') as w:
    json.dump(mowEvent[0]["mows"][0]["tiers"][5], w, indent=4)
    
with open('battle_pass.json', 'w') as w:
    json.dump(battlePass, w, indent=4)
    
with open('lre_13_waves.json', 'w') as w:
    json.dump(lre_13, w, indent=4)
    
with open('lr_event.json', 'w') as w:
    json.dump(lre_data, w, indent=4)
    
with open('lre_waves.json', 'w') as w:
    json.dump(lre_waves, w, indent=4)
    
with open('npcs.json', 'w') as w:
    json.dump(dat["clientGameConfig"]["units"]["npc"], w, indent=4)
    
with open('hero_events.json', 'w') as w:
    json.dump(heroEvents, w, indent=4)
    
with open('paid_offers.json', 'w') as w:
    json.dump(shop, w, indent=4)
    
with open('chests.json', 'w') as w:
    json.dump(chests, w, indent=4)
    
with open('campaign.json', 'w') as w:
    json.dump(campaign_data, w, indent=4)