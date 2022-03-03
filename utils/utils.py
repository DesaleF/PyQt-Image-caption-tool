import os


VALID_FORMAT = ('.BMP', '.GIF', '.JPG', '.JPEG', '.PNG', '.PBM', '.PGM', '.PPM', '.TIFF', '.XBM')  # Image formats supported by Qt

def getImages(folder):
    """ Get the names and paths of all the images in a directory. 
    Args:
        folder (str): directory with images
    """
    image_list = []
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if file.upper().endswith(VALID_FORMAT):
                im_path = os.path.join(folder, file)
                image_obj = {'name': file, 'path': im_path }
                image_list.append(image_obj)
    return image_list


def save_to_txt(path, txt):
    """save txt into .txt file

    Args:
        path (str): full path to txt file
        txt (str): the text/string to be saved
    """
    with open(path, 'w') as f:
        f.write(txt)
        
def load_text(path):
    """read .txt file and return the content

    Args:
        path (str): full path to .txt file
    """
    with open(path, 'r') as f:
        return str(f.read())
    