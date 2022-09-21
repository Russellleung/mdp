#clone YOLOv5 and 
'''pip install -qr requirements.txt
!git clone https://github.com/ultralytics/yolov5  # clone repo
%cd yolov5
%pip install -qr requirements.txt # install dependencies
'''

import torch
import subprocess
import json

print(f"Setup complete. Using torch {torch.__version__} ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")

p = subprocess.getstatusoutput("python detect.py --weights best_v3.pt --save-conf --img 640 --conf 0.1 --source ./imagezmq_images") 
print(p[1])
output = p[1]

with open('outputs/output_test.txt', 'w') as f:    # path to output .txt file
  f.write(output)


def process_output(path = None, string = None):

  if path==None and string==None:
    print('No output specified for processing.')
    return
  elif path!=None and string!=None:
    print('Multiple outputs specified for processing.')
    return
  elif path!=None:
    f = open(path, 'r')
    # split each line into a string, all in 1 list
    raw = f.read().split('\n')
  else:
    raw = string.split('\n')
  
  #a list of only strings of image lines in output
  raw = [line for line in raw if (line[:5]=="image")]
  output = {}
  detected_classes = []
  for line in raw:
    #split the line into words
    line_split = line.split()
    name = [i for i in line_split if i.endswith(".jpg:")][0]
    print(name)
    name = name[:-1] #remove : from image name
    # no classes detected
    #last word
    if line_split[-1].endswith("ms"):
      detections = None
      confidences = None
    # classes detected
    else:
      for e in line_split:
        if e.endswith("ms"):
          speed = e
      # from aft 640x480 to before speed
      raw_classes = line_split[line_split.index("640x640")+1:line_split.index(speed)]
      confidences = line_split[line_split.index(speed)+1:]
      #no. of classes detected in the pic
      class_num = [int(i) for i in raw_classes if not i.endswith(',')]
      #remove ',' only int
      #classes detected in 1 pic
      classes = [int(''.join(filter(str.isdigit, i))) for i in raw_classes if i.endswith(',')]
      classes_with_duplicates = []
      for i in range(len(classes)):
        for dup in range(class_num[i]):
          classes_with_duplicates.append(classes[i])
      detections = []
      assert(len(classes_with_duplicates) == len(confidences))
      for i in range(len(confidences)):
        #added
        detected_classes.append(classes_with_duplicates[i])
        detections.append([classes_with_duplicates[i], float(confidences[i])])
    output[name] = detections
    print(detections)
    print(confidences)
  # return output
  if detections:
    print(detections[0][0])
    return detections[0][0] 
  else:
    return 1

  # return detected_classes

# print(process_output(path = "outputs/output_test.txt"))
# print(json.dumps(process_output(path = "outputs/output_test.txt"), indent=4))    # path to output .txt file

