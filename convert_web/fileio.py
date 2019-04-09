from zipfile import ZipFile
from os.path import isfile, basename


def write_file(file_path, data):
    with open(file_path, "wb") as f:
        f.write(data)


def write_zip(zip_path, *paths):
    with ZipFile(zip_path, "w") as zip_file:
        for path in paths: 
            if isfile(path):
                zip_file.write(path, basename(path))


