import os
import shutil

def save_uploaded_file(upload_dir: str, file) -> str:
    file_location = os.path.join(upload_dir, file.filename.replace(" ", "_"))
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_location

def delete_file(path: str):
    if os.path.exists(path):
        os.remove(path)
