import os

# USD File Template
class USDFileTemplate:
    def __init__(self, filePath):
        # Check if  the file exists
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"File {filePath} does not exist.")
        
        self.filePath = filePath
        self.contents = None
        # Open the file and read the contents
        with open(filePath, 'r') as file:
            self.contents = file.read()

    # Replace content from the template
    def replace(self, oldStr, newStr):
        if self.contents is None:
            return
        
        # Replace the old string with the new string in the contents
        self.contents = self.contents.replace(oldStr, newStr)

    def save(self, newFilePath=None):
        # If newFilePath is not provided, save to the original file
        if newFilePath is None:
            newFilePath = self.filePath
        
        # Write the modified contents back to the file
        with open(newFilePath, 'w') as file:
            file.write(self.contents)
    