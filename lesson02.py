from lesson01 import adder
print(adder(1,2))

rows = []
number_of_columns = 10
number_of_rows = 12
for row_index in range(number_of_rows):
    line=[]
    for column_index in range(number_of_columns):
        line.append("")
    rows.append(line)
rows[5][5] = "X"
for row in rows:
    print(row)