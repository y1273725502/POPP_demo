import os


folder_path = r'C:\Users\12737\Documents\Capstone_project'


file_names = os.listdir(folder_path)


py_files = [file for file in file_names if file.endswith('.py')]

print(py_files)