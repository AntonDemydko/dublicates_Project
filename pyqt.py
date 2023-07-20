import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

# Global variable to store the selected path
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
