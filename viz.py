"""
Jeremy B. Merrill



"""
#TODO: Refactor optimization algorithm to use all the constraints:
#   Do not pair three expenditures that all have a whole fifth of a bill to themselves.
#   Find a way to deal with 16.30 excess.

from jinja2 import Environment, FileSystemLoader, Markup
from copy import deepcopy

GROUP_MAX = 201
TOLERANCE = 7
TOLERANCE_EXACT = 1
TRANCH_WIDTH = 20
CALLOUT_WIDTH = 60 #characters
BORDER_WIDTH = 2 #as set in css, .coverer
TOTAL_PER_STUDENT = 276.30
LARGEST_BILL = 20 #i.e. the largest bill is a twenty dollar bill
NAME_CORRECTIONS = {"Office Supplies": "Of.Supp",
            "President's Room & Board": "Prez's Room & Board" }

small_bills = [(10, "ten"), (5, "five"), (1, "one")]
coins = [(.25, "quarter"), (.10, "dime"), (.05, "nickel"), (.01, "penny")]
small_types = small_bills + coins

env = Environment(loader = FileSystemLoader('./'), autoescape=True, trim_blocks=True)

def findSmallBills(remainder, expenditures):
    """Find the expenditures which most closely represent the remainder of money that doesn't fit into the largest bill."""
    largest = (0, [])
    for i,exp in enumerate(expenditures):
        if exp["cost_per"] < (remainder + 5): #this "if" is just a sanity check: things work fine without this check, but it's inefficent.
            leftover = remainder - exp["cost_per"]
            one_level_down = findSmallBills(leftover, expenditures[(i+1):])
            candidate_largest = (one_level_down[0] + exp["cost_per"], one_level_down[1] + [exp] )
            if abs((abs(remainder - largest[0]) - abs(remainder - candidate_largest[0]))) < .00005: #like equality, but not caring about precision errors, etc.
                if len(largest[1]) > len(candidate_largest[1]):
                    largest = candidate_largest
            elif (abs(remainder - largest[0]) - abs(remainder - candidate_largest[0])) > .00005: #likewise, but requiring positive sign
                largest = candidate_largest
        elif exp["cost_per"] == remainder:
            largest = (remainder, [exp])
    return largest

def doPairs(remaining_pixels, expenditures, exps_with_whole_tranches_so_far):
    """expenditures must be ordered."""
    best_tranch = (0, [])
    for i,exp in enumerate(expenditures):
        if exp["pixels"] < (remaining_pixels + 5): #this "if" is just a sanity check: things work fine without this check, but it's inefficent.
            leftover = remaining_pixels - exp["pixels"]
            whole_tranches_left = exps_with_whole_tranches_so_far
            if exp["whole_tranches"] > 0:
                whole_tranches_left -= 1
            one_level_down = doPairs(leftover, expenditures[(i+1):], whole_tranches_left)
            candidate_best = (one_level_down[0] + exp["pixels"], one_level_down[1] + [exp] )

            if (exps_with_whole_tranches_so_far > 0 or exp["whole_tranches"] == 0):
                if abs((abs(remainder - largest[0]) - abs(remainder - candidate_largest[0]))) < .005: #like equality, but not caring about precision errors, etc.
                    if len(largest[1]) > len(candidate_largest[1]):
                        largest = candidate_largest
                elif (abs(remainder - largest[0]) - abs(remainder - candidate_largest[0])) > .005: #likewise, but requiring positive sign
                    largest = candidate_largest

        elif abs(exp["cost_per"] - remainder) < TOLERANCE and (exps_with_whole_tranches_so_far > 0 or exp["whole_tranches"] == 0):
            best_tranch = (remainder, [exp])
    return best_tranch

def display_name_format(expenditure, name_corrections):
    """In place changes to expenditure name."""
    expenditure["display_name_split"] = expenditure["display_name"]

    if expenditure["display_name_split"] in name_corrections:
        expenditure["display_name_split"] = name_corrections[expenditure["display_name_split"]]
    return expenditure

def processExpenditure(e):
    """add pixels, whole_tranches, and cost_per to expenditure dicts."""
    cost = e["cost"]
    cost_per = cost / 1150.0
#    if len(e["blurb"]) > CALLOUT_WIDTH:
#        for i in range(int(len(e["blurb"]) / CALLOUT_WIDTH)):
#            try:
#                split_index = e["blurb"].rindex(" ", (((i + 1) * CALLOUT_WIDTH)+i*6) -5, (((i + 1) * CALLOUT_WIDTH)+i*6) +5)
#                e["blurb"] = e["blurb"][:split_index] + Markup("<br />") + e["blurb"][split_index:]                
#            except ValueError:
#                e["blurb"] = e["blurb"][:(((i + 1) * CALLOUT_WIDTH)+i*6)] + Markup("<br />") + e["blurb"][(((i + 1) * CALLOUT_WIDTH)+i*6):]
    e["cost_per"] = cost_per
    e["whole_tranches"] = cost_per // 4
    e["pixels"] = ((cost_per / 4) % 1) *200
    e["bills"] = []
    e["which_bill"] = 0
    return e

def processSmallBills(e):
    #del e["whole_tranches"]
    #del e["pixels"]
    #del e["bills"]
    #del e["which_bill"]
    e["bills"] = []
    cost_per = e["cost_per"]    
    for money_amt, money_name in small_types:
        of_this_type = int(cost_per // money_amt)
        if of_this_type != 0:
            for x in xrange(of_this_type):
                e["bills"].append(money_name)
            cost_per = cost_per % money_amt
    print "<!--",e["cost_per"], e["bills"],"-->"
    e = display_name_format(e, NAME_CORRECTIONS)

    e["left"] = 40                #left, top, whole_tranches_in_this_bill, 
    e["top"] = 0
    e["whole_tranches_in_this_bill"] = 5
    return e


def convertPixelToPercent(pixel_height):
    return ((pixel_height / GROUP_MAX) * 100)

expenditures = [] #a list of dicts repring all expenditures
expenditures.append({"display_name":"ASCMC Senate","cost":10000,"safe_name":"senate", "blurb":"ASCMC Senate meets on Mondays"})
expenditures.append({"display_name":"Senate Student Trips", "cost":2000,"safe_name":"senate_trips", "blurb":"The ASCMC Senate has a separate fund for funding student trips to, for instance, Harvard MUN."})
expenditures.append({"display_name":"Campus Organizations Chair Fund", "cost":8500,"safe_name":"co_chair", "blurb":"The CO Chair, Stagory Athena '11, has a separate fund to disburse to clubs at his/her whim."})
expenditures.append({"display_name":"General Fund", "cost":1285,"safe_name":"general_fund", "blurb":"God only knows what this is for..."})
#expenditures.append({"display_name":"Class 2011 (2012)", "cost":18000,"safe_name":"class_2011", "blurb":"The Senior Class budget. Spent by the Senior Class President Mary Doyle '12 on parties, such as the 100 Days and 200 Days parties."})
expenditures.append({"display_name":"Class 2012 (2013)", "cost":3500, "safe_name":"class_2012", "blurb":"The Junior Class budget. Spent by the Junior Class President, cStagory Athena '13."})
expenditures.append({"display_name":"Class 2013 (2014)", "cost":3000, "safe_name":"class_2013", "blurb":"The Sophomore Class budget. Spent by the Sophomore Class President, Stagory Athena '14."})
expenditures.append({"display_name":"Class 2014 (2015)", "cost":2000, "safe_name":"class_2014", "blurb":"The Freshman Class budget. Spent by their president, when he or she is elected."})
expenditures.append({"display_name":"SAC", "cost":17500, "safe_name":"sac", "blurb":"The Student Activities Chair's budget. The SAC, Stagory Athena, plans many of the Saturday night events."})
expenditures.append({"display_name":"DAC", "cost":8500, "safe_name":"dac", "blurb":"The Dorm Activities Chair's budget. The DAC, Stagory Athena, plans TNC."})
expenditures.append({"display_name":"SLC", "cost":11500, "safe_name":"slc", "blurb":"The Sober Loser Chair's budget. The SLC, Burke Zanft, plans dry activities like Hub Quiz."})
expenditures.append({"display_name":"Off-Campus Sports Events", "cost":3500, "safe_name":"offcampus_sports", "blurb":"blah blah."})
expenditures.append({"display_name":"Monte Carlo", "cost":12000, "safe_name":"monte", "blurb":"Monte Carlo blah blah"})
expenditures.append({"display_name":"White Party", "cost":4000, "safe_name":"white", "blurb":"blah blah"})
expenditures.append({"display_name":"Wedding Party", "cost":12000, "safe_name":"wedding", "blurb":"blah blah"})
expenditures.append({"display_name":"President's Fund", "cost":2500, "safe_name":"pres_fund", "blurb":"blah blah"})
expenditures.append({"display_name":"Dorms Total", "cost":31500, "safe_name":"dorms", "blurb":"blah blah"})
expenditures.append({"display_name":"Forum", "cost":6000, "safe_name":"forum", "blurb":"blah blah"})
expenditures.append({"display_name":"Ayer", "cost":29000, "safe_name":"ayer", "blurb":"blah blah"})
#expenditures.append({"display_name":"Office Supplies", "cost":750, "safe_name":"office_supplies", "blurb":"blah blah"})
expenditures.append({"display_name":"Contingency", "cost":25000, "safe_name":"contingency", "blurb":"blah blah"})
expenditures.append({"display_name":"Event(s) Damages", "cost":5000, "safe_name":"damages", "blurb":"blah blah"})
expenditures.append({"display_name":"Campus Security (Private)", "cost":15000, "safe_name":"private_sec", "blurb":"blah blah"})
expenditures.append({"display_name":"Student Security", "cost":5000, "safe_name":"student_sec", "blurb":"blah blah"})
expenditures.append({"display_name":"Stipends", "cost":9400, "safe_name":"stipends", "blurb":"blah blah"})
expenditures.append({"display_name":"President's Room & Board", "cost":7000, "safe_name":"pres_room", "blurb":"blah blah"})
expenditures.append({"display_name":"5C Clubs (Total)", "cost":25165, "safe_name":"clubs_5c", "blurb":"blah blah"})
expenditures.append({"display_name":"CMC Clubs (Total)", "cost":39150, "safe_name":"clubs_cmc", "blurb":"blah blah"})

expenditures = [processExpenditure(e) for e in expenditures]

#--- Separate expenditures into those which are going into twenties and which are small bills and coins.

dollars_into_small_bills_and_coins = TOTAL_PER_STUDENT % LARGEST_BILL
small_bills_and_coins = []
small_bills_and_coins = findSmallBills(dollars_into_small_bills_and_coins, expenditures)[1]

#TODO remove from expenditures the ones that are going into small bills/coins
#<temporary>
#small_bills_and_coins.append({"display_name":"Class 2011 (2012)", "cost":18000,"safe_name":"class_2011", "blurb":"The Senior Class budget. Spent by the Senior Class President Mary Doyle '12 on parties, such as the 100 Days and 200 Days parties."})
#small_bills_and_coins.append({"display_name":"Office Supplies", "cost":750, "safe_name":"office_supplies", "blurb":"blah blah"})
#small_bills_and_coins = [processExpenditure(e) for e in small_bills_and_coins] 
#</temporary>
for exp in small_bills_and_coins:
    expenditures.remove(exp)
small_bills_and_coins = [processSmallBills(e) for e in small_bills_and_coins]

#-----

def expenditureMatch(expenditure1, expenditures_rest, key="pixels"):
    """From a SORTED list of expenditures, return a set of expenditures for whom the sum of the "pixel" field is closest to GROUP_MAX and which includes the first element of expenditures."""
    target = GROUP_MAX - expenditure1[key]
    matched_expenditures = list() #rename this.
    matched_expenditures.append(expenditure1)
    expenditures_rest.reverse()
    for expenditure in expenditures_rest:
        #these if statements should be rewritten for clarity, to not repeat reverse, return behavior.
        if abs(expenditure[key] - target) >= TOLERANCE: 
            # if an expenditure is too big, skip it
            pass
        if abs(expenditure[key] - target) < TOLERANCE_EXACT: #pair an expenditure and stop if it's within the EXACT tolerance range.
            matched_expenditures.append(expenditure)
            expenditures_rest.remove(expenditure)
            target = target - expenditure[key]
            #print "Pairing " + str([exp["display_name"] + ": " + str(exp[key]) for exp in matched_expenditures]) + ". Diff: " + str(target)
            expenditures_rest.reverse()
            return matched_expenditures, expenditures_rest
        if (abs(expenditure[key] - target) < TOLERANCE) \
            or (expenditure[key] < target): 
            #pair an expenditure and keep going if it is within the TOLERANCE range or less than the amount of pixels still needed.
            matched_expenditures.append(expenditure)
            expenditures_rest.remove(expenditure)
            target = target - expenditure[key]
    #print "Pairing " + str([exp["display_name"] + ": " + str(exp[key]) for exp in matched_expenditures]) + ". Diff: " + str(target)
    expenditures_rest.reverse()
    return matched_expenditures, expenditures_rest


sorted_expenditures = sorted(expenditures, key=lambda exp : exp.get("pixels"))
list_of_matches = []

while sorted_expenditures: #... is not empty
    (matched_expenditures, sorted_expenditures) = expenditureMatch(sorted_expenditures.pop(),sorted_expenditures)
    list_of_matches.append(matched_expenditures)

#-------------------
tranches = [] #a tranch is a list of tuples: (display_height, expenditure)
#TODO: order expenditures in match as: (big) small* (big)
for match in list_of_matches:
    mixtranch = [] #mixtranch is a tranch with more than one item in it.
    
    #tranch_item first
    for x in range(0,int(match[0]["whole_tranches"])):
        tranches.append([(convertPixelToPercent(GROUP_MAX), match[0])])
    mixtranch.append((convertPixelToPercent(match[0]["pixels"]), match[0]))
    
    #tranch_item second through second-to-last
    for exp in match[1:-1]:
       mixtranch.append((convertPixelToPercent(exp["pixels"]), exp))
    
    #tranch_item last
    if len(match) > 1:
        mixtranch.append((convertPixelToPercent(match[-1]["pixels"]), match[-1]))

    #normalize pixel sizes
    pixelsum = 0
    mixtranch2 = []
    for tranch_item in mixtranch:
        pixelsum += tranch_item[0]
    for i,tranch_item in enumerate(mixtranch):
        if i < len(mixtranch)-1:
            tranch_item = ((convertPixelToPercent(tranch_item[0] * GROUP_MAX / pixelsum) - BORDER_WIDTH), tranch_item[1]) #TODO -2 accounts for border width, only for height though.
        else:
            tranch_item = ((convertPixelToPercent(tranch_item[0] * GROUP_MAX / pixelsum)), tranch_item[1]) #TODO -2 accounts for border width
        mixtranch2.append(tranch_item)
    tranches.append(mixtranch2)
    if len(match) != 1:
        for x in range(0,int(match[-1]["whole_tranches"])):
            tranches.append([(convertPixelToPercent(GROUP_MAX), match[-1])])

#---------------- Split the names properly

bills = [] #a list of bills, a bill is a five-element list of tranches (which are tuples)
while len(tranches) >= 5:
    bills.append(tranches[:5])
    tranches = tranches[5:]



bills_by_exp = []
for bill_i,bill in enumerate(bills):
    bills_by_exp.append([])
    for tranch_index, tranch in enumerate(bill):
        for exp_index,expenditure in enumerate(tranch):
            if (expenditure[1]["safe_name"] not in [x["safe_name"] for x in bills_by_exp[bill_i]]): 

                FONT_HEIGHT = 16 / GROUP_MAX #needs to be a percent: the number should be in pixels.

                expenditure = (expenditure[0], display_name_format(expenditure[1], NAME_CORRECTIONS))

                expenditure[1]["left"] = tranch_index * TRANCH_WIDTH #this is a percentage!!
                expenditure[1]["top"] = 0

                #left, top, whole_tranches_in_this_bill, 

                if expenditure[1]["which_bill"] == 0:
                    expenditure[1]["leftover_tranches"] = expenditure[1]["whole_tranches"] #only if it isn't already set?
                expenditure[1]["whole_tranches_in_this_bill"] = min(expenditure[1]["leftover_tranches"], 5, 4-tranch_index)
                expenditure[1]["leftover_tranches"] -= min(expenditure[1]["leftover_tranches"], 5, 4-tranch_index)

                expenditure[1]["text_width"] = expenditure[1]["whole_tranches_in_this_bill"] * TRANCH_WIDTH
                if expenditure[1]["whole_tranches_in_this_bill"] == 0 or (expenditure[0] > FONT_HEIGHT and tranch_index != 4 and expenditure[1]["which_bill"] == 0):
                    expenditure[1]["text_width"] += 20
                    #TODO: this shouldn't happen if the partial bit is in a diff bill.

                if expenditure[1]["whole_tranches_in_this_bill"] == 0 or expenditure[0] > FONT_HEIGHT:
                    if exp_index == 1:
                        expenditure[1]["top"] = tranch[0][0]
                    elif exp_index == 2:
                        expenditure[1]["top"] = tranch[1][0] + tranch[0][0]
                    elif exp_index == 3:
                        expenditure[1]["top"] = tranch[1][0] + tranch[0][0] + tranch[2][0]

                if bill_i not in expenditure[1]["bills"]:
                    expenditure[1]["bills"].append(bill_i)
                #print("<!--",expenditure[1]["safe_name"], "whole_tranches_in_bill", expenditure[1]["whole_tranches_in_this_bill"], "left", expenditure[1]["left"], "text_width", expenditure[1]["text_width"], "-->")
                bills_by_exp[bill_i].append(deepcopy(expenditure[1]))
                expenditure[1]["which_bill"] += 1

template = env.get_template('viztemplate.py')

print template.render({'bills': bills, 'expenditures':expenditures, 
                        'GROUP_MAX': GROUP_MAX, 'bills_by_exp':bills_by_exp, 
                        'small_bills_and_coins': small_bills_and_coins, 
                        'small_bills': small_bills,
                        'coins': coins})
