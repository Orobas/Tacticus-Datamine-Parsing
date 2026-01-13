import json
patchVersion = "135"
fName = patchVersion + "-MechEnemies-Formatted.json"
with open('units.json', 'r') as file:
    unit_dat = json.load(file)
with open('upgrades.json', 'r') as file:
    upgrades_dat = json.load(file)
with open('hs_reward.json', 'r') as file:
    hs_reward = json.load(file)

sw_reward = hs_reward["faction_boost_space_wolves_tier_high"]["reward"]

upgrade_list = {}
upgrade_list_raw = {}    
for i in range(0,15):
    u_list = []
    u_list_raw = []
    for u in unit_dat["spaceWolfPriest"]["upgrades"][i]:
        u_list.append(upgrades_dat[u]["name"])
        u_list_raw.append(u)
    upgrade_list[i] = u_list
    upgrade_list_raw[i] = u_list_raw
  
print(upgrade_list)
sw_upgrade_reward = []
sw_upgrade_reward_raw = []
for reward in sw_reward:
    if "upg" in reward["chestRewardId"]:
        sw_upgrade_reward.append(upgrades_dat[reward["chestRewardId"]]["name"])
        sw_upgrade_reward_raw.append(reward["chestRewardId"])
print(sw_upgrade_reward)

upgrade_dict = {}
upgrade_dict_raw = {}

for rank in upgrade_list_raw:
    for upgrade in upgrade_list_raw[rank]:
        if not upgrade in upgrade_dict_raw:
            upgrade_dict_raw[upgrade] = 1
        else:
            upgrade_dict_raw[upgrade] += 1
print(upgrade_dict_raw)

def unpack(upgrades, count):
    unpack_dict = {}
    for craft in upgrades_dat[upgrades]["crafting"]:
        if "crafting" in upgrades_dat[craft["id"]]:
            unpack_dict[craft["id"]] = unpack(craft["id"], craft["amount"] * count)
        else:
            unpack_dict[craft["id"]] = craft["amount"] * count
    return unpack_dict

upgrade_dict_raw_crafts = {}
upgrade_dict_raw_minus = {}
rewards_removed = []
for u in upgrade_dict_raw:
    if not u in sw_upgrade_reward_raw:
        upgrade_dict_raw_minus[u] = upgrade_dict_raw[u]
    else:
        if upgrade_dict_raw[u] > 1:
            upgrade_dict_raw_minus[u] = upgrade_dict_raw[u] - 1
        rewards_removed.append(u)
            

            

for upgrade in upgrade_dict_raw:
    if "crafting" in upgrades_dat[upgrade]:
        upgrade_dict_raw_crafts[upgrade] = unpack(upgrade, upgrade_dict_raw[upgrade])
    else:
        upgrade_dict_raw_crafts[upgrade] = upgrade_dict_raw[upgrade]

reward_crafts = {}
for reward_upgrade in sw_upgrade_reward_raw:
    if "crafting" in upgrades_dat[reward_upgrade]:
        reward_crafts[reward_upgrade] = unpack(reward_upgrade, 1)
    else:
        reward_crafts[reward_upgrade] = reward_upgrade

full_raw_list = {}
full_reward_list = {}
def unpack_count(upgrade):
    for u in upgrade:
        if isinstance(upgrade[u], dict):
            unpack_count(upgrade[u])
        else:
            if not u in full_raw_list:
                full_raw_list[u] = 0
            full_raw_list[u] += upgrade[u]

def unpack_count_reward(rewards):
    for r in rewards:
        if isinstance(rewards[r], dict):
            unpack_count_reward(rewards[r])
        else:
            if not r in full_reward_list:
                full_reward_list[r] = 0
            full_reward_list[r] += rewards[r]
            
unpack_count(upgrade_dict_raw_crafts)
unpack_count_reward(reward_crafts)
full_list = {}
full_reward = {}
for raw in full_raw_list:
    full_list[upgrades_dat[raw]["name"]] = full_raw_list[raw]

for reward_raw in full_reward_list:
    full_reward[upgrades_dat[reward_raw]["name"]] = full_reward_list[reward_raw]

print("UPGRADE LIST")
print(upgrade_list)
print("FULL:")
print(full_list)
print("Reward craft")
print(reward_crafts)
print("FULL REWARD:")
print(full_reward)

full_minus_reward = {}
for reward_c in full_reward:
    if reward_c in full_list:
        full_list[reward_c] += -full_reward[reward_c]

print("FULL AFTER REWARD")
for u in full_list:
    print(u + ": " + str(full_list[u]))
'''
for upgrade in upgrade_dict_raw_crafts:
    if isinstance(upgrade_dict_raw_crafts[upgrade], dict):
        unpacked_dict = unpack_count(upgrade_dict_raw_crafts[upgrade])
    else:
        if not upgrade in full_raw_list:
            full_raw_list[upgrade] = 0
        full_raw_list[upgrade] += upgrade_dict_raw_crafts[upgrade]
print(upgrade_dict_raw_crafts)
'''

