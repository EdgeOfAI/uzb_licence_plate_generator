# -*-coding: UTF-8 -*-
import numpy as np
from genplate_advanced import *
import os
import pandas as pd
import pickle
import cv2
import os
import random 
lets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
val_l = [ 2959, 469, 172, 187, 149, 194, 201, 300, 0, 98, 110, 127, 276, 135, 114, 131, 90, 132, 133, 211, 80, 96, 60, 66, 80, 86]
val_n = [2271, 995, 920, 1008, 1197, 865, 942, 883, 856]
sum_l = 0
sum_n = 0

for i in range(len(lets)):
    val_l[i] = 4000 - val_l[i]

for i in range(9):
    val_n[i] = 4000 - val_n[i]

print(sum(val_l))
def rand_range(lo, hi):
    return lo + r(hi - lo)


def r(val):
    return int(np.random.random() * val)

counter = 5000
def gen_rand():
    name = ""
    #generating name
    global counter 
    if counter : 
        counter -= 1
    if counter :
        #first
        num = random.choice(nums)
        name += num
        for i in range(len(nums)):
            if(nums[i] == num):
                val_n[i] -= 1
                if val_n[i] == 0:
                    val_n.remove(val_n[i])
                    nums.remove(nums[i])
                break
        #second
        num = random.choice(nums)
        name += num
        for i in range(len(nums)):
            if(nums[i] == num):
                val_n[i] -= 1
                if val_n[i] == 0:
                    val_n.remove(val_n[i])
                    nums.remove(nums[i])
                break
        
        #third
        let = random.choice(lets)
        name += let
        for i in range(len(lets)):
            if(lets[i] == let):
                val_l[i] -= 1
                if val_l[i] == 0:
                    val_l.remove(val_l[i])
                    lets.remove(lets[i])
                break

        #fourth
        num = random.choice(nums)
        name += num
        for i in range(len(nums)):
            if(nums[i] == num):
                val_n[i] -= 1
                if val_n[i] == 0:
                    val_n.remove(val_n[i])
                    nums.remove(nums[i])
                break
        
        #fifth
        num = random.choice(nums)
        name += num
        for i in range(len(nums)):
            if(nums[i] == num):
                val_n[i] -= 1
                if val_n[i] == 0:
                    val_n.remove(val_n[i])
                    nums.remove(nums[i])
                break
        
        #sixth
        num = random.choice(nums)
        name += num
        for i in range(len(nums)):
            if(nums[i] == num):
                val_n[i] -= 1
                if val_n[i] == 0:
                    val_n.remove(val_n[i])
                    nums.remove(nums[i])
                break
        
        #sevens
        let = random.choice(lets)
        name += let
        for i in range(len(lets)):
            if(lets[i] == let):
                val_l[i] -= 1
                if val_l[i] == 0:
                    val_l.remove(val_l[i])
                    lets.remove(lets[i])
                break
        
        #eighth
        let = random.choice(lets)
        name += let
        for i in range(len(lets)):
            if(lets[i] == let):
                val_l[i] -= 1
                if val_l[i] == 0:
                    val_l.remove(val_l[i])
                    lets.remove(lets[i])
                break
    else:
        for i in range(8):
            let = random.choice(lets)
            name += let
            for i in range(len(lets)):
                if(lets[i] == let):
                    val_l[i] -= 1
                    if val_l[i] == 0:
                        val_l.remove(val_l[i])
                        lets.remove(lets[i])
                    break
    return name


def gen_sample(genplate_advanced, width, height):
    name = gen_rand()
    img = genplate_advanced.generate(name)
    img = cv2.resize(img, (width, height))
    # img = np.multiply(img, 1 / 255.0)
    # img = img.transpose(2, 0, 1)
    if len(name) != 8:
        print(name, counter)
    return name, img


def genBatch(batchSize, outputPath):
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    # label_store = []
    for i in range(batchSize):
        print('create num:' + str(i))
        name, img = gen_sample(genplate_advanced, 320, 64)
        # label_store.append(label)
        filename = os.path.join(outputPath, str(i).zfill(4) )
        # filename = os.path.join(outputPath, label + ".jpg")
        # filename = outputPath + '/' + str(label) + ".jpg"
        # print(filename)
        cv2.imwrite(filename + ".jpg", img)
        st = open('example.txt', 'r')
        st = st.readlines()
        string = ''
        clss = get_str()
        i = 0
        for line in st:
            string += str(clss[i]) + line
            i += 1
        wrt = open(filename + ".txt", 'w+')
        wrt.write(string)
        # print(string)
        # exit()
    # label_store = pd.DataFrame(label_store)
    # np.savetxt('label.txt', label_store)
    # label_store.to_csv('label.txt')


batchSize = 20
# batchSize = 5
path = './data/train_data'
font_ch = './font/platech.ttf'
font_en = './font/platechar.ttf'
font_uz = './font/uzb.ttf'
bg_dir = './NoPlates'
genplate_advanced = GenPlate(font_uz, font_en, bg_dir)
genBatch(batchSize=batchSize, outputPath=path)

# create train label
a = np.loadtxt('label.txt')
b = np.zeros([batchSize, 65])
for i in range(batchSize):
    for j in range(7):
        b[i, int(a[i, j])] = int(a[i, j])

# create image train data
img_data = np.zeros([batchSize, 64, 320, 3])
for i in range(batchSize):
    img_path = path + '/' + str(i).zfill(4) + ".jpg"
    img_temp = cv2.imread(img_path)
    img_temp = np.reshape(img_temp, (64, 320, 3))
    img_data[i, :, :, :] = img_temp


print(b)
print('numbers:',len(nums), print(len(lets)))
for i in range(len(nums)):
    print(nums[i], val_n[i])
for i in range(len(lets)):
    print(lets[i], val_l[i])
output = open('train_data.pkl', 'wb')
pickle.dump(img_data, output)
# output = open('train_label.pkl', 'wb')
# pickle.dump(b, output)