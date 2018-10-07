import csv

standard_add = [1175,"RUSKIN","COURT","MIAMI","FLORIDA",33180,1732]

STREET_NUM = 0
STREET_NAME = 1
SUFFIX = 2
CITY = 3
STATE = 4
ZIP = 5
ZIP4 = 6

max_val = None

with open('/home/vatsal/Downloads/HackRU/MOCK_DATA.csv') as f:
    reader = csv.reader(f)
    next(reader)
    max_val = max(int(column[STREET_NUM].replace(',', '')) for column in reader)

def validate_address(standard_add):
    with open('/home/vatsal/Downloads/HackRU/MOCK_DATA.csv') as csv_file:
        file = csv.reader(csv_file, delimiter=',')
        line = 0
        for row in file:
            if line == 0:
                line += 1
            else:
                if standard_add[STATE] == row[STATE] and standard_add[CITY] == row[CITY]:
                    if (standard_add[STREET_NUM] <= max_val) and (standard_add[STREET_NAME] == row[STREET_NAME]) and (standard_add[ZIP] == row[ZIP]):
                        return True
                    else:
                        continue
                else:
                    line += 1

print(validate_address(standard_add))



