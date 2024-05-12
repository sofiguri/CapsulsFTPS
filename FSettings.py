import os
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
folder_path = os.path.join(os.getcwd(), 'Folder_for_test')
os.makedirs(folder_path, exist_ok=True)
log_path = os.path.join(os.getcwd(), 'log_file.txt')
User_path = os.path.join(os.getcwd(), 'User_file.txt')