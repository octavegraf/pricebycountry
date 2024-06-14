import csv
import sys

# Creating CSV file
def open_file(csv_path, csv_line, method):
    with open(csv_path, method, newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_line)
    print("CSV file modified.")

# Counting rows and columns CSV file
def count_csv (csv_path, rows_columns):
    with open(csv_path) as csv_file:
        data = list(csv.reader(csv_file))
    if rows_columns == "rows":
        return len(data)
    if rows_columns == "columns":
        return len(data[0])
    else:
        print("Error : rows or columns not defined.")
        sys.exit(1)

def read_element_csv(csv_path, row, column):
    with open(csv_path, mode='r', newline='') as csv_file:
        data = list(csv.reader(csv_file))
        return data[row][column]
    
def add_chatgpt_data(csv_path, row, chatgpt_response):
    with open(csv_path, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)
    price, currency = chatgpt_response.split(',')
    price = price.strip()
    currency = currency.strip()
    rows[row].extend([price, currency])
    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(rows)