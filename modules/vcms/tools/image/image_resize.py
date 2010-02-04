# -- GENERAL FUNCTION
# -- ----------------
import os
from django.core.files.storage import FileSystemStorage
import Image as ImageLib

def _save_thumbnail(self, fileName, url="uploadto/misc/", size=(100,40), genthumbnail=True):
    if self.file:
        #filename = fileName
        if genthumbnail:
            fs = FileSystemStorage()
            image = ImageLib.open(str(fileName))

            original_ratio = image.size[0] / image.size[1]
            required_ratio = size[0] / size[1]

            if original_ratio > required_ratio:
                # The image is too large
                correct_width = int(required_ratio / original_ratio * image.size[0])
                # Computing the bounding box
                left = (image.size[0] - correct_width) // 2
                right = left + correct_width
                upper = 0
                lower = image.size[1] - 1   # Pixels are indexed from zero
                bounding_box = (left, upper, right, lower)
                image = image.crop(bounding_box)
            elif original_ratio < required_ratio:
                # The image is too high
                correct_height = int(original_ratio / required_ratio * image.size[1])
                # Computing the bounding box
                left = 0
                right = image.size[0] - 1   # Pixels are indexed from zero
                upper = (image.size[1] - correct_height) // 2
                lower = upper + correct_height
                bounding_box = (left, upper, right, lower)
                image = image.crop(bounding_box)

            image.thumbnail(size)
            filename = self.file.name.split("/")[-1].split('.')
            thumbname = str(filename[0] + "_tn." + str(filename[1]))
            image.save(fs.location + "/" + url + thumbname)
            return url + thumbname
            
def save_resized_image(self, fileName, url="uploadto/misc/", size=(100,40), genthumbnail=True ):
    try:
        return _save_thumbnail(self, fileName, url, size, genthumbnail)
    except:
        return False
    