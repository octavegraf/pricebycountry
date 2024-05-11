import csv

# Creating CSV file
def new_file(csv_path, csv_line) :
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_line)
    print("CSV file created.")

# Adding line CSV file
def add_line(csv_path, csv_line) :
    with open(csv_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_line)
    print("Line added to CSV file.")
