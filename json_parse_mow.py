import json
import math
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from pathlib import Path
from networkx.drawing.nx_agraph import graphviz_layout
from tabulate import tabulate
#with open('gameconfig_1_34.json', 'r') as file:
#        dat = json.load(file)
        
        
#print(dat["clientGameConfig"]["liveEvents"]["idunLiveEventConfigs"])

with open('units.json', 'r') as file:
    unit_dat = json.load(file)

with open('mow_event.json', 'r') as file:
    mow_dat = json.load(file)

def typeText(t):
    tt = ""
    if t == "incursionBattle":
        tt = "B"
    if t == "chest":
        tt = "C"
    if t == "incursionEnhancement":
        tt = "E"
    return tt
    
path = {}

def createNodes(json_dat):
    path = {}
    labelDict = {}
    battleDict = {}
    keyNodes = []
    for node in json_dat:
        path[node["index"]] = {}
        path[node["index"]]["path"] = []
        typeT = typeText(node["type"])
        path[node["index"]]["type"] = typeT
        labelDict[str(node["index"])] = node["nodeName"]
        if typeT == "B":
            path[node["index"]]["battleId"] = node["battleId"]
            battleDict[node["battleId"]] = {}
            battleDict[node["battleId"]]["name"] = node["nodeName"]
            battleDict[node["battleId"]]["index"] = str(node["index"])
        if "unlockedBy" in node:
            for i in node["unlockedBy"]:
                path[i["index"]]["path"].append(node["index"])
        if not "exclusiveWith" in node:
            keyNodes.append(node["index"])
    return path, labelDict, battleDict, keyNodes


def createBList(json_dat):
    blist = {}                 
    for battle in json_dat:
        blist[battle["battleId"]] = len(battle["enemies"])
    return blist

def createGraph(path, blist, labellist, battlelist, title, fullPath, colourMap):
    G.clear()
    plt.clf()
    #print(path)
    #print(blist)
    for key in path:
        node = str(key)
        G.add_node(node)

    for key in path:
        for i in path[key]["path"]:
            if path[key]["type"] == "B1":
                node = str(key)
            else:    
                node = str(key)
            if path[i]["type"] == "B1":
                node2 = str(i)
            else:    
                node2 = str(i)
            G.add_edge(node, node2)
    G.edges()
    pos=graphviz_layout(G, prog='dot')
    plt.figure(figsize=(10,14))
    nx.draw(G, pos, labels=labellist, with_labels=True, node_color=colourMap, node_size=600)
    ax = plt.gca()
    y = 1
    for b,bNode in battlelist.items():
        c = colourMap[int(battlelist[b]["index"])]
        plt.text(1.05, 0.9 - y * (.025), str(bNode["name"]) + ":" + str(blist[b]),  color=c, transform=ax.transAxes, fontsize=12, verticalalignment='center', horizontalalignment='right')
        y += 1
    plt.title(title, fontsize=20)
    fname = title + ".jpg"
    nodePath = Path("Nodemaps")
    print(fname)
    if not nodePath.is_dir():
        os.mkdir(nodePath)
    plt.savefig("Nodemaps\\" + fname, dpi=300, bbox_inches='tight')
    
def recurString(rstr, node, firstNode):
    if str(node) == str(firstNode):
        return ""
    if rstr == "":
        return str(node)
    else:
        return rstr + "," + str(node)
    
    
def continuePath(path, nodeIndex, endNode, recur_string, firstNode):
    recur_list = []
    if len(path[nodeIndex]["path"]) > 1:
        for i in path[nodeIndex]["path"]:
            if i == endNode:
                recur_list.append(recurString(recur_string, str(nodeIndex), firstNode))
            else:
                r_string = recurString(recur_string, str(nodeIndex), firstNode)
                rReturn = continuePath(path, i, endNode, r_string, firstNode)
                for r in rReturn:
                    recur_list.append(r)
                #recur_list.append(str(continuePath(path, i, endNode, r_string)))
    else:
        if path[nodeIndex]["path"][0] == endNode:
            recur_list.append(recurString(recur_string, str(nodeIndex), firstNode))
        else:
            r_string = recurString(recur_string, str(nodeIndex), firstNode)
            rReturn = continuePath(path, path[nodeIndex]["path"][0], endNode, r_string, firstNode)
            for r in rReturn:
                    recur_list.append(r)
            #recur_list.append(str(continuePath(path, path[nodeIndex]["path"][0], endNode, r_string)))
    return recur_list
    
def keyNodePathR(path, keyNodes):
    branch =[]
    for i in range(0, len(keyNodes)-1):
        startNode = keyNodes[i]
        endNode = keyNodes[i+1]
        if (int(endNode) - int(startNode)) == 1:
            continue
        new_path = []
        path_list = continuePath(path, startNode, endNode, "", startNode)
        branch.append(path_list)
    return branch

    
def keyNodePath(path, keyNodes):
    branch = []
    for i in range(0, len(keyNodes)-1):
        startNode = keyNodes[i]
        endNode = keyNodes[i+1]
        if (int(endNode) - int(startNode)) == 1:
            continue
        new_path = []
        for x in path[startNode]["path"]:
            if len(path[x]["path"]) == 1:
                if path[x]["path"][0] == endNode:
                    new_path.append(x)
                    continue
                else:
                    new_path2 = []
                    for y in path[x]["path"]:
                        if len(path[y]["path"]) == 1:
                            if path[y]["path"][0] == endNode:
                                new_path2.append(x)
                                new_path2.append(y)
                            else:
                                print("Shouldn't reach here")
                        else:
                            print("Shouldn't reach here")
                    new_path.append(new_path2)
            else:
                
                
                for y in path[x]["path"]:
                    new_path2 = []
                    if len(path[y]["path"]) == 1:
                        if path[y]["path"][0] == endNode:
                            new_path2.append(x)
                            new_path2.append(y)
                        else:
                            print("Shouldn't reach here")
                    else:
                        print("Shouldn't reach here")
                    new_path.append(new_path2)    
        branch.append(new_path)
    return branch

def flattenList(l):
    i = 0
    t_list = l
    new_list = []
    for a in t_list:
        for n in a:
            if len(n.split(',')) > 1:
                temp = n.split(',')
                for x in temp:
                    if not x in new_list or int(x) == -1:
                        new_list.append(x)
                i += 1
            else:
                if not n in new_list or int(n) == -1:
                    new_list.append(n)
    return new_list

def checkEnemiesBranch(path, battleList, branchList):
    bestPath = []
    badPath = []
    choicePath = []
    for branch in branchList:
        eCountList = []
        for node in branch:
            eCount = 0
            for n in node.split(','):
                if path[int(n)]['type'] == "B":
                    eCount += battleList[path[int(n)]['battleId']]
            eCountList.append(eCount)
        maxE = 0
        badPathT = []
        choicePathT = []
        bestPathT = []
        for e in range(len(eCountList)):
            if eCountList[e] == 0:
                badPathT.append(branch[e])
            elif eCountList[e] == maxE:
                if len(bestPathT) > 0:
                    choicePathT.append(bestPathT.pop())
                choicePathT.append(branch[e])
            elif eCountList[e] > maxE:
                if len(bestPathT) > 0:
                    badPathT.append(bestPathT.pop())
                if len(choicePathT) > 0:
                    for i in range(len(choicePathT)):
                        badPathT.append(choicePathT.pop(0))
                maxE = eCountList[e]
                bestPathT.append(branch[e])
            elif eCountList[e] < maxE:
                badPathT.append(branch[e])
        if len(badPathT) > 0:
            if len(choicePathT) == 0 and len(bestPathT) == 0:
                choicePath.append(badPathT)
            else:
                badPath.append(badPathT)
        if len(choicePathT) > 0:
            layerList = []
            if len(choicePathT[0].split(',')) > 1:
                pathSize = len(choicePathT[0].split(','))
                layerList = []
                for i in range(pathSize):
                    layer = []
                    for c in choicePathT:
                        splitC = c.split(',')
                        if not splitC[i] in layer:
                            layer.append(splitC[i])
                    layerList.append(layer)        
                for l in layerList:
                    if len(l) == 1:
                        bestPath.append(l)
                    else:
                        choicePath.append(l)
            else:
                choicePath.append(choicePathT)
        if len(bestPathT) > 0:
            bestPath.append(bestPathT)
        else:
            if len(choicePathT) > 0:
                if len(layerList) > 0: 
                    for l in layerList:
                        if len(l) > 1:
                            bestPath.append(["-1"])
                else:
                    bestPath.append(["-1"])
            else:
                bestPath.append(["-1"])
            
    bestPath = flattenList(bestPath)
    badPath = flattenList(badPath)
    for best in bestPath:
        if best in badPath:
            badPath[:] = [item for item in badPath if item != best]
    badPath.sort(key=int)
    
    return bestPath, choicePath, badPath
   
    
def createFullPath(path, bestPath):
    fullPath = []
    fullPath.append("0")
    step = 0
    while step != len(path)-1:
        if len(path[int(step)]["path"]) > 1:
            nextStep = bestPath.pop(0)
            if int(nextStep) == -1:
                fullPath.append("-1")
                step = path[int(step)]["path"][0]
            else:
                for n in nextStep.split(","):
                    if not n in fullPath: 
                        fullPath.append(n)
                        step = n
        else:
            if not path[int(step)]["path"][0] in fullPath: fullPath.append(str(path[int(step)]["path"][0]))
            step = path[int(step)]["path"][0] 
    return fullPath

def fullPathCount(path, fullPath, battlelist, choicePath):
    totalCount = 0
    for step in fullPath:
        if int(step) == -1:
            choice = choicePath.pop(0)[0]
            if path[int(choice)]['type'] == "B":
                totalCount += battlelist[path[int(choice)]["battleId"]]
        elif path[int(step)]['type'] == "B":
            totalCount += battlelist[path[int(step)]["battleId"]]
    return totalCount

def makeColourMap(fullPath, choicePath, badPath, pathLen):
    colourMap = [None] * pathLen
    for b in badPath:
        colourMap[int(b)] = '#E8565F'
    for f in fullPath:
        colourMap[int(f)] = '#27F591'
    for c1 in choicePath:
        for c in c1:
            if len(c.split(',')) > 1:
                for cs in c.split(','):
                    colourMap[int(cs)] = '#F59827'   
            else:
                colourMap[int(c)] = '#F59827'
    
    i = 0
    #print(colourMap)
    return colourMap

rarity_dict = {}
G = nx.Graph()    

def testPaths(path, fullPath, choicePath, badPath):
    print("Testing paths")
    for i in range(len(path)):
        if str(i) in fullPath:
            continue
        choiceFound = False
        for c in choicePath:
            if str(i) in c:
                choiceFound = True
        if choiceFound:
            continue
        if str(i) in badPath:
            continue
        print(str(i) + " is missing in all paths")

def test_mow(mow_index):
    mow = mow_dat["mows"][mow_index]
    mow_type = mow["unitId"]
    unit_name = unit_dat[mow_type]["name"]
    replace_char = "'- "
    for c in replace_char:
        unit_name = unit_name.replace(c,"")
    print(unit_name)
    for tier in mow["tiers"]:
        json_bat = tier["battles"]
        json_node = tier["nodes"]
        rarity = tier["rarity"]
        if rarity in rarity_dict:
            rarity_dict[rarity].append(len(rarity_dict[rarity]) + 1)
        else:
            rarity_dict[rarity] = [1]
        t_bList = createBList(json_bat)
        t_path, t_labels, t_battles, t_keyNodes = createNodes(json_node)
        
        t_branches = keyNodePathR(t_path, t_keyNodes)
        t_bestPath, t_choicePath, t_badPath = checkEnemiesBranch(t_path, t_bList, t_branches)
        t_fullPath = createFullPath(t_path, t_bestPath)
        t_colourMap = makeColourMap(t_fullPath, t_choicePath, t_badPath, len(t_path))
        t_count = fullPathCount(t_path, t_fullPath, t_bList, t_choicePath)
        print(rarity)
        print(rarity_dict)
        name = unit_name + "-" + rarity + "-" + str(len(rarity_dict[rarity])) + "-" + str(t_count)
        createGraph(t_path, t_bList, t_labels, t_battles, name, t_fullPath, t_colourMap)

def test_mow_one_tier(mow_index, tier_index):
    mow = mow_dat["mows"][mow_index]
    mow_type = mow["unitId"]
    unit_name = unit_dat[mow_type]["name"]
    replace_char = "'- "
    for c in replace_char:
        unit_name = unit_name.replace(c,"")
    print(unit_name)
    tier = mow["tiers"][tier_index]
    json_bat = tier["battles"]
    json_node = tier["nodes"]
    rarity = tier["rarity"]
    if rarity in rarity_dict:
        rarity_dict[rarity].append(len(rarity_dict[rarity]) + 1)
    else:
        rarity_dict[rarity] = [1]
    t_bList = createBList(json_bat)
    t_path, t_labels, t_battles, t_keyNodes = createNodes(json_node)
    
    t_branches = keyNodePathR(t_path, t_keyNodes)
    t_bestPath, t_choicePath, t_badPath = checkEnemiesBranch(t_path, t_bList, t_branches)
    t_fullPath = createFullPath(t_path, t_bestPath)
    t_colourMap = makeColourMap(t_fullPath, t_choicePath, t_badPath, len(t_path))
    t_count = fullPathCount(t_path, t_fullPath, t_bList, t_choicePath)
    print(rarity)
    print(rarity_dict)
    name = unit_name + "-" + rarity + "-" + str(len(rarity_dict[rarity])) + "-" + str(t_count)
    createGraph(t_path, t_bList, t_labels, t_battles, name, t_fullPath, t_colourMap)

def full_mow():
    for mow in mow_dat["mows"]:
        rarity_dict = {}
        mow_type = mow["unitId"]
        unit_name = unit_dat[mow_type]["name"]
        replace_char = "'- "
        for c in replace_char:
            unit_name = unit_name.replace(c,"")
        for tier in mow["tiers"]:
            json_bat = tier["battles"]
            if "nodes" in tier:
                json_node = tier["nodes"]
                rarity = tier["rarity"]
                if rarity in rarity_dict:
                    rarity_dict[rarity].append(len(rarity_dict[rarity]) + 1)
                else:
                    rarity_dict[rarity] = [1]
                t_bList = createBList(json_bat)
                t_path, t_labels, t_battles, t_keyNodes = createNodes(json_node)
                
                t_branches = keyNodePathR(t_path, t_keyNodes)
                t_bestPath, t_choicePath, t_badPath = checkEnemiesBranch(t_path, t_bList, t_branches)
                t_fullPath = createFullPath(t_path, t_bestPath)
                t_colourMap = makeColourMap(t_fullPath, t_choicePath, t_badPath, len(t_path))
                t_count = fullPathCount(t_path, t_fullPath, t_bList, t_choicePath)
                print(rarity)
                print(rarity_dict)
                name = unit_name + "-" + rarity + "-" + str(len(rarity_dict[rarity])) + "-" + str(t_count)
                createGraph(t_path, t_bList, t_labels, t_battles, name, t_fullPath, t_colourMap)
            else:
                rarity = tier["rarity"]
                if rarity in rarity_dict:
                    rarity_dict[rarity].append(len(rarity_dict[rarity]) + 1)
                else:
                    rarity_dict[rarity] = [1]
                enemyCount = 0
                for b in tier["battles"]:
                    enemyCount += len(b["enemies"])
                print(unit_name + "-" + rarity + "-" + str(len(rarity_dict[rarity])) + "-" + str(enemyCount))
                print("Enemy Count: " + str(enemyCount))
                
#test_mow(4)
#test_mow_one_tier(1,11)
full_mow()
#    
#json_bat = mow_dat["tiers"][0]["battles"]
#json_node = mow_dat["tiers"][0]["nodes"]
#rarity = mow_dat["tiers"][0]["rarity"]
#t_bList = createBList(json_bat)
#t_path, t_labels, t_battles ,t_keynodes = createNodes(json_node)
#branches = keyNodePathR(t_path, t_keynodes)
#print(branches)
#t_bestPath, t_choicePath, t_badPath = checkEnemiesBranch(t_path, t_bList, branches)
#t_fullPath = createFullPath(t_path, t_bestPath)
#testPaths(t_path, t_fullPath, t_choicePath, t_badPath)
#t_colourMap = makeColourMap(t_fullPath, t_choicePath, t_badPath, len(t_path))
#t_count = fullPathCount(t_path, t_fullPath, t_bList, t_choicePath)
#name = rarity + "1-" + str(t_count)
#createGraph(t_path, t_bList, t_labels, t_battles, name, t_fullPath, t_colourMap)

