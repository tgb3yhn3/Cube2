import tkinter as tk
import tkinter.font as tkFont
from enum import Enum

##########################################################
#                        全域變數          
##########################################################
class Color(Enum):
    WHITE  = 0
    RED    = 1
    ORANGE = 2
    YELLOW = 3
    GREEN  = 4
    BLUE   = 5

cubeColorData = [[[Color.WHITE for col in range(3)] for row in range(3)] for face in range(6)]    #儲存每個魔術方塊格子的顏色資料
manuallySelectedColors = Color.WHITE    #手動填色功能中，目前選中的顏色 
standardPixelSize = 35    #會影響畫面上所有元件的大小(其值相當於魔術方塊中一格的邊長)

##########################################################
#                          函式         
##########################################################
def clickFaceButton(FaceButtons,face,row,col):
    #功能:被按的魔術方塊格子按鈕會根據manuallySelectedColors的值改變顏色，同時也會更改此格的顏色資料(cubeColorData[face][row][col])
    #參數:FaceButtons：所有魔術方塊格子按鈕  face:在魔術方塊的哪一面  num:是同一面中的第幾格
    global cubeColorData
    if manuallySelectedColors == Color.WHITE:
        FaceButtons[face][row][col].configure(bg = "white")
        cubeColorData[face][row][col] = Color.WHITE
    elif manuallySelectedColors == Color.RED:
        FaceButtons[face][row][col].configure(bg = "red")
        cubeColorData[face][row][col] = Color.RED
    elif manuallySelectedColors == Color.ORANGE:
        FaceButtons[face][row][col].configure(bg = "orange")
        cubeColorData[face][row][col] = Color.ORANGE
    elif manuallySelectedColors == Color.YELLOW:
        FaceButtons[face][row][col].configure(bg = "yellow")
        cubeColorData[face][row][col] = Color.YELLOW
    elif manuallySelectedColors == Color.GREEN:
        FaceButtons[face][row][col].configure(bg = "green")
        cubeColorData[face][row][col] = Color.GREEN
    elif manuallySelectedColors == Color.BLUE:
        FaceButtons[face][row][col].configure(bg = "blue")
        cubeColorData[face][row][col] = Color.BLUE

def clickManuallySetColorButton(manuallyChooseColorBlock,i):
    #功能:按下手動調色盤的顏色格子按鈕後，會改變manuallySelectedColors的值
    #參數:manuallyChooseColorBlock:被選中的顏色會顯示在這裡  i:第幾個顏色
    global manuallySelectedColors
    if i == 0:
        manuallySelectedColors = Color.WHITE 
        manuallyChooseColorBlock.configure(bg = "white")
    elif i == 1:
        manuallySelectedColors = Color.RED 
        manuallyChooseColorBlock.configure(bg = "red")
    elif i == 2:
        manuallySelectedColors = Color.ORANGE
        manuallyChooseColorBlock.configure(bg = "orange")
    elif i == 3:
        manuallySelectedColors = Color.YELLOW 
        manuallyChooseColorBlock.configure(bg = "yellow")
    elif i == 4:
        manuallySelectedColors = Color.GREEN 
        manuallyChooseColorBlock.configure(bg = "green")
    elif i == 5:
        manuallySelectedColors = Color.BLUE 
        manuallyChooseColorBlock.configure(bg = "blue")

def clickStartButton():
    #功能：按下開始執行按鈕的事件，轉回魔術方塊之前，簡單檢查一下魔術方塊能不能成功轉回來
    
    #1.判斷每面的中間格子顏色是否重複出現
    centerBlock = []
    for i in range(6):
        centerBlock.append(cubeColorData[i][1][1])
    if len(set(centerBlock))!=len(centerBlock):
        startErrorMessage.set("每一面中間格子的顏色不能重複!")
        return
    
    #2.判斷每面的中間格子的對面格子顏色是否符合
    if(True):
        if(centerBlock[0] == Color.WHITE and centerBlock[5] != Color.YELLOW):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[0] == Color.RED and centerBlock[5] != Color.ORANGE):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[0] == Color.ORANGE and centerBlock[5] != Color.RED):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[0] == Color.YELLOW and centerBlock[5] != Color.WHITE):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[0] == Color.GREEN and centerBlock[5] != Color.BLUE):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[0] == Color.BLUE and centerBlock[5] != Color.GREEN):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[1] == Color.WHITE and centerBlock[3] != Color.YELLOW):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[1] == Color.RED and centerBlock[3] != Color.ORANGE):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[1] == Color.ORANGE and centerBlock[3] != Color.RED):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[1] == Color.YELLOW and centerBlock[3] != Color.WHITE):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[1] == Color.GREEN and centerBlock[3] != Color.BLUE):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[1] == Color.BLUE and centerBlock[3] != Color.GREEN):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[2] == Color.WHITE and centerBlock[4] != Color.YELLOW):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[2] == Color.RED and centerBlock[4] != Color.ORANGE):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[2] == Color.ORANGE and centerBlock[4] != Color.RED):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[2] == Color.YELLOW and centerBlock[4] != Color.WHITE):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[2] == Color.GREEN and centerBlock[4] != Color.BLUE):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return
        if(centerBlock[2] == Color.BLUE and centerBlock[4] != Color.GREEN):
            startErrorMessage.set("每一面中間格子與它對面的格子顏色不符合!\n(例如中間格子是黃色的話，對面的中間格子必須是白色)")
            return

    #3.每個顏色必須恰好出現9次
    if(True):
        whiteNum = 0
        redNum = 0
        orangeNum = 0
        yellowNum = 0
        greenNum = 0
        blueNum = 0
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if(cubeColorData[i][j][k]== Color.WHITE):
                        whiteNum += 1
                    if(cubeColorData[i][j][k]== Color.RED):
                        redNum += 1
                    if(cubeColorData[i][j][k]== Color.ORANGE):
                        orangeNum += 1
                    if(cubeColorData[i][j][k]== Color.YELLOW):
                        yellowNum += 1
                    if(cubeColorData[i][j][k]== Color.GREEN):
                        greenNum += 1
                    if(cubeColorData[i][j][k]== Color.BLUE):
                        blueNum += 1   
        if(whiteNum != 9):
            startErrorMessage.set("同個顏色總共必須剛好9格!")
            return
        if(redNum != 9):
            startErrorMessage.set("同個顏色總共必須剛好9格!")
            return
        if(orangeNum != 9):
            startErrorMessage.set("同個顏色總共必須剛好9格!")
            return
        if(yellowNum != 9):
            startErrorMessage.set("同個顏色總共必須剛好9格!")
            return
        if(greenNum != 9):
            startErrorMessage.set("同個顏色總共必須剛好9格!")
            return
        if(blueNum != 9):
            startErrorMessage.set("同個顏色總共必須剛好9格!")
            return
                         
##########################################################
#                         主程式          
##########################################################

#產生視窗
window = tk.Tk()
window.title('cubeGUI')
window.geometry('{}x{}'.format(standardPixelSize*16, standardPixelSize*18))

#視窗字體樣式設定
fontstyle1 = tkFont.Font(family="Helvetica", size=12)

#window下的子視窗元件
title                       = tk.Label(window,bg='green', fg='yellow',font=('Arial', 25), width=15, text='解魔術方塊工具')    #主標題
spaceBelowTitle             = tk.Frame(window, width = standardPixelSize*13, height = standardPixelSize*0.4)    #空白
sixFaceOfCubeArea           = tk.Frame(window, width = standardPixelSize*13, height = standardPixelSize*9.5)    #魔術方塊每一面的九宮格
spaceBelowsixFaceOfCubeArea = tk.Frame(window, width = standardPixelSize*13, height = standardPixelSize*0.4)    #空白
setColorArea                = tk.Frame(window, width = standardPixelSize*13, height = standardPixelSize*1)      #填色區
spaceBelowSetColorArea      = tk.Frame(window, width = standardPixelSize*13, height = standardPixelSize*1)      #空白
start                       = tk.Frame(window, width = standardPixelSize*13, height = standardPixelSize*2)      #開始按鈕
title.grid(row=0,column=0)
spaceBelowTitle.grid(row=1,column=0)
sixFaceOfCubeArea.grid(row=2,column=0)
spaceBelowsixFaceOfCubeArea.grid(row=3,column=0) 
setColorArea.grid(row=4,column=0)
spaceBelowSetColorArea.grid(row=5,column=0)
start.grid(row=6,column=0)






#window -> sixFaceOfCubeArea(為了讓6個面呈十字排列，此區域裡可放3*4個九宮格)
sixFaceOfCubeArea.rowconfigure((0,1,2), weight = 1)
sixFaceOfCubeArea.columnconfigure((0,1,2,3), weight = 1)
sixFaceOfCubeArea.grid_propagate(0)
sixFaceOfCubeArea_faces = [0 for i in range(6)]    #魔術方塊的6個面
FaceButtons = [[[0 for col in range(3)] for row in range(3)] for face in range(6)]    #每一面有9個格子Button

#window -> sixFaceOfCubeArea(row 0:第0面)
sixFaceOfCubeArea_faces[0] = tk.Frame(sixFaceOfCubeArea, width = standardPixelSize*3, height =standardPixelSize*3)
sixFaceOfCubeArea_faces[0].grid(row=0,column=1)
for row in range(3):
    for col in range(3):
        #為了改用像素單位調整Button長寬，所以才把Button塞在Frame裡面，Frame的長寬即Button長寬
        FaceButtonFrame = tk.Frame(sixFaceOfCubeArea_faces[0],width=standardPixelSize,height=standardPixelSize)
        FaceButtonFrame.grid(row = int(row), column = int(col))        
        FaceButtonFrame.rowconfigure(0, weight = 1)
        FaceButtonFrame.columnconfigure(0, weight = 1)
        FaceButtonFrame.grid_propagate(0)#固定FaceButtonFrame的大小      
        FaceButtons[0][row][col] = tk.Button(FaceButtonFrame,bg = "white",command=lambda temprow = row,tempcol = col: clickFaceButton(FaceButtons,0,temprow,tempcol))
        FaceButtons[0][row][col].grid(sticky = "NSWE")#Button填滿整個Frame，使得Frame的長寬等於Button長寬
        
#window -> sixFaceOfCubeArea(row 1:第1~4面)    
for face in range(1,5):
    sixFaceOfCubeArea_faces[face] = tk.Frame(sixFaceOfCubeArea, width = standardPixelSize*3, height =standardPixelSize*3)
    sixFaceOfCubeArea_faces[face].grid(row=1,column=face-1)
    for row in range(3):
        for col in range(3):
            #為了改用像素單位調整Button長寬，所以才把Button塞在Frame裡面，Frame的長寬即Button長寬
            FaceButtonFrame = tk.Frame(sixFaceOfCubeArea_faces[face],width=standardPixelSize,height=standardPixelSize)
            FaceButtonFrame.grid(row = int(row), column = int(col))        
            FaceButtonFrame.rowconfigure(0, weight = 1)
            FaceButtonFrame.columnconfigure(0, weight = 1)
            FaceButtonFrame.grid_propagate(0)#固定FaceButtonFrame的大小        
            FaceButtons[face][row][col] = tk.Button(FaceButtonFrame,bg = "white",command=lambda tempface = face,temprow = row,tempcol = col: clickFaceButton(FaceButtons,tempface,temprow,tempcol))
            FaceButtons[face][row][col].grid(sticky = "NSWE")#Button填滿整個Frame，使得Frame的長寬等於Button長寬

#window -> sixFaceOfCubeArea(row 2:第5面)
sixFaceOfCubeArea_faces[5] = tk.Frame(sixFaceOfCubeArea, width = standardPixelSize*3, height =standardPixelSize*3)
sixFaceOfCubeArea_faces[5].grid(row=2,column=1)
for row in range(3):
    for col in range(3):
        #為了改用像素單位調整Button長寬，所以才把Button塞在Frame裡面，Frame的長寬即Button長寬
        FaceButtonFrame = tk.Frame(sixFaceOfCubeArea_faces[5],width=standardPixelSize,height=standardPixelSize)
        FaceButtonFrame.grid(row = int(row), column = int(col))        
        FaceButtonFrame.rowconfigure(0, weight = 1)
        FaceButtonFrame.columnconfigure(0, weight = 1)
        FaceButtonFrame.grid_propagate(0)#固定FaceButtonFrame的大小
        FaceButtons[5][row][col] = tk.Button(FaceButtonFrame,bg = "white",command=lambda temprow = row,tempcol = col: clickFaceButton(FaceButtons,5,temprow,tempcol))
        FaceButtons[5][row][col].grid(sticky = "NSWE")#Button填滿整個Frame，使得Frame的長寬等於Button長寬
        

#window -> setColorArea
ManuallySetColorButtons = [0 for i in range(6)]    
ManuallySetColorButtonBackground = ['white','red','orange','yellow','green','blue'] 
#為了改用像素單位調整Label長寬，所以才把Label塞在Frame裡面，Frame的長寬即Label長寬
setColorArea_titleFrame = tk.Frame(setColorArea,width = standardPixelSize*2.5, height = standardPixelSize*1)
setColorArea_titleFrame.rowconfigure(0, weight = 1)
setColorArea_titleFrame.columnconfigure(0, weight = 1)
setColorArea_titleFrame.grid_propagate(0)
setColorArea_titleFrame.grid(row = 0, column = 0)
setColorArea_titleLabel = tk.Label(setColorArea_titleFrame,fg='black',font=fontstyle1,text='手動填色')
setColorArea_titleLabel.grid(sticky = "NSWE")#Label填滿整個Frame，使得Frame的長寬等於Button長寬

manuallyChooseColorBlock = tk.Frame(setColorArea,width = standardPixelSize*0.7, height = standardPixelSize*0.7,bg='white',highlightbackground="black",highlightthickness=1)
manuallyChooseColorBlock.grid(row = 0, column = 1)

spaceOfSetColorArea1 = tk.Frame(setColorArea,width=standardPixelSize*0.5,height=standardPixelSize)#空白區域
spaceOfSetColorArea1.grid(row = 0, column = 2)
                                               
for i in range(6):
    #為了改用像素單位調整Button長寬，所以才把Button塞在Frame裡面，Frame的長寬即Button長寬
    ManuallySetColorButtonFrame = tk.Frame(setColorArea,width=standardPixelSize,height=standardPixelSize)
    ManuallySetColorButtonFrame.rowconfigure(0, weight = 1)
    ManuallySetColorButtonFrame.columnconfigure(0, weight = 1)
    ManuallySetColorButtonFrame.grid_propagate(0)
    ManuallySetColorButtonFrame.grid(row = 0, column = int(i)+3)
    ManuallySetColorButtons[i] = tk.Button(ManuallySetColorButtonFrame,font = fontstyle1,bg = ManuallySetColorButtonBackground[i],command=lambda tempi = i: clickManuallySetColorButton(manuallyChooseColorBlock,tempi))
    ManuallySetColorButtons[i].grid(sticky = "NSWE")#Button填滿整個Frame，使得Frame的長寬等於Button長寬
    
spaceOfSetColorArea2 = tk.Frame(setColorArea,width=standardPixelSize*1,height=standardPixelSize)#空白區域
spaceOfSetColorArea2.grid(row = 0, column = 9)

setColorByCameraButtonFrame = tk.Frame(setColorArea,width=standardPixelSize*5,height=standardPixelSize)
setColorByCameraButtonFrame.rowconfigure(0, weight = 1)
setColorByCameraButtonFrame.columnconfigure(0, weight = 1)
setColorByCameraButtonFrame.grid_propagate(0)
setColorByCameraButtonFrame.grid(row = 0, column = 10)
setColorByCameraButton = tk.Button(setColorByCameraButtonFrame,font = fontstyle1,bg = 'lightblue',text='影像辨識自動填色')
setColorByCameraButton.grid(sticky = "NSWE")

#window -> start
startErrorMessage = tk.StringVar()    #錯誤訊息內容(按下開始按鈕後，若出現錯誤，則顯示錯誤訊息)
startErrorMessage.set('')             #錯誤訊息初始化
startErrorMessageLabelFrame = tk.Frame(start,width=standardPixelSize*13,height=standardPixelSize*2)
startErrorMessageLabelFrame.rowconfigure(0, weight = 1)
startErrorMessageLabelFrame.columnconfigure(0, weight = 1)
startErrorMessageLabelFrame.grid_propagate(0)
startErrorMessageLabelFrame.grid(row=1,column=0)
startErrorMessageLabel = tk.Label(startErrorMessageLabelFrame,font = tkFont.Font(family="微軟正黑體", size=12),fg='red',textvariable=startErrorMessage)
startErrorMessageLabel.grid(sticky = "NSWE")


startButtonFrame = tk.Frame(start,width=standardPixelSize*6,height=standardPixelSize*1.5)
startButtonFrame.rowconfigure(0, weight = 1)
startButtonFrame.columnconfigure(0, weight = 1)
startButtonFrame.grid_propagate(0)
startButtonFrame.grid(row=0,column=0)
startButton = tk.Button(startButtonFrame,font = fontstyle1,bg = 'pink',text='START',command = lambda : clickStartButton())
startButton.grid(sticky = "NSWE")



window.mainloop()


