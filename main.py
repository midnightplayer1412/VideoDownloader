import os
import yt_dlp
from tkinter import *

# Check download_video folder existing
def check_dir():
    print("Checking directory...")
    path = os.getcwd() + "\downloaded_video"
    if not os.path.exists(path):
        os.mkdir(path)
        print("Directory created successfully ...")
    else:
        print("Directory already exists ...")
    

if __name__ == "__main__":
    # Exception handling
    try:
        check_dir()
        root = Tk()
        root.mainloop()
    except Exception as e:
        print(f"Error occur: {e}")
    