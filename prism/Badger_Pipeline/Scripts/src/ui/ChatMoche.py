
import os
import random

def getUnChatMoche() :
    # Get the current file path
    file = os.path.abspath(__file__)
    # Get the parent directory
    parent_dir = os.path.dirname(file)
    parent_dir = os.path.dirname(parent_dir)
    parent_dir = os.path.dirname(parent_dir)
    # Get the rc/chat_moche directory
    chat_moche_dir = os.path.join(parent_dir, "rc", "chat_moche")
    chat_moche_dir = chat_moche_dir.replace("\\", "/")

    print("Chat Moche Directory:", chat_moche_dir)
    # Get the list of all the files .png in the directory
    files = [f for f in os.listdir(chat_moche_dir) if f.endswith('.png')]

    # Get a random file from the list
    if files:
        random_file = random.choice(files)
        # Return the full path of the random file
        return os.path.join(chat_moche_dir, random_file).replace("\\", "/")
    else:
        print("No .png files found in the chat_moche directory.")
        # return ""
        return ""

