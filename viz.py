"""
Jeremy B. Merrill



"""
#TODO: Refactor optimization algorithm to use all the constraints:
#   Do not pair three expenditures that all have a whole fifth of a bill to themselves.
#   Find a way to deal with 16.30 excess.

from jinja2 import Environment, FileSystemLoader, Markup
from copy import deepcopy
from vizconfig import TOTAL_PER_CAPITA, LARGEST_BILL, NAME_CORRECTIONS, TRANCHES_PER_BILL, BILLS_PER_COLUMN, NUMBER_OF_STUDENTS, expenditures, explanatory_paragraph, title

GROUP_MAX = 201
TOLERANCE = 7
TOLERANCE_EXACT = 1
TRANCH_WIDTH = 100 / TRANCHES_PER_BILL
CALLOUT_WIDTH = 60 #characters
BORDER_WIDTH = 2 #as set in css, .coverer



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
    cost_per = cost / float(NUMBER_OF_STUDENTS)
    e["blurb"] = Markup(e["blurb"].replace("'", "\\'"))
#    if len(e["blurb"]) > CALLOUT_WIDTH:
#        for i in range(int(len(e["blurb"]) / CALLOUT_WIDTH)):
#            try:
#                split_index = e["blurb"].rindex(" ", (((i + 1) * CALLOUT_WIDTH)+i*6) -5, (((i + 1) * CALLOUT_WIDTH)+i*6) +5)
#                e["blurb"] = e["blurb"][:split_index] + Markup("<br />") + e["blurb"][split_index:]                
#            except ValueError:
#                e["blurb"] = e["blurb"][:(((i + 1) * CALLOUT_WIDTH)+i*6)] + Markup("<br />") + e["blurb"][(((i + 1) * CALLOUT_WIDTH)+i*6):]
    e["cost_per"] = float(int(cost_per * 100))/100
    e["whole_tranches"] = cost_per // 4
    e["pixels"] = ((cost_per / 4) % 1) *200
    e["bills"] = []
    e["which_bill"] = 0
    #print " ".join([e["safe_name"], "$" + str(e["cost_per"]), "=", str(e["whole_tranches"]), str(e["pixels"])]) + "<br />"
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
    #print "<!--",e["cost_per"], e["bills"],"-->"
    e = display_name_format(e, NAME_CORRECTIONS)

    e["left"] = 40                #left, top, whole_tranches_in_this_bill, 
    e["top"] = 0
    e["whole_tranches_in_this_bill"] = 5
    return e


def convertPixelToPercent(pixel_height):
    return ((pixel_height / GROUP_MAX) * 100)



expenditures = [processExpenditure(e) for e in expenditures]

#--- Separate expenditures into those which are going into twenties and which are small bills and coins.

dollars_into_small_bills_and_coins = TOTAL_PER_CAPITA % LARGEST_BILL
small_bills_and_coins = []
small_bills_and_coins = findSmallBills(dollars_into_small_bills_and_coins, expenditures)[1]


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
            #print "Pairing " + str([exp["display_name"] + ": " + str(exp[key]) for exp in matched_expenditures]) + ". Diff: " + str(target) + "<br />"
            expenditures_rest.reverse()
            return matched_expenditures, expenditures_rest
        if (abs(expenditure[key] - target) < TOLERANCE) \
            or (expenditure[key] < target): 
            #pair an expenditure and keep going if it is within the TOLERANCE range or less than the amount of pixels still needed.
            matched_expenditures.append(expenditure)
            expenditures_rest.remove(expenditure)
            target = target - expenditure[key]
    #print "Pairing " + str([exp["display_name"] + ": " + str(exp[key]) for exp in matched_expenditures]) + ". Diff: " + str(target) + "<br />"
    expenditures_rest.reverse()
    return matched_expenditures, expenditures_rest


sorted_expenditures = sorted(expenditures, key=lambda exp : exp.get("pixels"))
list_of_matches = []

while sorted_expenditures: #... is not empty
    (matched_expenditures, sorted_expenditures) = expenditureMatch(sorted_expenditures.pop(),sorted_expenditures)
    list_of_matches.append(matched_expenditures)

#-------------------
tranches = [] #a tranch is a list of tuples: (display_height, expenditure)

def orderMatch(match):
    """ Put a match in order so that the first and last elements have whole tranches and all middle elements don't."""
    new_match = [[] for x in xrange(0, len(match))]
    expenditures_with_whole_tranches = [exp for exp in match if exp["whole_tranches"] > 0]
    #assert len(expenditures_with_whole_tranches) <= 2
    if len(expenditures_with_whole_tranches) > 0:
        new_match[0] = expenditures_with_whole_tranches[0]
        if len(expenditures_with_whole_tranches) > 1:
            new_match[-1] = expenditures_with_whole_tranches[-1]
        for index, exp in enumerate([exp for exp in match if exp["whole_tranches"] == 0]):
            new_match[index+1] = exp
        return new_match
    else:
        return match


for match in list_of_matches:
    match = orderMatch(match)
    #print ' '.join([exp["safe_name"] + " " + str(exp["whole_tranches"]) for exp in match]) + "<br />"
    mixtranch = [] #mixtranch is a tranch with more than one item in it.
    
    #first tranch_item
    for x in range(0,int(match[0]["whole_tranches"])):
        tranches.append([(convertPixelToPercent(GROUP_MAX), match[0])])
    mixtranch.append((convertPixelToPercent(match[0]["pixels"]), match[0]))
    
    # second through second-to-last tranch_item 
    for shouldnt_be_outer_exp in match[1:-1]:
      for exp in shouldnt_be_outer_exp:
        mixtranch.append((convertPixelToPercent(exp["pixels"]), exp))
    
    #last tranch_item
    if len(match) > 1:
        mixtranch.append((convertPixelToPercent(match[-1]["pixels"]), match[-1]))

    #normalize pixel sizes
    pixelsum = 0
    mixtranch2 = []
    for tranch_item in mixtranch:
        pixelsum += tranch_item[0]
    for i,tranch_item in enumerate(mixtranch):
        if i < len(mixtranch)-1:
            tranch_item = ((convertPixelToPercent(tranch_item[0] * GROUP_MAX / pixelsum) - BORDER_WIDTH), tranch_item[1])
        else:
            tranch_item = ((convertPixelToPercent(tranch_item[0] * GROUP_MAX / pixelsum)), tranch_item[1]) 
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
temp_storage = []
for bill_i,bill in enumerate(bills):
    if bill_i == (BILLS_PER_COLUMN *2):
      temp_storage.reverse() #this flips the _text_ in the second column over, but not the bills themselves.
      bills_by_exp.extend(temp_storage)
    if bill_i >= BILLS_PER_COLUMN and bill_i < BILLS_PER_COLUMN *2:
      temp_storage.append([])
    else:
      bills_by_exp.append([])
    #if bill_i % 2 == 0:
    #  bill.reverse() #for the "boustrephedon"-style of layout.
    for tranch_index, tranch in enumerate(bill):
        for exp_index,expenditure in enumerate(tranch):
            #print str(expenditure) + "<br />"

            if bill_i >= BILLS_PER_COLUMN and bill_i < BILLS_PER_COLUMN *2:
              not_in_bill_yet = (expenditure[1]["safe_name"] not in [x["safe_name"] for x in temp_storage[bill_i-BILLS_PER_COLUMN]])
            else:
              not_in_bill_yet = (expenditure[1]["safe_name"] not in [x["safe_name"] for x in bills_by_exp[bill_i]])
            if not_in_bill_yet: 
                FONT_HEIGHT = (16.0 / GROUP_MAX) * 100 #needs to be a percent: make the number (i.e. "16" on this line) should be in pixels.

                expenditure = (expenditure[0], display_name_format(expenditure[1], NAME_CORRECTIONS))

                expenditure[1]["left"] = tranch_index * TRANCH_WIDTH #this is a percentage!!
                if expenditure[0] < FONT_HEIGHT+4:
                    expenditure[1]["left"] += 20

                expenditure[1]["top"] = 0

                if expenditure[1]["which_bill"] == 0:
                    expenditure[1]["leftover_tranches"] = expenditure[1]["whole_tranches"] #only if it isn't already set?
                tranches_left_in_this_bill = 5-tranch_index

                if expenditure[0] != 0 and expenditure[0] != 100:
                  tranches_left_in_this_bill = max(0, tranches_left_in_this_bill-1)
                expenditure[1]["whole_tranches_in_this_bill"] = min(expenditure[1]["leftover_tranches"], 5, tranches_left_in_this_bill)
                expenditure[1]["leftover_tranches"] -= min(expenditure[1]["leftover_tranches"], 5, tranches_left_in_this_bill)

                expenditure[1]["text_width"] = expenditure[1]["whole_tranches_in_this_bill"] * TRANCH_WIDTH
                if (expenditure[0] > FONT_HEIGHT+4 and expenditure[0] < GROUP_MAX and expenditure[1]["which_bill"] == 0 and (tranch_index + expenditure[1]["whole_tranches_in_this_bill"] < 5)) and bill_i % 2 == 1:
                    expenditure[1]["text_width"] += 20
                    #print "Adding 20 to " + expenditure[1]["safe_name"] + " such that " + str(expenditure[0]) + " > " + str(FONT_HEIGHT+4) +  "<br />"

                if expenditure[1]["whole_tranches_in_this_bill"] == 0:
                    expenditure[1]["text_width"] = 20

                if (bill_i >= BILLS_PER_COLUMN and bill_i < (BILLS_PER_COLUMN *2)) != (bill_i % 2 == 0):
                  #print expenditure[1]["safe_name"] + " was at " + str(expenditure[1]["left"]) +" with width " + str(expenditure[1]["text_width"]) + "<br />"
                  expenditure[1]["left"] = 100 - (expenditure[1]["left"] + (expenditure[1]["text_width"]))
                  #Reflect  the text for reversed bills.
                  if (expenditure[0] > FONT_HEIGHT+4 and expenditure[0] < GROUP_MAX and expenditure[1]["which_bill"] == 0 and (tranch_index + expenditure[1]["whole_tranches_in_this_bill"] < 5)) and False: #only if it's starting with a partial tranch
                      expenditure[1]["left"] -= 20
                      expenditure[1]["top"] = 0
                      #print "adjusting text <br />"


                if expenditure[1]["whole_tranches_in_this_bill"] == 0 or expenditure[0] > FONT_HEIGHT:
                    if exp_index == 1:
                        expenditure[1]["top"] = tranch[0][0]
                    elif exp_index == 2:
                        expenditure[1]["top"] = tranch[1][0] + tranch[0][0]
                    elif exp_index == 3:
                        expenditure[1]["top"] = tranch[1][0] + tranch[0][0] + tranch[2][0]
                if expenditure[1]["whole_tranches_in_this_bill"] == 0 and expenditure[0] < FONT_HEIGHT:
                    expenditure[1]["display_name_split"] = ""
                    #Don't display names if they don't fit at all.

                if bill_i not in expenditure[1]["bills"]:
                    expenditure[1]["bills"].append(bill_i)
                #print("<!--",expenditure[1]["safe_name"], "whole_tranches_in_bill", expenditure[1]["whole_tranches_in_this_bill"], "left", expenditure[1]["left"], "text_width", expenditure[1]["text_width"], "-->")
                if bill_i >= BILLS_PER_COLUMN and bill_i < (BILLS_PER_COLUMN *2):
                  #Flip the middle column over.
                  temp_storage[bill_i-BILLS_PER_COLUMN].append(deepcopy(expenditure[1]))
                else:
                  bills_by_exp[bill_i].append(deepcopy(expenditure[1]))
                expenditure[1]["which_bill"] += 1



    if (bill_i >= BILLS_PER_COLUMN and bill_i < (BILLS_PER_COLUMN *2)) != (bill_i % 2 == 0):
      #if it's in the left or right column, flip every other starting with index 0. If in the middle column, flip every other starting with index 1.
      #this convoluted logic makes the boustrephedon work in the middle column.
      bill.reverse() #for the "boustrephedon"-style of layout.
      #reflects the text in every other bill.
temp = bills[BILLS_PER_COLUMN:BILLS_PER_COLUMN*2]
temp.reverse()
bills = bills[:BILLS_PER_COLUMN] + temp + bills[BILLS_PER_COLUMN*2:]


template = env.get_template('viztemplate.py')

print template.render({'bills': bills, 'expenditures':expenditures, 
                        'GROUP_MAX': GROUP_MAX, 'bills_by_exp':bills_by_exp, 
                        'small_bills_and_coins': small_bills_and_coins, 
                        'small_bills': small_bills,
                        'coins': coins,
                        'BILLS_PER_SIDE': BILLS_PER_COLUMN,
                        'explanatory_paragraph': Markup(explanatory_paragraph),
                        'title': Markup(title),})

