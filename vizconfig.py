"""
Configuration file for BudgetViz
by Jeremy B. Merrill
"""
global TOTAL_PER_STUDENT, LARGEST_BILL, NAME_CORRECTIONS, TRANCHES_PER_BILL

#The total amount of money to be represented. (Often per capita spending.)
TOTAL_PER_STUDENT = 276.30 

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
