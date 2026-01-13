from deepdiff import DeepDiff
from mergedeep import merge
import json
import re
import os
	
def nestedDict(d, keys):
    currentDict = d
    for key in keys:
        if isinstance(key, int):
            currentDict = currentDict[key]
        else:
            if key.isdigit():
                currentDict = currentDict[int(key)]
            else:
                currentDict = currentDict[key]
    return currentDict

def nestedDictValue(d, keys):
    currentDict = d
    for key in keys[:-1]:
        currentDict = currentDict[key]
    return currentDict[keys[-1]]

def nestedDictRoot(keys, value):
    nested_dict = {}
    nested_dict[keys[-1]] = value
    for key in reversed(keys[:-1]):
        nested_dict = {key: nested_dict}
    return nested_dict

def nestedDictOldNew(o, n, keys):
    oDict = o
    nDict = n
    for key in keys:
        oDict = oDict[key]
        nDict = nDict[key]
    return oDict, nDict

def nestedDictRootOldNew(keys, oldValue, newValue):
    nested_dict = {}
    nested_dict[keys[-1]] = {}
    nested_dict[keys[-1]]["oldValue"] = oldValue
    nested_dict[keys[-1]]["newValue"] = newValue
    for key in reversed(keys[:-1]):
        nested_dict = {key: nested_dict}
    return nested_dict
        
def compareTwo(oldDat, newDat):
    diff = DeepDiff(oldDat, newDat, ignore_order=True)
    diffDict = diff.to_dict()
    changes = {}
    newDict = {}
    if "dictionary_item_added" in diffDict:
        for new in diffDict["dictionary_item_added"]:
            root = new[4:-2]
            rootString = root.replace("'", " ").replace("[", " ").replace("]", " ")
            rootSplit = rootString.split()
            if len(rootSplit) == 1:
                newDict[rootSplit[0]] = newDat[rootSplit[0]]
            else:
                value = nestedDict(newDat, rootSplit)
                nested = nestedDictRoot(rootSplit, value)
                merge(newDict, nested)

    if "iterable_item_added" in diffDict:
        for iterNew in diffDict["iterable_item_added"]:
            root = iterNew[4:]
            rootString = root.replace("'", " ").replace("[", " ").replace("]", " ")
            rootSplit = rootString.split()
            rootSplitInitial = rootSplit[:-1]
            rootSplitFormat = []
            for r in rootSplitInitial:
                if r.isdigit():
                    rootSplitFormat.append(int(r))
                else:
                    rootSplitFormat.append(r)
            rootSplitIndex = int(rootSplit[-1])
            nest = nestedDict(newDat, rootSplitFormat)
            value = nest[rootSplitIndex]
            nested = nestedDictRoot(rootSplitFormat, value)
            merge(newDict, nested)
    
    removedDict = {}
    if "dictionary_item_removed" in diffDict:
        for removed in diffDict["dictionary_item_removed"]:
            root = removed[4:-2]
            rootString = root.replace("'", " ").replace("[", " ").replace("]", " ")
            rootSplit = rootString.split()
            rootSplitFormat = []
            for r in rootSplit:
                if r.isdigit():
                    rootSplitFormat.append(int(r))
                else:
                    rootSplitFormat.append(r)
            nestValue = nestedDictValue(oldDat, rootSplitFormat)
            nest = nestedDictRoot(rootSplit, nestValue)
            merge(removedDict, nest)
    
    if "iterable_item_removed" in diffDict:      
        for iterRemoved in diffDict["iterable_item_removed"]:
            root = iterRemoved[4:]
            rootString = root.replace("'", " ").replace("[", " ").replace("]", " ")
            rootSplit = rootString.split()
            rootSplitInitial = rootSplit[:-1]
            rootSplitFormat = []
            for r in rootSplitInitial:
                if r.isdigit():
                    rootSplitFormat.append(int(r))
                else:
                    rootSplitFormat.append(r)
            rootSplitIndex = int(rootSplit[-1])
            nest = nestedDict(oldDat, rootSplitFormat)
            value = nest[rootSplitIndex]
            nested = nestedDictRoot(rootSplitFormat, value)
            merge(removedDict, nested)

    changedDict = {}
    if "values_changed" in diffDict:
        for changed in diffDict["values_changed"]:
            root = changed[6:-2]
            rootString = root.replace("'", " ").replace("[", " ").replace("]", " ")
            rootSplit = rootString.split()
            rootSplitFormat = []
            for r in rootSplit:
                if r.isdigit():
                    rootSplitFormat.append(int(r))
                else:
                    rootSplitFormat.append(r)
            oldValue, newValue = nestedDictOldNew(oldDat, newDat, rootSplitFormat)
            nest = nestedDictRootOldNew(rootSplitFormat, oldValue, newValue)
            merge(changedDict, nest)

    if len(newDict) > 0: changes["added"] = newDict
    if len(removedDict) > 0: changes["removed"] = removedDict
    if len(changedDict) > 0: changes["changed"] = changedDict    
    return changes

