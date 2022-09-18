import cv2
import detect
import os

def rgbToGray(picture):
    # Conversion from RGB to gray
    picture = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
    print("Sending to image resizing...")

    return reSize(picture)

def reSize(picture):
    # Resizing image to 544 x 544
    width = 544
    height = 544
    dim = (width, height)
    picture = cv2.resize(picture, dim, interpolation = cv2.INTER_AREA)
    print("Sending to image histogram equalization...")

    return histEqualize(picture)

def histEqualize(picture):
    # Equalize histogram so that it will not be too dark or too bright
    picture = cv2.equalizeHist(picture)
    print("Sending to image conversion, numpy array to jpg...")

    #return flipImages(picture)
    return convertToPng(picture)

def flipImages(picture):  # only if you put the camera upside down
    picture = cv2.flip(picture, 0)
    print("Sending to image conversion, numpy array to jpg...")

    return convertToPng(picture)

def convertToPng(picture):
    # Convert from numpy array to a .png file
    output_dir = os.path.join('runs', 'output', 'output.png')
    cv2.imwrite(output_dir, picture)
    print("Sending to image detection...")

    # Parse the .png file into the YOLOv5 model
    results_dir = os.path.join('runs', 'results')
    return detect.run(weights='60epoch_RGB.pt',
                      source=output_dir,
                      imgsz=544,
                      conf_thres=0.25,
                      iou_thres=0.25,
                      max_det=1,
                      device='',
                      view_img=False,  # show results
                      save_txt=False,  # save results to *.txt
                      save_conf=False,  # save confidences in --save-txt labels
                      save_crop=False,  # save cropped prediction boxes
                      nosave=False,  # do not save images/videos
                      classes=None,  # filter by class: --class 0, or --class 0 2 3
                      agnostic_nms=False,  # class-agnostic NMS
                      augment=False,  # augmented inference
                      visualize=False,  # visualize features
                      update=False,  # update all models
                      project=results_dir,  # save results to project/name
                      exist_ok=False,  # existing project/name ok, do not increment
                      line_thickness=3,  # bounding box thickness (pixels)
                      hide_labels=False,  # hide labels
                      hide_conf=False,  # hide confidences
                      half=False,   # use FP16 half-precision inference
                      )