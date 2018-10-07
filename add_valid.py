import csv
import difflib

# input address provided by address standardization tool
standard_add = ['1775',"RUSKIN","COURT","MIAMI","FLORIDA",'33180','1732']

STREET_NUM = 0
STREET_NAME = 1
SUFFIX = 2
CITY = 3
STATE = 4
ZIP = 5
ZIP4 = 6

# validating address is real or fake by comparing the standardized address with main database. Assuming city and state are valid and correct
def validate_address(standard_add):
    with open('/home/vatsal/Downloads/HackRU/MOCK_DATA.csv') as csv_file:
        file = csv.reader(csv_file, delimiter=',')
        line = 0
        for row in file:
            if line == 0:
                line += 1
            else:
                if standard_add[STATE] == row[STATE] and standard_add[CITY] == row[CITY]:
                    if (standard_add[STREET_NUM] == row[STREET_NUM]) and (standard_add[STREET_NAME] == row[STREET_NAME]) and (standard_add[ZIP] == row[ZIP]):
                        return True
                    else:
                        continue
                else:
                    line += 1

print(validate_address(standard_add))

# similarity match compares the validated address (input) from above for each address field
# and returns the most probable address that's closest to a valid and real address

def similarity_match(pri_add, predirect, street, suffix, postdirect, sec_add_identify, sec_add, city, state, zip, zip4):

# start by comparing each input field in input address with corresponding field in a list of matched addresses
# Prioritize by state, zip, city, street name, etc.
# store each field comparison value for every similarity comparison.
    difflib.SequenceMatcher(None, pri_add[0][1], street[0][1]).ratio()
# the field with highest value according to priority is stored and the others are discarded.
# we continue by comparing the next field, and storing maximum priorities.
# once all the fields are compared, the max value with similarity matching is declared as the most probable real address.




