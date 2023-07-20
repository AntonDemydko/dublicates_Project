import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

from datetime import date, timedelta, datetime
from collections import Counter

def generate_dates(start_date, end_date): # generation of list of dates from start to end (included)
    delta = timedelta(days=1)
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += delta

selected_path = None

def browse_file():
    global selected_path
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(None, "Select File", "", "All Files (*);;Text Files (*.txt)", options=options)
    if file_path:
        print("Selected file:", file_path)
        selected_path = file_path
        app.quit()  # Close the application after selection

def browse_directory():
    global selected_path
    options = QFileDialog.Options()
    directory_path = QFileDialog.getExistingDirectory(None, "Select Directory", "", options=options)
    if directory_path:
        print("Selected directory:", directory_path)
        selected_path = directory_path
        app.quit()  # Close the application after selection

# Create the application object
app = QApplication(sys.argv)

# Create the main application window (QWidget)
root = QWidget()
root.setWindowTitle("File Dialog Example")

# Create buttons to browse file and directory
file_button = QPushButton("Browse File", root)
file_button.clicked.connect(browse_file)

directory_button = QPushButton("Browse Directory", root)
directory_button.clicked.connect(browse_directory)

# Arrange the buttons in a vertical layout
layout = QVBoxLayout()
layout.addWidget(file_button)
layout.addWidget(directory_button)
root.setLayout(layout)

# Show the main window
root.show()

# Execute the application event loop
app.exec_()

# The event loop has finished, and we can access the selected path in the global variable
print("Selected path:", selected_path)

db = pd.read_excel(selected_path)

check = dict()


for index, row in db.iterrows():
    startdate = date(int(str(row['from']).split('.')[-1]), # year transformed from excel format dd.mm.yyyy
                     int(str(row['from']).split('.')[-2]), # month transformed from excel format dd.mm.yyyy
                     int(str(row['from']).split('.')[-3])) # day transformed from excel format dd.mm.yyyy
    
    enddate = date(int(str(row['to']).split('.')[-1]), # year transformed from excel format dd.mm.yyyy
                   int(str(row['to']).split('.')[-2]), # month transformed from excel format dd.mm.yyyy
                   int(str(row['to']).split('.')[-3])) # day transformed from excel format dd.mm.yyyy
    
    datelist = [str(d) for d in generate_dates(start_date=startdate, end_date=enddate)] # creation list of dates

    if row['inn'] not in check:
        
        check[row['inn']] = datelist
    else:
        check[row['inn']] += datelist

db_temp = []
xl_out = 'errorsout.xlsx'

with open ('errors.txt', 'w') as file:

    for i in check:

        temp = Counter(check.get(i))
        
        problems = [p for p, count in temp.items() if count > 1]
        if problems:
            db_temp.append({i: problems})

        if problems:
            file.write(str(i) + ' -> ' + ' '.join(problems) + '\n')

transformed_data = dict()
for d in db_temp:
    for key, values in d.items():
        transformed_data[key] = values

maxlen = max(len(values) for values in transformed_data.values())
for key in transformed_data:
    transformed_data[key].extend([None]*(maxlen - len(transformed_data[key])))


df_t = pd.DataFrame(transformed_data).T
db_out = pd.DataFrame(df_t)
db_out.to_excel(xl_out, header=False)
        