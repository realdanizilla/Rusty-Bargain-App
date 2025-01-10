import csv
from datetime import datetime

# Define your CSV file and the output SQL file
csv_file = 'data/car_data.csv' 
sql_file = 'raw_car_data.sql'
table_name = 'bronze_car_data'

# Define the columns that need datetime formatting
datetime_columns = ['DateCrawled', 'DateCreated', 'LastSeen']
string_columns = ['VehicleType', 'Gearbox', 'Model', 'FuelType', 'Brand', 'NotRepaired']

# Open the CSV file and the SQL file
with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile, open(sql_file, 'w', encoding='utf-8') as sqlfile:
    reader = csv.DictReader(csvfile)
    headers = reader.fieldnames  # Get the header row

    # Write the INSERT statements
    for row in reader:
        values = []
        for col in headers:
            value = row[col]
            if value == '':
                values.append('NULL')  # Handle empty values as NULL
            elif col in datetime_columns:
                # Parse and reformat datetime columns
                try:
                    parsed_date = datetime.strptime(value, '%d/%m/%Y %H:%M')  
                    formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')  # Format for PostgreSQL
                    values.append(f"'{formatted_date}'")
                except ValueError:
                    # Handle invalid datetime formats gracefully
                    values.append('NULL')
            elif col in string_columns:
                try:
                    values.append(f"'{value}'")
                except ValueError:
                    values.append('NULL')
            else:
                # Keep non-empty values as they are
                values.append(value)

        # Join the values into a single string
        values_str = ','.join(values)
        sqlfile.write(f"INSERT INTO {table_name} ({','.join(headers)}) VALUES ({values_str});\n")

print(f"SQL file '{sql_file}' has been created.")
