import pandas as pd
import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
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
        QMessageBox.information(None, 'Message', 'Chosen file: ' + selected_path + '\n\n\nfile completed, find it at errorsout.xlsx')
        app.quit()  # Close the application after selection

# Create the application object
app = QApplication(sys.argv)

# Create the main application window (QWidget)
root = QWidget()
root.setWindowTitle("Choose the needed file:")

# Create buttons to browse file and directory
file_button = QPushButton("Browse File", root)
file_button.clicked.connect(browse_file)
file_button.setFixedSize(400, 50)

# Arrange the buttons in a vertical layout
layout = QVBoxLayout(root)
layout.addStretch(1)
layout.addWidget(file_button, 0, alignment=PyQt5.QtCore.Qt.AlignHCenter)
root.setLayout(layout)

# place the image to make an app look more silly
image_path = '/home/antd/pyprojects/dublicates_Project/monkey.webp'
pixmap = QPixmap(image_path)
label = QLabel(root)
label.setPixmap(pixmap)
label.setScaledContents(True)
label.resize(700, 400)

# Show the main window
root.show()
root.resize(700, 500)

# Execute the application event loop
app.exec_()

# The event loop has finished, and we can access the selected path in the global variable
print("Selected path:", selected_path)

db = pd.read_excel(selected_path)

check = dict()
pibs = dict()

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

    pibs[row['inn']] = row['pib']

db_temp = []
xl_out = 'errorsout.xlsx'

with open ('errors.txt', 'w') as file:

    for i in check:

        temp = Counter(check.get(i))
        
        problems = [p for p, count in temp.items() if count > 1]
        if problems:
            db_temp.append({i: problems})

        if problems:
            file.write(str(i) + ' ' + str(pibs.get(i))+ ' -> ' + ' '.join(problems) + '\n')

transformed_data = dict()
for d in db_temp:
    for key, values in d.items():
        transformed_data[key] = [pibs.get(key)] + values

maxlen = max(len(values) for values in transformed_data.values())
for key in transformed_data:
    transformed_data[key].extend([None]*(maxlen - len(transformed_data[key])))


df_t = pd.DataFrame(transformed_data).T
db_out = pd.DataFrame(df_t)
db_out.to_excel(xl_out, header=False)
        