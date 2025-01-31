
import time
import json
import yaml
import collections
import zipfile
from io import BytesIO
from PIL import Image
import os


def create_zip_fun(folder_path):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    buffer.seek(0)
    return buffer
