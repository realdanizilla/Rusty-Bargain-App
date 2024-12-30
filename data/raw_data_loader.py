import csv

# Define your CSV file and the output SQL file
csv_file = 'car_data.csv'
sql_file = '../raw_car_data.sql'
table_name = 'bronze_car_data'

# Open the CSV file and the SQL file
with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile, open(sql_file, 'w', encoding='utf-8') as sqlfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Get the header row

    # Write the INSERT statements
    for row in reader:
        # Create a list of values
        values = []
        for value in row:
            if value == '':
                values.append('NULL')  # Keep empty values as empty strings
            else:
                #values.append(f"'{value}'")  # Wrap non-empty values in single quotes
                values.append(value)

        # Join the values into a single string
        values_str = ','.join(values)
        sqlfile.write(f"INSERT INTO {table_name} ({','.join(headers)}) VALUES ({values_str});\n")

print(f"SQL file '{sql_file}' has been created.")