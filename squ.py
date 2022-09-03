from time import sleep
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
class imageRecognitioner:
    #from matplotlib import pyplot as plt
    # 设置putText函数字体
    font=cv.FONT_HERSHEY_SIMPLEX
        #color=["white","orange","orange","blue","white","green","yellow","red","red"]
    ul=[]
    faceDict={}
    keyList=[]
    cmap=list()
    value1=0
    value2=255
    #以 紅 橙 黃 綠 藍 白 當順序
    hsvMap={
    #儲存顏色的範圍(h-low,h-high,s-low,s-high,v-high,v-low)
            "red":[0,8,43,255,46,255],
            "orange":[9,25,43,255,46,255],
            "yellow":[26,50,43,255,46,255],
            "green":[50,100,43,255,46,255],
            "blue":[100,124,90,255,46,255],
            "white":[0,180,0,90,150,255]
            }
    rgbMap={
    #儲存顏色的範圍(h-low,h-high,s-low,s-high,v-high,v-low)
            "red":[255,0,0],
            "orange":[11,25,43,255,46,255],
            "yellow":[26,50,43,255,46,255],
            "green":[50,100,43,255,46,255],
            "blue":[100,124,90,255,46,255],
            "white":[0,180,0,90,150,255]
            }
             

    def between(self,color,map):
        #功能:檢查顏色是否在範圍裡
        if color[0]<map[0] or color[0]>map[1] or color[1]<map[2] or color[1]>map[3] or color[2]<map[4] or color[2]>map[5]:
            return False
        else:
            return True

    def findColor(self,color,cmap=cmap):
        #功能:找出這個hsv數值屬於哪種顏色
        #print(color)
        if self.between(color,self.hsvMap['red']):
            return 'red'
        elif self.between(color,self.hsvMap['orange']):
            return 'orange'
        elif self.between(color,self.hsvMap['yellow']):
            return 'yellow'
        elif self.between(color,self.hsvMap['green']):
            return 'green'
        elif self.between(color,self.hsvMap['blue']):
            return 'blue'
        elif self.between(color,self.hsvMap['white']):
            return 'white'
        return "unknown"
    def str2color(self,j):
        #功能把字串轉成rgb
        c=(0,0,0)
        if(j=='red'):
            c=(255,0,0)
        elif (j=='blue'):
            c=(0,0,255)
        elif (j=='green'):
            c=(0,255,0)
        elif (j=='white'):
            c=(255,255,255)
        elif (j=='yellow'):
            c=(255,255,0)
        elif (j=='orange'):
            c=(255,69,0)
        else:
            c=(0,0,0)
        return c
    def allColorIsValid(self,color):
        #功能:檢查是不是有unknown的顏色
        for i in color:
            if(i=='unknown'):
                return False
        return True
    
    def angle_cos(self,p0, p1, p2):
        #功能:计算两边夹角额cos值
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

    def find_squares(self,img,hsv):
        #功能:找出方形並辨識顏色
        squares = []
        color=[]
        pos=[]
        # img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

        # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(2,2))
        # img = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
        # # img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

        # img =cv.adaptiveThreshold(img,20,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,3,5) #cv2.imwrite()
        # try:
        #      _, contours, hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
        # except:
        #      contours, hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img=cv.fastNlMeansDenoising(img, 10, 15, 7, 21)
        img = cv.GaussianBlur(img, (5, 5), 0)   
    
        # img = cv.Canny(img, self.value1, self.value2, apertureSize=3)   
        img = cv.Canny(img, 5,10, apertureSize=3)   
        kernel = np.ones((4, 4), np.uint8)
        img = cv.dilate(img, kernel, iterations=4) 
        contours, _hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        #print("轮廓数量：%d" % len(contours))
        index = 0
        # 轮廓遍历
        for cnt in contours:
            cnt_len = cv.arcLength(cnt, True) #计算轮廓周长
            cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True) #多边形逼近
            # 条件判断逼近边的数量是否为4，轮廓面积是否大于1000，检测轮廓是否为凸的
            if len(cnt) >= 4 and cv.contourArea(cnt) > 5000 :
                #print( cv.contourArea(cnt))
                M = cv.moments(cnt) #计算轮廓的矩
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])#轮廓重心
                pos.append([cx,cy])
                # print(img[cy][cx])
                #ul.append(img[cy][cx].tolist())
                #findColor(hsv[cy][cx])
                cnt = cnt.reshape(-1, 2)
                max_cos = np.max([self.angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                # 只检测矩形（cos90° = 0）
                #if max_cos < 0.1:
                # 检测四边形（不限定角度范围）
                if True:
                    index = index + 1
                    cv.putText(img,("#%d"%index+self.findColor(hsv[cy][cx])),(cx,cy),self.font,0.5,(255,0,255),2)
                    #print(str(index)+":"+self.findColor(hsv[cy][cx]))
                    squares.append(cnt)
                    color.append(self.findColor(hsv[cy][cx]))
        
        return squares, img,color,pos

    def sortPos(self,color,pos):
        #功能:依據位置進行排序

        for i in range(8):
            for j in range(8-i):
                if(pos[j][0]>pos[j+1][0]):
                    temp=pos[j]
                    pos[j]=pos[j+1]
                    pos[j+1]=temp
                    temp=color[j]
                    color[j]=color[j+1]
                    color[j+1]=temp
        for k in range(3):
            for m in range(2):
                for n in range(2-m):
                    j=n+k*3
                    if(pos[j][1]>pos[j+1][1]):
                        temp=pos[j]
                        pos[j]=pos[j+1]
                        pos[j+1]=temp
                        temp=color[j]
                        color[j]=color[j+1]
                        color[j+1]=temp
        return color
    

    def findCube(self,frame):
        #功能:把找到的顏色標示出來繪製在左上角
        #sleep(0.1)
        hsvImg=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        squares, img,color,pos =self.find_squares(frame,hsvImg)#找出方形及辨識顏色
    
        img=cv.cvtColor(img,cv.COLOR_GRAY2BGR)
        cv.drawContours( img, squares, -1, (0, 0, 255), 10 )
        for i in range(len(squares)):
            j=color[i]
            c=(0,0,0)
            if(j=='red'):
                c=(255,0,0)
            elif (j=='blue'):
                c=(0,0,255)
            elif (j=='green'):
                c=(0,255,0)
            elif (j=='white'):
                c=(255,255,255)
            elif (j=='yellow'):
                c=(255,255,0)
            elif (j=='orange'):
                c=(255,69,0)
            else:
                c=(0,0,0)
            cv.fillPoly(img, [squares[i]], c)
        if(len(pos)==9 and self.allColorIsValid(color)):
            print("find")
            color=self.sortPos(color,pos)
            if(color[4] not in self.faceDict.keys()):
                self.keyList.append(color[4])
            self.faceDict[color[4]]=color
            
            
        size=100
        borderSize=50
        for faces in range(len(self.faceDict.keys())):
            for i in range(3):
                for j in range(3):
                    img=cv.rectangle(img, (i*size+borderSize+faces*size*3,j*size+borderSize), (i*size+size+faces*size*3,j*size+size), self.str2color(self.faceDict[self.keyList[faces]][i*3+j]), borderSize)

        return img


    def scanImage(self,img="./test5.jpg"):
        #功能:讀取照片並辨識裡面的魔術方塊的顏色
        img = cv.imread(img)
        # print(avg(ul))
        while True:
            cv.imshow('video',self.findCube(img))
            if cv.waitKey(1) == ord('q'):
                break

    def scanVideo(self,videoinput='./img/v4.mp4'):
        #TODO
        #功能:讀取影片並辨識裡面魔術方塊的顏色
        
        cap=cv.VideoCapture(videoinput)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                while True:
                    if cv.waitKey(1) == ord('q'):
                        break
                break
            cv.imshow('video',cv.cvtColor(self.findCube(frame),cv.COLOR_BGR2RGB))
        
            if cv.waitKey(1) == ord('q'):
                break
        
    def useCamera(self):
        #功能:從視訊鏡頭讀入frame
        cap = cv.VideoCapture(2)
        oneFrame=False
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
            #frame = cv.imread("./b.jpg")
            cv.imshow('video',cv.cvtColor(self.findCube(frame),cv.COLOR_BGR2RGB))
            # break
            if cv.waitKey(1) == 27:
                break



    def getColor(self,img):
        #功能:把找到的顏色回傳
        #sleep(0.1)
        frame=cv.imread(img)
        hsvImg=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        squares, img,color,pos =self.find_squares(frame,hsvImg)#找出方形及辨識顏色

        color=self.sortPos(color,pos)
        colorList=[]
        for i in range(3):
            tempList=[]
            for j in range(3):
               tempList.append(color[i*3+j])
            colorList.append(tempList)

        return colorList
    def example(self):
        # main() #使用圖片
        # scanVideo()#使用影片
        # useCamera()#使用視訊鏡頭
    
        #print(__doc__)
        #cmap=correct(cmap)
        #print("main cmap")
        #print(cmap)


        img=[cv.imread("./img/1.jpg"),
                cv.imread("./img/2.jpg"),
                cv.imread("./img/3.jpg"),
                cv.imread("./img/4.jpg"),
                cv.imread("./img/5.jpg"),
                cv.imread("./img/6.jpg")
                ]
        plt.figure(figsize=(8, 6), dpi=80)
        for i in range(6):
            
            plt.subplot(2,6,i+1)
            img[i]=cv.cvtColor(img[i],cv.COLOR_BGR2RGB)
            plt.imshow(img[i])
            plt.subplot(2,6,i+7)
            img[i]=cv.cvtColor(img[i],cv.COLOR_RGB2BGR)
            plt.imshow(self.findCube(img[i]))
        plt.show()
    def nothing(self,x):
        pass
    def debug(self):
        cap = cv.VideoCapture(2)

        
        cv.namedWindow('image',cv.WINDOW_NORMAL)
        cv.createTrackbar('Value1', 'image', 0, 255, self.nothing)
        cv.createTrackbar('Value2', 'image', 0, 255, self.nothing)
        cv.setTrackbarPos('Value2', 'image', 255)
        while(1):
            rat,img=cap.read()
            self.value1=cv.getTrackbarPos('Value1', 'image')
            self.value2=cv.getTrackbarPos('Value2', 'image')
            if(self.value1< self.value2):
                cv.imshow('image', cv.cvtColor(self.findCube(img),cv.COLOR_BGR2RGB))
            if cv.waitKey(10) & 0xFF == ord('q'):
                break
# test=imageRecognitioner()
# test.scanVideo()
# test.scanImage()
