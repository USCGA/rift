import os
import warnings
from flask_uploads import UploadSet, ALL, IMAGES

# Upload Sets
ctf_files = UploadSet('ctf', ALL)
images = UploadSet('images', IMAGES)

#TODO Add some safety features to this bad boy.
def Delete(set: UploadSet, filename: str):
    try:
        os.remove(set.path(filename))
    except OSError as err:
        warnings.warn("Failed to remove file: \"" + filename + "\". \n" + err.message)
    