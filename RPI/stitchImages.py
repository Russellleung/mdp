from imutils import paths
from PIL import Image
import shutil
import os

def stitching():

  # replace with new directory
  image_folder = r'C:\Users\ASUS\Desktop\mdp\mdpv1_yolov5\stitchedImages\rawCaptures'
  imagePaths = list(paths.list_images(image_folder))
  images = [Image.open(x) for x in imagePaths]
  widths, heights = zip(*(i.size for i in images))

  total_width = sum(widths)
  max_height = max(heights)

  new_im = Image.new('RGB', (total_width, max_height))

  x_offset = 0
  for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]

  new_im.save('stitchedImages/stitchedOutput.png', format='png')

def copyCapture():
  movdir = r"C:\Users\ASUS\Desktop\mdp\mdpv1_yolov5\runs\detect"
  basedir = r"C:\Users\ASUS\Desktop\mdp\mdpv1_yolov5\stitchedImages\rawCaptures"
  # Walk through all files in the directory that contains the files to copy
  ii = 2
  for root, dirs, files in os.walk(movdir):
      for filename in files:
          # I use absolute path, case you want to move several dirs.
          old_name = os.path.join( os.path.abspath(root), filename )
          #C:\Users\ASUS\Desktop\mdp\mdpv1_yolov5\runs\detect\exp\image.jpg

          # Separate base from extension
          base, extension = os.path.splitext(filename)

          # Initial new name
          new_name = os.path.join(basedir, filename)
          #C:\Users\ASUS\Desktop\mdp\mdpv1_yolov5\stitchedImages\rawCaptures\image.jpg

          # If folder basedir/base does not exist
          if not os.path.exists(basedir):
              print (basedir, "not found" )
              continue    # Next filename
          elif not os.path.exists(new_name):  # folder exists, file does not, just copy in
              shutil.copy(old_name, new_name)
          else:  # folder exists, file exists as well
              while True:
                  new_name = os.path.join(basedir, base + "_" + str(ii) + extension)
                  if not os.path.exists(new_name):
                    shutil.copy(old_name, new_name)
                    print ("Copied", old_name, "as", new_name)
                    break 
              ii += 1

def clearImages(folder):
  for filename in os.listdir(folder):
      file_path = os.path.join(folder, filename)
      try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
              shutil.rmtree(file_path)
      except Exception as e:
          print('Failed to delete %s. Reason: %s' % (file_path, e))

# clearImages(r'C:\Users\ASUS\Desktop\mdp\mdpv1_yolov5\stitchedImages\rawCaptures')
# clearImages(r'C:\Users\ASUS\Desktop\mdp\mdpv1_yolov5\runs\detect')
# copyCapture()
# stitching()