from numpy.lib.function_base import diff
from data_aug.data_aug import *
from data_aug.bbox_util import *
import numpy as np 
import cv2 
import matplotlib.pyplot as plt 
import pickle as pkl
import random
# %matplotlib inline
root_dir = "data/train_data/"
list_imgs = os.listdir(root_dir)
clss = [0]
for i in range(137):
    clss.append(0)
def box_to_str(box):
    box = box.tolist()
    print(box)
    s = ''
    for arr in box:
        x = float(arr[0] + arr[2]) / 2.0
        y = float(arr[1] + arr[3]) / 2.0
        w = float(arr[2] - arr[0])
        h = float(arr[3] - arr[1])
        cls = arr[4]
        clss[cls] += 1
        s += str(cls) + ' ' + str(x/320) + ' ' + str(y/64) + ' ' + str(w/320) + ' ' + str(h/64) + '\n'
    print(s)
    return s


def get_bbox(path):
    txt = open(path, "r")
    box = []
    for line in txt:
        arr = line.split()
        x1 = int((float(arr[1]) - float(arr[3]) / 2) * 320)     
        x2 = int((float(arr[1]) + float(arr[3]) / 2) * 320)
        y1 = int((float(arr[2]) - float(arr[4]) / 2) * 64)
        y2 = int((float(arr[2]) + float(arr[4]) / 2) * 64)
        ln = [x1, y1, x2, y2, int(arr[0])]
        box.append(ln)
    
    # print(box)
    # print(np.array(box))
    return np.array(box)

counter = 1

for img_path in list_imgs:
    if(img_path[-4:]==".txt"):
        continue
    path = os.path.join(root_dir, img_path)
    # print(path)
    txt_path = os.path.join(root_dir, img_path.replace(".jpg", ".txt"))
    bboxes = get_bbox(txt_path)
    # print(bboxes, type(bboxes))
    # exit()
    img = cv2.imread(path)  #opencv loads images in bgr. the [:,:,::-1] does bgr -> rg
    if counter % 8 == 1 :
        img_, bboxes_ = RandomTranslate(0.3, diff = True)(img.copy(), bboxes.copy())
    # elif counter % 8 == 2 :
    #     img_, bboxes_ = RandomHorizontalFlip(1)(img.copy(), bboxes.copy())
    elif counter % 8 == 3 :
        img_, bboxes_ = RandomScale(0.3, diff = True)(img.copy(), bboxes.copy())
    elif counter % 8 == 4 :
        img_, bboxes_ = RandomHSV(hue =(20,100), saturation=(0,200), brightness=(0,150))(img.copy(), bboxes.copy())
    elif counter % 8 == 5 :
        img_, bboxes_ = RandomShear(0.3)(img.copy(), bboxes.copy())
    # elif counter % 8 == 6:
    #     img_, bboxes_ = Resize((160,32))(img.copy(), bboxes.copy())
    else:
        img_, bboxes_ = RandomRotate(random.randrange(10,20))(img.copy(), bboxes.copy())
    # cv2.rectangle(img,(bboxes[5][0],bboxes[5][1]), (bboxes[5][2],bboxes[5][3]),(255,0,0),2)
    # # print("org_cls", bboxes[5][4])
    # cv2.rectangle(img_,(bboxes_[5][0],bboxes_[5][1]), (bboxes_[5][2],bboxes_[5][3]),(255,0,0),2)
    #print(bboxes_)
    string = box_to_str(bboxes_)
    ann_path = os.path.join("result", img_path.replace(".jpg", ".txt"))
    file2 = open(ann_path , "w" )
    print(ann_path)
    file2.write(string)
    file2.close
    cv2.imwrite("result/" + img_path, img_)
    counter += 1
    print(counter)
    # print("fake_cls", bboxes_[5][4])
    # cv2.imshow('test',img_)
    # cv2.imshow('test1',img)
    # cv2.waitKey(0)
print(clss)
    