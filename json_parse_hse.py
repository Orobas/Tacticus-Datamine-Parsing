import json
patchVersion = "135"
fName = patchVersion + "-HomeScreenEvent-Formatted.json"
dataToTake = ["eventType", "eventName", "eventId", "rewardProgressId", "tradeInResourceCurrency", "tradeInResourceAmountPerPoint", "initialOfferIds", "modifiers", "trackers"]
storeDeals = ["_playmore", "_bundle", "_booster"]
with open('hs_events.json', 'r') as file:
    hse_dat = json.load(file)

with open('tiered_rewards.json', 'r') as tr_file:
    tr_dat = json.load(tr_file)

with open('paid_offers.json', 'r') as po_file:
    po_dat = json.load(po_file)

with open('upgrades.json', 'r') as upgrades_file:
    upgrades_dat = json.load(upgrades_file)

hse_formatted = {}
#for hs in hs_dat:
#    hs_name = hs["eventName"]
#    rewardId = hs["rewardProgressId"]
#    hs["reward"] = tr_dat[rewardId]
#    hs_format[hs_name] = hs

def formatHomeScreenEvent():
    for hse in hse_dat:
        hse_formatted[hse] = {}
        for tier in hse_dat[hse]:
            hse_formatted[hse][tier] = {}
            for d in dataToTake:
                if d in hse_dat[hse][tier]:
                    if d == "initialOfferIds":
                        hse_formatted[hse][tier]["storeOffers"] = {}
                        print(d)
                        if len(hse_dat[hse][tier][d]) > 0:
                            eventOffer = str(hse_dat[hse][tier][d][0])
                            for deal in storeDeals:
                                print(deal)
                                print(deal in eventOffer)
                                eventOffer = eventOffer.replace(deal, "")
                            print(eventOffer)
                            for storeOffer in po_dat["offers"]:
                                if eventOffer in storeOffer:
                                    print(storeOffer)
                                    rmId = po_dat["offers"][storeOffer]["realMoneyProductId"]
                                    if not rmId in hse_formatted[hse][tier]["storeOffers"]: hse_formatted[hse][tier]["storeOffers"][rmId] = {}
                                    hse_formatted[hse][tier]["storeOffers"][rmId]["price"] = po_dat["realMoneyProducts"][rmId]["price"]
                                    hse_formatted[hse][tier]["storeOffers"][rmId]["rewards"] = po_dat["realMoneyProducts"][rmId]["rewards"]
                    else:
                        hse_formatted[hse][tier][d] = hse_dat[hse][tier][d]
            hse_formatted[hse][tier]["rewards"] = tr_dat[hse_formatted[hse][tier]["rewardProgressId"]]
formatHomeScreenEvent()    
    
with open(fName, 'w') as hs_file:
    json.dump(hse_formatted, hs_file, indent=4)
