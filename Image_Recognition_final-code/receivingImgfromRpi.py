import cv2
import preprocessingImages
import os

def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png')):
    """
    Get the latest image file in the given directory
    """
    valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
    # Filter out directories, no-extension, and wrong extension files
    valid_files = [f for f in valid_files if '.' in f and \
        f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

    if not valid_files:
        raise ValueError("No valid images in %s" % dirpath)

    return max(valid_files, key=os.path.getmtime)

def main():
    image = get_latest_image(dirpath=r'C:\Users\JiaEn\Desktop\yolov5-master\yolov5-master', valid_extensions=('jpg', 'jpeg', 'png'))
    # Read the image file as a numpy array
    picture = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    #print("")
    #print("Sending to image conversion, RGB to Grayscale...")

    #return preprocessingImg.rgbToGray(picture)
    return preprocessingImg.convertToPng(picture)
if __name__ == "__main__":
    main()