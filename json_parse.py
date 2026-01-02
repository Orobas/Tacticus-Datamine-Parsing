import json
import math
import itertools
from tabulate import tabulate
with open('gameconfig_1_35.json', 'r') as file:
        dat = json.load(file)
        
battle_list = ["Alpha","Beta","Gamma","Delta","Epsilon","Zeta"]

num_of_battles = 15
alliance_list = ["Imperial", "Xenos", "Chaos"]
#Continue with Imp
#sector_list = [60, 40, 29]
#battle_start_list = [3, 3, 2]
#As is
#sector_list = [59, 40, 29]
#battle_start_list = [0, 3, 2]
sector_list = [60, 40, 29]
battle_start_list = [3, 3, 2]
enemy_total = [0, 0, 0]
sector_list_o = [60, 40, 29]
battle_start_list_o = [3, 3, 2]
enemy_total_o = [0, 0, 0]
avg_total = [0, 0, 0]
#with open('out.json', 'w') as w:
#    json.dump(dat["clientGameConfig"]["battles"]["waves"]["tracks"], w, indent=4)
#dat["clientGameConfig"]["battles"]["waves"]["tracks"]

def roman_numeral(num):
    lookup = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    result = ""
    for value, roman_char in lookup:
        while num >= value:
            result += roman_char
            num -= value
    return result

def tens(num):
    num_div = math.floor((num - 1)/10)
    num_str = str(num_div) + "1-" + str(num_div+1) + "0"
    return str(num_str)

def count_enemy_all():
    alliances = {}
    for alliance in range(3):
        sector_ten_list = {}
        sector_list = {}
        sector_count = 1
        for sector in dat["clientGameConfig"]["battles"]["waves"]["tracks"][alliance]["tiers"]:
            b_enemy_count = {}
            battle_count = 0
            for battle in sector["battles"]:
                enemy_count = 0
                for wave in battle["waves"]:
                    enemy_count += len(wave["enemies"]["defaultGroup"])
                b_enemy_count[battle_list[battle_count]] = enemy_count
                battle_count += 1
            
            sector_list[sector_count] = {"Name" : roman_numeral(sector_count), "Battles": b_enemy_count}
            sector_count += 1
            #if (sector_count -1) % 10 == 0:
            #    ten_range = "{0}".format(tens(sector_count-1))
            #   sector_ten_list[ten_range] = sector_list
            #    sector_list = {}
        alliances[alliance_list[alliance]] = sector_list
    return alliances
            

def do_battle(sector, battle, instructions, nc):
    total_count = 0
    sect = sector.copy()
    batt = battle.copy()
    print("Node Num: " + str(nc))
    print("Node: " + str(instructions))
    print("Sect: " + str(sect))
    print("Batt: " + str(batt))
    for i in range(max(instructions)):
        if i < instructions[0]:
            total_count += formatted_data["Imperial"][sect[0]]["Battles"][battle_list[batt[0]]]
            batt[0] += 1
            if batt[0] == 6:
                sect[0] += 1
                batt[0] = 0
        if i < instructions[1]:
            total_count += formatted_data["Xenos"][sect[1]]["Battles"][battle_list[batt[1]]]
            batt[1] += 1
            if batt[1] == 6:
                sect[1] += 1
                batt[1] = 0
        if i < instructions[2]:
            total_count += formatted_data["Chaos"][sect[2]]["Battles"][battle_list[batt[2]]]
            batt[2] += 1
            if batt[2] == 6:
                sect[2] += 1
                batt[2] = 0
    return total_count
    
def highest(sector, battle):
    imp_count = formatted_data["Imperial"][sector[0]]["Battles"][battle_list[battle[0]]]
    xeno_count = formatted_data["Xenos"][sector[1]]["Battles"][battle_list[battle[1]]]
    chaos_count = formatted_data["Chaos"][sector[2]]["Battles"][battle_list[battle[2]]]
    highest, alliance_name, alliance_index = imp_count, "Imperial", 0
    if xeno_count > highest: highest, alliance_name, alliance_index = xeno_count, "Xenos", 1
    if chaos_count > highest: highest, alliance_name, alliance_index = chaos_count, "Chaos", 2
    return alliance_name, alliance_index, highest

def highest_cumulative(sector, battle):
    total_count = 0
    steps = []
    for i in range(11):
        name, i, count = highest(sector, battle)
        total_count += count
        steps.append(name)
        battle[i] += 1
        if battle[i] == 6:
            battle[i] = 0
            sector[i] += 1
    return total_count, steps

def partitions(n, k):
    for c in itertools.combinations(range(n+k-1), k-1):
        yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]

def node(state, step, ind):
    n_state = state
    n_step = step
    n_state[ind] += 1
    if step != 8:
        node(n_state, n_step + 1, 0)
        node(n_state, n_step + 1, 1)
        node(n_state, n_step + 1, 2)
    else:
        print(n_state)
        input()
        return state
        
def start_path_tree(s, b):
    o_sec = s
    o_bat = b
    node_list = []
    for p in partitions(num_of_battles, 3):
        node_list.append(p)
    print("NUM OF NODES: " + str(len(node_list)))
    node_count = 0
    count_list = []
    for node in node_list:
        sec = o_sec
        bat = o_bat
        print("SEC: " + str(sec))
        print("BAT: " + str(bat))
        node_count += 1
        count = do_battle(sec, bat, node, node_count)
        count_list.append(count)
        print("Node " + str(node_count) + ": " + str(node) + " Count: " + str(count))
    highest_count = max(count_list)
    print("\nBest: " + str(node_list[count_list.index(highest_count)]) + " Count: " + str(highest_count))
        

def orig():   
    for alliance in range(3):
        print("Alliance: " + str(alliance))
        battle_count = 0 
        sector_enemy_count = 0
        battle_bool = False
        while True: 
            battle_index = 0
            print("Sector " + str(sector_list_o[alliance]))
            for battle in dat["clientGameConfig"]["battles"]["waves"]["tracks"][alliance]["tiers"][int(sector_list_o[alliance])-1]["battles"]:
                battle_enemy_count = 0
                wave_count = 0
                if battle_index == battle_start_list_o[alliance]: battle_bool = True
                if not battle_bool: 
                    battle_index += 1
                    continue
                print("\tBattle " + battle_list[battle_index] + ", " + str(battle_count + 1))
                for wave in battle["waves"]:
                    wave_count+=1
                    enemy_count = len(wave["enemies"]["defaultGroup"])
                    battle_enemy_count += enemy_count
                    print("\t\tWave " + str(wave_count) + ": " + str(enemy_count))
                print("\n\tTotal: " + str(battle_enemy_count))
                sector_enemy_count += battle_enemy_count
                battle_index += 1
                battle_count += 1
                if battle_count == num_of_battles: break
            if battle_count == num_of_battles: break
            sector_list_o[alliance] += 1
        enemy_total[alliance] = sector_enemy_count
        avg_total[alliance] = round((sector_enemy_count / 11), 2)
        print("\nTotal: " + str(sector_enemy_count))
        print("Average: " + str(sector_enemy_count / 11))
        
    data = [] 
    for alliance in range(3):
        data.append((alliance_list[alliance], enemy_total[alliance], avg_total[alliance]))
    data = tuple(data)
    print(tabulate(data, headers=["Alliance", "Total Nids", "Average Nids"]))
    
formatted_data = count_enemy_all()
#print(formatted_data)



tc, path = highest_cumulative(sector_list, battle_start_list)
print("Total count: " + str(tc))
print(path)
node_list = []
sec_o = sector_list_o.copy()
bat_o = battle_start_list_o.copy()
start_path_tree(sec_o, bat_o)
with open('onslaught_enemy_count.json', 'w') as w:
    json.dump(formatted_data, w, indent=4)

#orig()