"""
Configuration file for BudgetViz
by Jeremy B. Merrill
"""
global TOTAL_PER_CAPITA, LARGEST_BILL, NAME_CORRECTIONS, TRANCHES_PER_BILL

#The total amount of money to be represented. (Often per capita spending.)
TOTAL_PER_CAPITA = 276.30 

#The dollar value of the largest bill. Default is 20 for a twenty dollar bill.
LARGEST_BILL = 20

# The names of some budget line items may be too large to fit into their respective portion of the bill.
# Enter shortened versions of the names here; the full name will be displayed on the tooltip and 
# the shortened version will be displayed on the bill itself.
# Put each substitution line inside the curly braces (these things {} ), in the format:
# "'Full long name': 'Shortname', " including the single quotes and the comma (') but not the double quotes (")
NAME_CORRECTIONS = {"Office Supplies": "Of.Supp",
                    "President's Room & Board": "Prez's Room & Board",
                    "President's Fund": "Prez's Fund",
                    "Event(s) Damages": "Event Damages",
                    "ASCMC Senate": "Senate",
                    "Campus Security (Private)": "Private Security",
                   }

# Each bill is divided into a certain number of vertical portions. How many tranches should be in each bill?
# Default: 5
TRANCHES_PER_BILL = 5


#The max number of bills per column.
BILLS_PER_COLUMN = 6


#---
#
# Put budget information here.
#
#---
title="How Does <span id=\"ascmc\">ASCMC</span> Spend Your Student Fees?"

explanatory_paragraph="""
ASCMC takes in $245 per student (<a href="http://www.claremontportside.com/?p=3922">$10 more than last year</a>) in student fees each year and spends $276.30 per capita. This visualization displays how much ASCMC spends on each line item.

According to ASCMC President Jessica Mao '12, the budget created by ASCMC's budget committee and approved by the ASCMC Senate and Executive Board. ASCMC is funded primarily by student fees disbursed by the Dean of Students office, half in September and half in January. The only condition ASCMC must meet before receiving its disbursements from CMC is to meet with the Deans, Mao says.
"""

expenditures = [] #a list of dicts repring all expenditures
expenditures.append({"display_name":"General Fund", "cost":1285,"safe_name":"general_fund", "blurb":"General Fund monies are disbursed \"at the discretion of the ASCMC executive board for providing funding for various groups that come before the board requesting money\", Mao said."}) #TODO ask JMao for examples
expenditures.append({"display_name":"Campus Security (Private)", "cost":15000, "safe_name":"private_sec", "blurb":"blah blah"}) #This is changing in rebudgeting.
expenditures.append({"display_name":"White Party", "cost":4000, "safe_name":"white", "blurb":"blah blah"})
expenditures.append({"display_name":"President's Fund", "cost":2500, "safe_name":"pres_fund", "blurb":"blah blah"})
expenditures.append({"display_name":"Forum", "cost":6000, "safe_name":"forum", "blurb":"The <a href='http://cmcforum.com'><em>CMC Forum</em></a> is ASCMC's official publication, covering student opinion, news and lifestyle at CMC. The Forum's Editor-in-Chief is Heath Hyatt '12. Hyatt's stipend of $250 is not included in this line item, but stipends paid to other editors or to writers are. The Forum also receives some funds from advertising."}) #TODO check stipend info, check advertising info.
expenditures.append({"display_name":"Contingency", "cost":25000, "safe_name":"contingency", "blurb":"blah blah"})
expenditures.append({"display_name":"Event(s) Damages", "cost":5000, "safe_name":"damages", "blurb":"blah blah"})
expenditures.append({"display_name":"Student Security", "cost":5000, "safe_name":"student_sec", "blurb":"blah blah"}) #Note that director of student sec recieves stipend from stipends line item
expenditures.append({"display_name":"Stipends", "cost":9400, "safe_name":"stipends", "blurb":"""Various ASCMC officers receive stipends, as specified in the ASCMC Constitution."""}) #TODO link to CPS coverage of Const amends.
expenditures.append({"display_name":"5C Clubs (Total)", "cost":25165, "safe_name":"clubs_5c", "blurb":""}) #Note CPS funding
expenditures.append({"display_name":"CMC Clubs (Total)", "cost":39150, "safe_name":"clubs_cmc", "blurb":"blah blah"}) 
"""<ul><li>CFO Stagory Athena '11 receives $500 per semester</li> <li>Vice President Aditya Pai '13 receives $400 per semester.</li><li>SAC, DAC, SLC and COC NAME NAMENAMENAME receive $300 each.</li><li>Class of 2012 President Mary Doyle and 2013 President Lannie Rosenfield each recieve $300 per semester.</li><li>The Director of Student Security, NAME NAME, receives $250 per semester.</li><li>The President Pro Tempore, Miles Lifson, receives $100 per semester.</li><li> Executive Secretary, which is currently unfilled after former Alexandra Cooke was elected to SLC Chair, receives $100 per semester.</li><li>The 2014 and 2015 Presidents, NAME NAME '14 and NAME NAME '15 respectively, receive $200 per semester.</li><li>The webmaster, Neal Kemp '13, receives $100 per semester.</li></li>The Property Manager, NAME NAME, receives $100 per semester.</li><li>The <em>Forum</em> editor-in-chief Heath Hyatt '12 receives $100 per semester.</li><li>The <em>Ayer</em> editors-in-chief Carlos Rivas '12 and Heidi Carlson '12 receive $250 per semester, but only if the <em>Ayer</em> meets or exceeds its expenses. This provision was enacted as part of <a href=\"http://www.claremontportside.com/?p=3973\">a package of constitutional reforms</a> passed in the Spring of 2011.</li></ul>"""

################################
# Andy / "We're writing about ASCMC's budget. What do you plan on doing with your budget this year? Kthxbye."
################################

expenditures.append({"display_name":"Senate Student Trips", "cost":2000,"safe_name":"senate_trips", "blurb":"The ASCMC Senate has a separate fund for funding student trips to, for instance, Harvard MUN."}) #check with Pai for this example
expenditures.append({"display_name":"Campus Organizations Chair Fund", "cost":8500,"safe_name":"co_chair", "blurb":"The CO Chair, Stagory Athena '11, has a separate fund to disburse to clubs at his/her whim."})
expenditures.append({"display_name":"Class 2012", "cost":18000,"safe_name":"class_2011", "blurb":"The Senior Class budget. Spent by the Senior Class President Mary Doyle '12 on parties, such as the 100 Days and 200 Days parties."}) #email Mary re: priorities
expenditures.append({"display_name":"Class 2013", "cost":3500, "safe_name":"class_2012", "blurb":"The Junior Class budget. Spent by the Junior Class President, Lannie Rosenfield '13."}) #email Lannie for her priorities
expenditures.append({"display_name":"Monte Carlo", "cost":12000, "safe_name":"monte", "blurb":"Monte Carlo blah blah"}) #This is planned by the Jr. class prez; email to Lannie about this too. I can't imagine there's much to be said beyond "Party, gambling themed." Where are you going to hold it?
expenditures.append({"display_name":"Class 2014", "cost":3000, "safe_name":"class_2013", "blurb":"The Sophomore Class budget. Spent by the Sophomore Class President, Gavin Landgraf '14."}) #email Gavin for his priorities
expenditures.append({"display_name":"Class 2015", "cost":2000, "safe_name":"class_2014", "blurb":"The Freshman Class budget. Spent by their president, when he or she is elected."}) #who's their president again?
expenditures.append({"display_name":"SAC", "cost":17500, "safe_name":"sac", "blurb":"The Student Activities Chair's budget. The SAC, Will Brown '12, plans many of the weekend evening events."})
expenditures.append({"display_name":"DAC", "cost":8500, "safe_name":"dac", "blurb":"The Dorm Activities Chair's budget. The DAC, Clare Riva '13, plans TNC."})
expenditures.append({"display_name":"SLC", "cost":11500, "safe_name":"slc", "blurb":"The Student Life Chair's budget. Alexandra Cooke '14 is the newly-elected SLC chair, after Burke Zanft '14 resigned, citing his desire to study abroad in the spring."})
expenditures.append({"display_name":"Ayer", "cost":29000, "safe_name":"ayer", "blurb":"blah blah"})

####################################
# Done
####################################
expenditures.append({"display_name":"President's Room & Board", "cost":7000, "safe_name":"pres_room", "blurb":"Each ASCMC President's room and board fees are paid for, half by ASCMC and half by the Dean of Students' office, in lieu of a stipend. President Mao said that she has chosen to only have her housing fees paid for, which costs ASCMC the same amount as it paid for former President Tammy Phan '10 during the 2010-2011 school year."})
expenditures.append({"display_name":"Office Supplies", "cost":750, "safe_name":"office_supplies", "blurb":"According to Mao, \"more than half\" of ASCMC's Office Supplies line item is spent on accounting supplies, like stamps and envelopes for checks. It also covers web hosting for ASCMC-hosted sites (which includes the <em>Port Side</em>)."})
expenditures.append({"display_name":"ASCMC Senate","cost":10000,"safe_name":"senate", "blurb":"ASCMC Senate meets on Mondays and is open to students elected by their dorms and students who attend most of the meetings. Aditya Pai '13 is the Senate President (and ASCMC Vice President). Senate approves budgets and resolutions, as well as providing funding for campus groups. New this year under Pai's administration is \"Open Senate\", which Pai describes as \"a 10-15 segment called Open Senate, during which time any CMCer -- Senator or not -- can bring up any campus issue for discussion.\" He writes in an all-school email that Open Senate can be used for \"Anything, really: eloquent tirades about the lack of parking, odes to the God-like competence of Elizabeth Morgan, and whatever else you want to complain/applaud/rant about on campus. The idea is to allow students to identify areas of improvement, and organize Senators to work on solutions.\""})
expenditures.append({"display_name":"Off-Campus Sports Events", "cost":3500, "safe_name":"offcampus_sports", "blurb":"\"This was mainly created for a Dodgers game trip.\", says Mao, but, she says, ASCMC is open to suggestions. \"The ASCMC executive board decides with the SLC chair usually playing a central role in the planning\", she adds."})
expenditures.append({"display_name":"Wedding Party", "cost":12000, "safe_name":"wedding", "blurb":"The Wedding Party, a tradition started in 2009, features all the accoutrement of a real wedding: catered dinner, a band, free-flowing bubbly beverages and even a balloon man. Tickets cost $20 (in addition to the $12,000 spent by ASCMC) and only 400 are available, according to Mao, though the live music and dance party after dinner are open to all students with or without a ticket."})
expenditures.append({"display_name":"Dorms Total", "cost":31500, "safe_name":"dorms", "blurb":"Each dorm receives funds for planning dorm events, like parties or dorm-wide snacks. Each dorm receives a set amount per resident."})
