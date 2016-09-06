#coding:utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt
from cv2 import erode
class cutImage(object):
    def __init__(self,img,bin_threshold,kernel,iterations,areaRange,border=10,show=True,write=True):
        self.img = img
        self.bin_threshold = bin_threshold
        self.kernel = kernel
        self.iterations = iterations
        self.areaRange = areaRange
        self.border = border
        self.show = show
    def getRes(self):
        if len(self.img.shape) == 2:  # 灰度图
            img_gray = self.img
        elif len(self.img.shape)==3:
            img_gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(img_gray,self.bin_threshold,255,0)

        img_erode = cv2.erode(thresh,self.kernel,iterations=self.iterations)
        if self.show:
            cv2.imshow('thresh',thresh)
            cv2.imshow('erode',img_erode)
        image,contours,hierarchy = cv2.findContours(img_erode,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        roiList = []
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if area >self.areaRange[0] and area <self.areaRange[1]:
                x,y,w,h = cv2.boundingRect(cnt)
                roi = self.img[y+self.border:(y+h)-self.border,x+self.border:(x+w)-self.border]
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                roiList.append(roi)
#                 cv2.imshow("D:\\nlp\\image\\output\\img_draw_1.jpg", img_erode)
#                 cv2.waitKey()
        cv2.imwrite('D:\\nlp\\image\\output\\img_draw.jpg',img)
        return roiList
        # return img
if __name__=='__main__':
    img = cv2.imread('./images/a1.jpg')
    bin_threshold = 200 # 二值化的阈值
    ker = np.ones((3,3),np.uint8) # 膨胀时的kernel
    iterations = 9  #膨胀时的次数
    areaRange = [1000,100000]  # 筛选区域的面积
    roi_res = cutImage(img,bin_threshold,ker,iterations,areaRange,0).getRes()
    n=0
    for each in roi_res:
        n=n+1
        cv2.imwrite("D:\\nlp\\image\\output\\"+'__%d'%n+'.jpg',each)
        # cv2.imshow('img',each)
    # cv2.waitKey()
