import os,shutil

def clear(filepath):
    files = os.listdir(filepath)
    for fd in files:
        cur_path = os.path.join(filepath,fd)
        if os.path.isdir(cur_path):
            if fd == "__pycache__":
                shutil.rmtree(cur_path)
                #print(cur_path)
            elif os.path.isdir(cur_path):
                clear(cur_path)
clear(os.getcwd())

