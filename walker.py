import os

def collectFile(path):
    folder = []
    list_files = []
    for item in os.walk(path):
        folder.append(item)

    for address, dirs, files in folder:
        for file in files:
            if file.endswith('.md'):
                list_files.append(os.path.join(address, file))
    return list_files
