# -*- coding:utf-8 -*-

"""
Asage: A fade-in fade-out album based on SSE4 and multithread.
Author: LiCheng
"""

import sys, random
import operator
from PyQt5.QtWidgets import (QWidget, QApplication, QColorDialog,
                             QVBoxLayout, QSizePolicy, QLabel, QFontDialog,
                             QTextEdit, QFrame, QPushButton, QGridLayout,
                             QMainWindow, QLabel, QAction, QFileDialog,
                             QSlider, QCheckBox, QProgressBar, QCalendarWidget,
                             QHBoxLayout, QLineEdit, QSplitter, QStyleFactory,
                             QComboBox, QScrollArea, QRadioButton)
from PyQt5.QtCore import QCoreApplication, QBasicTimer, QDate, QMimeData
from PyQt5.QtGui import QIcon, QColor, QPixmap, QDrag, QPainter, QFont, \
    QBrush, QPen, QPainterPath, QImage
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os.path as op
import os
import time
from ctypes import *
from multiprocessing import Process, pool, Queue
from threading import Thread, Semaphore




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.mainWidget = MainWidget()

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.count = 0
        self.DIR_PATH = "./"
        self.picList = []
        self.index = 0
        self.main()
        self.q = Queue()
        #self.p = Thread(target=self.sseNpFloat, args=(self.picList[self.index - 1], self.picList[self.index]))
        self.semaphore = Semaphore(1)
        self.processFlag = True
        self.direction = 0 #为0是下一张，为1是上一张


    def initUI(self):

        self.loadPicBtn = QPushButton('加载目录', self)
        #self.deletePicBtn = QPushButton('移除图片', self)
        self.nextPicBtn = QPushButton('下一张', self)
        self.prePicBtn = QPushButton('上一张', self)

        #scroll = QScrollArea()

        self.hboxBtn = QHBoxLayout()
        self.hboxBtn.setSpacing(10)
        self.hboxBtn.addWidget(self.loadPicBtn)
        #self.hboxBtn.addWidget(self.deletePicBtn)
        self.hboxBtn.addWidget(self.nextPicBtn)
        self.hboxBtn.addWidget(self.prePicBtn)


        hboxPic = QHBoxLayout()
        hboxPic.addStretch(1)

        #pic1, pic2 = self.chosePics()
        #self.picFade(pic1, pic2)
        self.piclbl = QLabel()
        self.piclbl.setGeometry(0, 0, 100, 200)
        self.piclbl.setFixedSize(1200, 600)
        self.piclbl.setScaledContents(True)
        self.piclbl.setPixmap(QPixmap(""))

        self.fadeLabel = QLabel()
        #self.fadeLabel.setText("Fading······ fade = %lf"%self.fadeRate)
        fadeBox = QVBoxLayout()
        fadeBox.addWidget(self.fadeLabel)

        self.rbNO = QRadioButton("不使用渐变", self)
        self.rbImage = QRadioButton("使用Image渐变", self)
        self.rbDefult = QRadioButton("使用Python渐变", self)
        self.rbSSE4 = QRadioButton("使用SSE4渐变", self)

        self.checkLabel = QLabel("选择渐变模式：  ",self)
        checkBox = QHBoxLayout()
        checkBox.addWidget(self.checkLabel)
        checkBox.addWidget(self.rbNO)
        checkBox.addWidget(self.rbDefult)
        checkBox.addWidget(self.rbImage)
        checkBox.addWidget(self.rbSSE4)
        checkBox.addStretch()

        hboxPic.addWidget(self.piclbl)

        #scroll.setWidget(self.piclbl)

        vbox = QVBoxLayout()

        vbox.addLayout(self.hboxBtn)
        vbox.addLayout(checkBox)
        vbox.addLayout(fadeBox)
        vbox.addLayout(hboxPic)

        self.setLayout(vbox)

        self.setGeometry(0, 0, 380, 250)
        self.setWindowTitle('Fading Album')
        self.show()

    def loadDir(self):
        self.picList=[]
        self.DIR_PATH = QFileDialog.getExistingDirectory(self, "Chose Directory", "./")
        if len(self.DIR_PATH):
            for list in os.listdir(self.DIR_PATH):
                if (list[-3:] == 'jpg') or (list[-4:] == 'jpeg') or (list[-3:] == 'png'):
                    if list[:4] == 'temp':
                        continue
                    self.picList.append(list)
            #print(self.DIR_PATH + "/" + self.picList[self.index])
            #print(self.picList)
            self.loadPic(self.DIR_PATH + "/" + self.picList[self.index])
        #self.piclbl.setPixmap(QPixmap(self.picList[self.index]))
        #self.sse = CDLL("./libsse.so")
        #self.sse.main()


    def nextPic(self):
        self.direction = 0
        if self.processFlag == True:
            self.processFlag = False
            if self.picList:
                self.index = self.index + 1
                if self.index == len(self.picList):
                    self.index = 0
                #print(self.picList[0])
                #print(self.picList[self.index], self.picList[self.index+1])
                #self.picFade(self.picList[self.index-1], self.picList[self.index])
                #self.picDefaultFade(self.picList[self.index-1], self.picList[self.index])
                #self.q.put(self.piclbl)
                #p = Thread(target=self.sseNpFloat, args = (self.picList[self.index-1], self.picList[self.index]))
                #print("Parent process is running")

                #self.semaphore.acquire()
                """
            
                if self.index == 0:
                    p = Thread(target=self.sseNpFloat,
                               args=(self.DIR_PATH + "/" + self.picList[-1],
                                self.DIR_PATH + "/" + self.picList[0]))
                    p.start()
                else:
                    p = Thread(target=self.sseNpFloat,
                           args = (self.DIR_PATH + "/" + self.picList[self.index - 1],
                                   self.DIR_PATH + "/" + self.picList[self.index]))
                    p.start()
                """

                if self.rbSSE4.isChecked():
                    self.processFunc(self.sseNpFloat)

                elif self.rbNO.isChecked():
                    self.processFunc(self.NOFade)

                elif self.rbImage.isChecked():
                    self.processFunc(self.picDefaultFade)

                elif self.rbDefult.isChecked():
                    self.processFunc(self.picFade)

                else:
                    self.processFunc(self.NOFade)

                #print("thrad is running")

                #print("Parent process is running")
                #self.sseNpFloat(self.DIR_PATH + "/" + self.picList[self.index], self.DIR_PATH + "/" + self.picList[self.index+1])

                #self.piclbl.setPixmap(QPixmap(self.picList[self.index]))
                #pixmap = QPixmap('')
                #pixmap.
                #self.picFade(Image.open(self.picList[self.index]), Image.open(self.picList[self.index+1]))

    def processFunc(self, target):#切换后的图片放在第一个参数
        if self.direction == 0:
            if self.index == 0:
                p = Thread(target = target,
                           args=(self.DIR_PATH + "/" + self.picList[0],
                                 self.DIR_PATH + "/" + self.picList[-1]))
                p.start()
            else:
                p = Thread(target = target,
                           args=(self.DIR_PATH + "/" + self.picList[self.index],
                                 self.DIR_PATH + "/" + self.picList[self.index - 1]))
                p.start()
        else:
            if self.index == len(self.picList) -1:
                p = Thread(target=target,
                           args=(self.DIR_PATH + "/" + self.picList[-1],
                                 self.DIR_PATH + "/" + self.picList[0]))
                p.start()
            else:
                p = Thread(target=target,
                           args=(self.DIR_PATH + "/" + self.picList[self.index],
                                 self.DIR_PATH + "/" + self.picList[self.index + 1]))
                p.start()

    def NOFade(self, name1, name2):
        self.loadPic(name1)
        self.processFlag = True


    def prePic(self):
        """
        if self.processFlag == True:
            if self.picList:
                self.index = self.index - 1
                if self.index == -1:
                    self.index = len(self.picList) - 1
                self.piclbl.setPixmap(QPixmap(self.DIR_PATH + "/" + self.picList[self.index]))
                self.count = self.count + 1
                print("prePIc -- self.count == " + str(self.count))
        """
        self.direction = 1
        if self.processFlag == True:
            self.processFlag = False
            if self.picList:
                self.index = self.index - 1

                if self.index == -1:
                    self.index = len(self.picList) - 1

                if self.rbSSE4.isChecked():
                    self.processFunc(self.sseNpFloat)

                elif self.rbNO.isChecked():
                    self.processFunc(self.NOFade)

                elif self.rbImage.isChecked():
                    self.processFunc(self.picDefaultFade)

                elif self.rbDefult.isChecked():
                    self.processFunc(self.picFade)

                else:
                    self.processFunc(self.NOFade)

    def picDefaultFade(self, name1, name2):
        """使用PIL库Image的默认融合函数blend()进行两张图片的融合"""
        #startTime = time.process_time()
        print("使用默认PIL提供的Image.blend()函数耗时：")
        totleTime = 0
        for fadeRate in range(1, 11):
            self.fadeLabel.setText("Fading······ fade rate = %.1f"%(fadeRate/10))
            startTime = time.process_time()
            img = Image.blend(Image.open(name2), Image.open(name1), fadeRate/10)
            endTime = time.process_time()
            totleTime = endTime - startTime + totleTime
            img.save(".temp.jpg")
            self.loadPic(".temp.jpg")
            #img.save("newtemp" + str(fadeRate / 10) + ".jpg")
            #plt.imshow(img)
            #plt.show()
        #endTime = time.process_time()
        self.processFlag = True
        print("共耗时%f秒"%(totleTime))

    def picFade(self, name1, name2):
        """使用python语法直接计算像素点的融合值"""
        print("未使用SSE4指令集计算像素：")
        ret = np.array(Image.open(".temp.jpg"))
        #print(type(ret))
        #print(name1)
        #print("name1:"+name2)
        img1 = np.array(Image.open(name1),dtype=np.int32)
        img2 = np.array(Image.open(name2),dtype=np.int32)
        rows, cols, channels = img1.shape
        #startTime = time.process_time()
        totleTime = 0
        for fadeRate in range (1, 11):
            self.fadeLabel.setText("Fading······ fade rate = %.1f"%(fadeRate/10))
            for i in range (0, rows):
                for j in range(0, cols):
                    #ret[i, j, :] = img1[i, j, :]*(fadeRate/10) + img2[i,j,:]*(1-(fadeRate/10))
                    #ret[i, j, :] = (img1[i, j, :] - img2[i, j, :]) * (fadeRate/10) + img2[i,j,:]
                    #ret[i, j, :] = img1[i, j, :] * (fadeRate/10) + img2[i,j,:] *  (1-fadeRate/10)
                    #retpix = img1[i, j, :] * (fadeRate/10) + img2[i,j,:] *  (1-fadeRate/10)
                    x1 = img1[i, j, :]
                    x2 = img2[i, j, :]
                    startTime = time.process_time()
                    #retpix1 = x1 * (fadeRate/10) + x2 * (1-fadeRate/10)
                    retpix = (x1 - x2) * (fadeRate/10) + x2  #这个式子与上面的式子计算出的数值不一样
                    #print((x1 * 0.1 + x2 *0.9))
                    #print(retpix1)
                    #print("----")
                    #print(retpix2)
                    #print("*****")
                    #print(operator.eq(retpix1, retpix2))
                    endTime = time.process_time()
                    ret[i, j, :] = retpix
                    totleTime = totleTime + endTime - startTime
            Image.fromarray(ret).save(".temp.jpg")
            self.loadPic(".temp.jpg")
            #self.piclbl.setPixmap(QPixmap(''))
            #self.piclbl.setPixmap(QPixmap("temp.jpg"))
            #print("showed on app:fadeRate =" + str(fadeRate))
        #endTime = time.process_time()
        self.processFlag = True
        print("共耗时%f秒"%(totleTime))

    def sse(self, name1, name2):
        """SSE测试方法，使用Image对图像处理"""
        img1 = Image.open(name1)
        img2 = Image.open(name2)
        img1_arr = img1.load()
        img2_arr = img2.load()
        img = Image.open("temp.jpg")
        img_arr = img.load()

        PIC1 = c_float * 4
        PIC2 = c_float* 4
        src1 = PIC1()
        src2 = PIC2()

        rows, cols = img1.size
        dll = CDLL("./libsse.so")
        dll.meargeFunc.restype = POINTER(c_float)
        for rgb in range(3):
            for row in range(rows):
                for col in range(cols):
                    if col%4 == 0 and col >0:
                        ret = dll.meargeFunc(src1, src2)
                        print("col=%d"%col)
                    src1[col % 4] = img1_arr[row, col][rgb]
                    src2[col % 4] = img2_arr[row, col][rgb]

                    #img_arr[row, col-3][rgb] = ret[0]
                    #img_arr[row, col-2][rgb] = ret[1]
                    #img_arr[row, col-1][rgb] = ret[2]
                    #img_arr[row, col][rgb] = ret[3]

        #img.save("newTemp.jpg")

        """
        dll = CDLL("./libsse.so")

        print("*"*10)
        PIC1 = c_float * 4
        PIC2 = c_float * 4
        pic1 = PIC1()
        pic2 = PIC2()
        
        img1 = Image.open(name1)
        img2 = Image.open(name2)
        img1_arr = img1.load()
        img2_arr = img2.load()
        pic1[0] = img1_arr[0, 0][0] * 0.2
        pic1[1] = img1_arr[0, 1][0] * 0.2
        pic1[2] = img1_arr[0, 2][0] * 0.2
        pic1[3] = img1_arr[0, 3][0] * 0.2
        pic2[0] = img2_arr[0, 0][0] * 0.8
        pic2[1] = img2_arr[0, 1][0] * 0.8
        pic2[2] = img2_arr[0, 2][0] * 0.8
        pic2[3] = img2_arr[0, 3][0] * 0.8

        #dll.meargeFunc(pic1, pic2)
        dll.meargeFunc.restype = POINTER(c_float)
        #ret = pointer(dll.meargeFun(pic1, pic2))
        ret = dll.meargeFunc(pic1, pic2)
        print(int(ret[2]))
        """

    def sseNp(self, name1, name2):
        """SSE测试方法，使用numpy.array()对图像处理"""
        img1 = np.array(Image.open(name1))
        img2 = np.array(Image.open(name2))
        img = np.array(Image.open("temp.jpg"))

        PIC1 = c_float * 4
        PIC2 = c_float * 4
        src1 = PIC1()
        src2 = PIC2()
        rows, cols, chans = img1.shape
        dll = CDLL("./libsse.so")
        dll.meargeFunc.restype = POINTER(c_float)
        startTime = time.process_time()
        for fadeRate in range(1,11):
            for rgb in range(3):
                for row in range(rows):
                    for col in range(cols):
                        if col%4 == 0 and col > 0:
                            ret = dll.meargeFunc(src1, src2)
                            img[row, col - 3][rgb] = int(ret[0])
                            img[row, col - 2][rgb] = int(ret[1])
                            img[row, col - 1][rgb] = int(ret[2])
                            img[row, col][rgb] = ret[3]
                        src1[col % 4] = img1[row, col, rgb]
                        src2[col % 4] = img2[row, col, rgb ]

            Image.fromarray(img).save("newtemp"+str(fadeRate/10)+".jpg")
        endTime = time.process_time()
        print("共耗时%f秒"%(endTime - startTime))

    def sseNpInt(self, name1, name2):
        """调用SSE函数处理像素，返回值为float*型，此方法未完全通过测试"""
        img1 = np.array(Image.open(name1))
        img2 = np.array(Image.open(name2))
        img = np.array(Image.open("temp.jpg"))

        PIC1 = c_int * 4
        PIC2 = c_int * 4
        src1 = PIC1()
        src2 = PIC2()
        rows, cols, chans = img1.shape
        dll = CDLL("./libsse.so")
        dll.meargeFunc.restype = POINTER(c_float)
        startTime = time.process_time()
        for fadeRate in range(1,11):
            fade = c_float(fadeRate/10)
            for rgb in range(3):
                for row in range(rows):
                    for col in range(cols):
                        if col%4 == 0 and col > 0:
                            ret = dll.meargeFunc(src1, src2, fade)
                            img[row, col - 3][rgb] = int(ret[0])
                            img[row, col - 2][rgb] = int(ret[1])
                            img[row, col - 1][rgb] = int(ret[2])
                            img[row, col][rgb] = ret[3]
                        src1[col % 4] = img1[row, col, rgb]
                        src2[col % 4] = img2[row, col, rgb ]

            Image.fromarray(img).save("newtemp"+str(fadeRate)+".jpg")
        endTime = time.process_time()
        print("共耗时%f秒"%(endTime - startTime))

    def sseNpFloat(self, name1, name2):
        """调用SSE函数处理像素，返回值为int*型，实际按钮调用的方法"""
        print("使用SSE4指令集计算像素：")
        img1 = np.array(Image.open(name1))
        img2 = np.array(Image.open(name2))
        img = np.array(Image.open(".temp.jpg"))
        totleTime = 0
        PIC1 = c_int * 4
        PIC2 = c_int * 4
        src1 = PIC1()
        src2 = PIC2()
        rows, cols, chans = img1.shape
        dll = CDLL("./libsse.so")
        dll.meargeFunc.restype = POINTER(c_int)
        startTime = time.process_time()
        for fadeRate in range(1,11):
            for rgb in range(3):
                for row in range(rows):
                    for col in range(cols):
                        if col%4 == 0 and col > 0:
                            #startTime = time.process_time()
                            ret = dll.meargeFunc(src1, src2, c_float(fadeRate/10))#一条计算指令耗时20s左右
                            #endTime = time.process_time()
                            #totleTime = endTime - startTime + totleTime

                            img[row, col - 3][rgb] = ret[0]#以下四条取值赋值指令耗时30s左右
                            img[row, col - 2][rgb] = ret[1]
                            img[row, col - 1][rgb] = ret[2]
                            img[row, col][rgb] = ret[3]

                        src1[col % 4] = img1[row, col, rgb]#以下两条取值赋值指令耗时70s
                        src2[col % 4] = img2[row, col, rgb ]
            #name = "newTemp"+str(fadeRate)+".jpg"
            Image.fromarray(img).save(".temp.jpg")
            #self.piclbl.setPixmap(QPixmap(name))
            self.fadeLabel.setText("Fading······ fade rate = %.1f"%(fadeRate/10))

            self.loadPic(".temp.jpg")

            #self.piclbl.setPixmap(QPixmap("temp.jpg"))
            #print(name)

        endTime = time.process_time()
        self.loadPic(name1)
        print("共耗时%f秒"%(endTime - startTime))
        #self.semaphore.release()
        self.processFlag = True

    def loadPic(self, name):
        """向相册中加载图片"""
        self.piclbl.setPixmap(QPixmap(name))
        #self.count = self.count + 1
        #print("self.count = " + str(self.count))


    def main(self):

        #p = Process(target=self.initUI())
        #p.start()
        self.initUI()
        self.loadPicBtn.clicked.connect(self.loadDir)
        self.nextPicBtn.clicked.connect(self.nextPic)
        self.prePicBtn.clicked.connect(self.prePic)
        #self.sseNpFloat("Avengers2.jpg", "BatMan.jpg")


if __name__ == '__main__':
    #batMam = Image.open('BatMan.jpg')
    #captain = Image.open('Captain.jpg')
    #image = Image.blend(batMam, captain, 0.3)

    #img = np.array(Image.open('deadpool.jpg'))
    #rows, cols, dims = img.shape
    #fade = 0.3
    #plt.figure('boy')
    #plt.imshow(img)
    #print(img.shape)
    #print(img.dtype)
    #print(img.size)
    #print(type(img))
    #for i in range(0,100):
    #   image = Image.blend(batMam, captain, i*0.01)
    #    merge = np.array(image)
    #    plt.imshow(image)
    #   plt.show()
    #img[i,j,:] = img[i,j,:] * fade + img2[i,j,:] * (1-fade)
    #plt.axis('off')
    #plt.imshow(img)
    #plt.show()

    QApplication.processEvents()
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    app.exec_()