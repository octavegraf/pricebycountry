import csv
import sys

# Creating CSV file
def open_file(csv_path, csv_line, method) :
    with open(csv_path, method, newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_line)
    print("CSV file modified.")

def count_csv (csv_path, rows_columns) :
    with open(csv_path) as f:
        data = list(csv.reader(f))
    if rows_columns == "rows":
        return len(data)
    if rows_columns == "columns":
        return len(data)
    else:
        print("Error : rows or columns not defined.")
        sys.exit(1)