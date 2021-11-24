#coding=utf-8
import os
import argparse
from math import *
import numpy as np
import cv2
# import PIL
from PIL import Image, ImageFont, ImageDraw
from PlateCommon import *
st = []
class GenPlate:
    def __init__(self, fontuz, fontEng, NoPlates):
        self.fontC = ImageFont.truetype(fontuz, 32, 0)
        self.fontE = ImageFont.truetype(fontuz, 52, 0)
        self.img = np.array(Image.new("RGB", (226, 70), (255, 255, 255)))
        cv2.imwrite('smth.jpg',self.img)
        self.bg = cv2.resize(cv2.imread("./images/template.bmp"), (226, 70))
        self.smu = cv2.imread("./images/smu2.jpg")
        self.noplates_path = []
        for parent, parent_folder, filenames in os.walk(NoPlates):
            for filename in filenames:
                path = parent + "/" + filename
                self.noplates_path.append(path)
    def draw(self, val):
        cls, xc, yc, wb, hb = [], [], [], [], []
        cls = val
        global st 
        self.img[0: 70, 8 : 28 ] = GenCh(self.fontC, val[0])
        xc.append(21)
        yc.append(28)

        self.img[0: 70, 28:48] = GenCh(self.fontC, val[1])
        xc.append(49)
        yc.append(28)

        base = 48 + 3
        self.img[0: 70, base: base + 24] = GenCh1(self.fontE, val[2])
        xc.append(89)
        yc.append(32)
        base += 24

        base = base + 3
        self.img[0: 70, base: base + 24] = GenCh1(self.fontE, val[3])
        xc.append(126)
        yc.append(32)
        base += 24

        base = base 
        self.img[0: 70, base: base + 24] = GenCh1(self.fontE, val[4])
        xc.append(161)
        yc.append(32)
        base += 24
        
        base = base 
        self.img[0: 70, base: base + 24] = GenCh1(self.fontE, val[5])
        xc.append(192)
        yc.append(32)
        base += 24
        
        base = base + 2
        self.img[0: 70, base: base + 24] = GenCh1(self.fontE, val[6])
        xc.append(231)
        yc.append(32)
        base += 24
        
        base = base 
        self.img[0: 70, base: base + 24] = GenCh1(self.fontE, val[7])
        xc.append(266)
        yc.append(32)
        st = []
        for i in range(8):
            aaa = ord(cls[i]) - 48
            if(aaa > 9) :
                aaa -= 7
            st.append(aaa)
        return self.img
    

    def generate(self, text):
        if len(text) == 8:
            # fg = self.draw(text.decode(encoding="utf-8"))
            fg = self.draw(text)
            fg = cv2.bitwise_not(fg)
            #fixing drawn image to bg
            com = cv2.bitwise_xor(fg, self.bg)
            #rotating dioganal angles 
            # com = rot(com,r(60)-30,com.shape,30)
            # cv2.imshow('img',com)
            # cv2.waitKey(0)
            # print(com.shape[1],com.shape[0])
            # #unknown
            # com = rot(com, r(40) - 20, com.shape, 20)
            # # cv2.imshow('com_rot2',com)
            # # cv2.waitKey(0)
            
            # #adding space and rotating
            # com = rotRandrom(com, 10, (com.shape[1], com.shape[0]))
            # # cv2.imshow('com_random',com)
            # # cv2.waitKey(0)
            
            # #nothing with rotation
            com = AddSmudginess(com, self.smu)
            # # cv2.imshow('com_addsmudg',com)
            # # cv2.waitKey(0)
            
            # com = tfactor(com)
            # # cv2.imshow('com_tfactor',com)
            # # cv2.waitKey(0)
            
            # com = random_envirment(com, self.noplates_path)
            # # cv2.imshow('com_rand_env',com)
            # # cv2.waitKey(0)
            
            com = AddGauss(com, 1 + r(2))
            # # cv2.imshow('com_addgauss',com)
            # # cv2.waitKey(0)
            
            com = addNoise(com)
            # # cv2.imshow('com_addnoise',com)
            # # cv2.waitKey(0)
            # # print(st)
            return com

    def genPlateString(self, pos, val):
        plateStr = ""
        box = [0, 0, 0, 0, 0, 0, 0]
        if(pos != -1):
            box[pos] = 1
        for unit, cpos in zip(box, range(len(box))):
            if unit == 1:
                plateStr += val
            else:
                if cpos == 0:
                    plateStr += chars[r(31)]
                elif cpos == 1:
                    plateStr += chars[41 + r(24)]
                else:
                    plateStr += chars[31 + r(34)]
        return plateStr

    def genBatch(self, batchSize, pos, charRange, outputPath, size):
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        for i in range(batchSize):
            plateStr = self.genPlateString(-1, -1)
            print(plateStr)
            img = self.generate(plateStr)
            print(st)
            print(img)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, size)
            # filename = os.path.join(outputPath, str(i).zfill(4) + '.' + plateStr + ".jpg")
            filename = os.path.join(outputPath, str(i).zfill(5) + '_' + plateStr)
            cv2.imwrite(filename + + ".jpg", img)
            # wrt = open(filename + ".txt", 'w+')
            # wrt.write(st)
            # print(st)
            # print(filename, plateStr)

def get_str():
    return st

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--font_ch', default='./font/platech.ttf')
    parser.add_argument('--font_en', default='./font/platechar.ttf')
    parser.add_argument('--bg_dir', default='./NoPlates')
    parser.add_argument('--out_dir', default='./data/plate_train', help='output dir')
    parser.add_argument('--make_num', default=10, type=int, help='num')
    parser.add_argument('--img_w', default=120, type=int, help='num')
    parser.add_argument('--img_h', default=32, type=int, help='num')
    return parser.parse_args()


def main(args):
    G = GenPlate(args.font_ch, args.font_en, args.bg_dir)
    G.genBatch(args.make_num, 2, range(31, 65), args.out_dir, (args.img_w, args.img_h))


if __name__ == '__main__':
    main(parse_args())
