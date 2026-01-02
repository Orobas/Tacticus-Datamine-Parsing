import json
patchVersion = "135"
fName = patchVersion + "-BattlePass-Formatted.json"
with open('battle_pass.json', 'r') as file:
        dat = json.load(file)

with open('units.json', 'r') as unit_file:
    unit_dat = json.load(unit_file)

with open('upgrades.json', 'r') as upgrades_file:
    upgrades_dat = json.load(upgrades_file)

with open('common_values.json', 'r') as swap_file:
    common_values = json.load(swap_file)

def bpRewards(bp):
    rewards = {}
    for reward in bp:
        if reward["chestRewardId"] == '':
            continue
        if ":" in reward["chestRewardId"]:
            reward_split = reward["chestRewardId"].split(":")
            item = reward_split[0]
            num = int(reward_split[1])
            if item in rewards:
                rewards[item] = int(rewards[item]) + num
            else:
                rewards[item] = num
        else:
            if reward["chestRewardId"] in rewards:
                rewards[reward["chestRewardId"]] = int(rewards[reward["chestRewardId"]]) + 1
            else:
                rewards[reward["chestRewardId"]] = 1
    return rewards

def bpLookup(bp_version):
    #print(bp_version)
    bp_copy = {**bp_version}
    for key,val in bp_version.items():
        if key in common_values["stringSwap"]:
            bp_copy[common_values["stringSwap"][key]] = val
            del bp_copy[key]
        if "shards" in key:
            unit = key.split("_")[1]
            unit_name = unit_dat[unit]["name"]
            bp_copy[unit_name + " shards"] = val
            del bp_copy[key]
        if "upg" in key and not "chest" in key:
            upgrade_name = upgrades_dat[key]["name"]
            bp_copy[upgrade_name] = val
            del bp_copy[key]
    #print(bp_copy)
    return bp_copy, unit_name
            

def bpCombine(f_bp,p_bp,ep_bp):
    print(f_bp)
    free_prem = {}
    free_extra_prem = {}
    free_prem.update(f_bp)
    for key, val in p_bp.items():
        if key in free_prem:
            free_prem[key] = free_prem[key] + val
        else:
            free_prem[key] = val
    free_extra_prem.update(free_prem)
    for key, val in ep_bp.items():
        if key in free_extra_prem:
            free_extra_prem[key] = free_extra_prem[key] + val
        else:
            free_extra_prem[key] = val
    print("FREE")
    print(f_bp)
    print("PREMIUM")
    print(p_bp)
    print("ULTIMATE")
    print(ep_bp)
    print("FREE + PREMIUM")
    print(free_prem)
    print("FREE + PREMIUM + ULTIMATE")
    print(free_extra_prem)
    return free_prem, free_extra_prem

formatted_bp = {}
for bp in dat:
    #print(bp)
    one_bp = {}
    free = bpRewards(dat[bp]["free"])
    premium = bpRewards(dat[bp]["premium"])
    extra_premium = bpRewards(dat[bp]["extra_premium"])
    free, bp_name = bpLookup(free)
    premium, bp_name = bpLookup(premium)
    extra_premium, bp_name = bpLookup(extra_premium)
    free_premium, free_extra_premium = bpCombine(free, premium, extra_premium)
    one_bp["free"] = free
    one_bp["premium"] = premium
    one_bp["extra_premium"] = extra_premium
    one_bp["free_premium"] = free_premium
    one_bp["free_extra_premium"] = free_extra_premium
    formatted_bp[bp_name.split(" ")[0]] = one_bp
    
with open(fName, 'w') as w:
    json.dump(formatted_bp, w, indent=4)
    