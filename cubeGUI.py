import tkinter as tk
import tkinter.font as tkFont
import Cube3x3 as Cube
import squ
import twophase.solver as sv
import RoundedCornerFrame as rcf
#import stepperMotorSolver as s_motor
##########################################################
#                        全域變數          
##########################################################

#資料
cubeColorData = [[['w' for col in range(3)] for row in range(3)] for face in range(6)]    #儲存每個魔術方塊格子的顏色資料
cubeColorDataString =""     #用字串表示魔術方塊格子的顏色資料
manuallySelectedColors = 'w'    #手動填色功能中，目前選中的顏色 
faceInitialColor = ['w','o','g','r','b','y'] #每一面的初始顏色

#畫面
standardPixelSize = 35    #會影響畫面上所有元件的大小(其值相當於魔術方塊中一格的邊長)
windowWidthMultiple = 13    #視窗寬度 = standardPixelSize * windowWidthMultiple
windowHeightMultiple = 14    #視窗高度 = standardPixelSize * windowHeightMultiple
functionBackgroundColor = "CadetBlue"   #操作功能區(functionArea)背景顏色
FaceButtons = [[[0 for col in range(3)] for row in range(3)] for face in range(6)]    #每一面有9個格子Button

##########################################################
#                          函式         
##########################################################
def cubeColorDataToString():
    #功能:把魔術方塊顏色資料轉成字串輸出
    global cubeColorData
    global cubeColorDataString
    cubeColorDataString = ''.join(str(i[0]) for row in cubeColorData for col in row for i in col)
    
def clickFaceButton(event,FaceButtons,face,row,col):
    #功能:被按的魔術方塊格子按鈕會根據manuallySelectedColors的值改變顏色，同時也會更改此格的顏色資料(cubeColorData[face][row][col])
    #參數:FaceButtons：所有魔術方塊格子按鈕  face:在魔術方塊的哪一面  num:是同一面中的第幾格
    global cubeColorData
    
    if manuallySelectedColors == 'w':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "white")
        cubeColorData[face][row][col] = 'w'
        
    elif manuallySelectedColors == 'r':
        FaceButtons[face][row][col].changeBackgroundColor(bg="red")
        cubeColorData[face][row][col] = 'r'
        
    elif manuallySelectedColors == 'o':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "orange")
        cubeColorData[face][row][col] = 'o'
        
    elif manuallySelectedColors == 'y':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "yellow")
        cubeColorData[face][row][col] = 'y'
        
    elif manuallySelectedColors == 'g':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "limegreen")
        cubeColorData[face][row][col] = 'g'
        
    elif manuallySelectedColors == 'b':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "blue")
        cubeColorData[face][row][col] = 'b'


def mouseEnterFaceButton(event,FaceButtons,face,row,col):
    #功能:滑鼠移動到魔術方塊格子按鈕上會有特效，不會更改此格的顏色資料(cubeColorData[face][row][col])
    #參數:FaceButtons：所有魔術方塊格子按鈕  face:在魔術方塊的哪一面  num:是同一面中的第幾格    
    global cubeColorData
    if cubeColorData[face][row][col] == 'w':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "silver")
        
    elif cubeColorData[face][row][col] == 'r':
        FaceButtons[face][row][col].changeBackgroundColor(bg="DarkRed")
        
    elif cubeColorData[face][row][col] == 'o':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "Chocolate")
        cubeColorData[face][row][col] = 'o'
        
    elif cubeColorData[face][row][col] == 'y':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "goldenrod")
        
    elif cubeColorData[face][row][col] == 'g':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "darkgreen")
        
    elif cubeColorData[face][row][col] == 'b':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "Darkblue")
    
def mouseLeaveFaceButton(event,FaceButtons,face,row,col):
    #功能:滑鼠從魔術方塊格子按鈕裡移開會有特效，不會更改此格的顏色資料(cubeColorData[face][row][col])
    #參數:FaceButtons：所有魔術方塊格子按鈕  face:在魔術方塊的哪一面  num:是同一面中的第幾格    
    global cubeColorData
    if cubeColorData[face][row][col] == 'w':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "white")
        
    elif cubeColorData[face][row][col] == 'r':
        FaceButtons[face][row][col].changeBackgroundColor(bg="red")
        
    elif cubeColorData[face][row][col] == 'o':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "orange")
        cubeColorData[face][row][col] = 'o'
        
    elif cubeColorData[face][row][col] == 'y':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "yellow")
        
    elif cubeColorData[face][row][col] == 'g':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "limegreen")
        
    elif cubeColorData[face][row][col] == 'b':
        FaceButtons[face][row][col].changeBackgroundColor(bg = "blue")   
        
def clickManuallySetColorButton(event,manuallyChooseColorBlock,i):
    #功能:按下手動調色盤的顏色格子按鈕後，會改變manuallySelectedColors的值
    #參數:manuallyChooseColorBlock:被選中的顏色會顯示在這裡  i:第幾個顏色
    global manuallySelectedColors
    if i == 0:
        manuallySelectedColors = 'w' 
        manuallyChooseColorBlock.configure(bg = "white")
    elif i == 1:
        manuallySelectedColors = 'r' 
        manuallyChooseColorBlock.configure(bg = "red")
    elif i == 2:
        manuallySelectedColors = 'o'
        manuallyChooseColorBlock.configure(bg = "orange")
    elif i == 3:
        manuallySelectedColors = 'y' 
        manuallyChooseColorBlock.configure(bg = "yellow")
    elif i == 4:
        manuallySelectedColors = 'g' 
        manuallyChooseColorBlock.configure(bg = "limegreen")
    elif i == 5:
        manuallySelectedColors = 'b' 
        manuallyChooseColorBlock.configure(bg = "blue")
        
def mouseEnterManuallySetColorButton(event,manuallySetColorButtons,i):
    if i == 0:
        manuallySetColorButtons[i].configure(bg = "silver")
    elif i == 1:
        manuallySetColorButtons[i].configure(bg = "DarkRed")
    elif i == 2:
        manuallySetColorButtons[i].configure(bg = "Chocolate")
    elif i == 3:
        manuallySetColorButtons[i].configure(bg = "goldenrod")
    elif i == 4:
        manuallySetColorButtons[i].configure(bg = "darkgreen")
    elif i == 5: 
        manuallySetColorButtons[i].configure(bg = "Darkblue")

def mouseLeaveManuallySetColorButton(event,manuallySetColorButtons,i):
    if i == 0:
        manuallySetColorButtons[i].configure(bg = "white")
    elif i == 1:
        manuallySetColorButtons[i].configure(bg = "red")
    elif i == 2:
        manuallySetColorButtons[i].configure(bg = "orange")
    elif i == 3:
        manuallySetColorButtons[i].configure(bg = "yellow")
    elif i == 4:
        manuallySetColorButtons[i].configure(bg = "limegreen")
    elif i == 5: 
        manuallySetColorButtons[i].configure(bg = "blue")
        
def mouseEnterFunctionButton(event,functionButton,color="blue"):
    functionButton.configure(fg = color)
  
def mouseLeaveFunctionButton(event,functionButton):
    functionButton.configure(fg = "black")    

def resetSixFaceColor():
    for face in range(0,6):
        for row in range(3):
            for col in range(3):
                if faceInitialColor[face] == 'w':
                    FaceButtons[face][row][col].changeBackgroundColor(bg = "white")
                    cubeColorData[face][row][col] = 'w'
                elif faceInitialColor[face] == 'r':
                    FaceButtons[face][row][col].changeBackgroundColor(bg="red")
                    cubeColorData[face][row][col] = 'r'         
                elif faceInitialColor[face] == 'o':
                    FaceButtons[face][row][col].changeBackgroundColor(bg = "orange")
                    cubeColorData[face][row][col] = 'o'   
                elif faceInitialColor[face] == 'y':
                    FaceButtons[face][row][col].changeBackgroundColor(bg = "yellow")
                    cubeColorData[face][row][col] = 'y'     
                elif faceInitialColor[face] == 'g':
                    FaceButtons[face][row][col].changeBackgroundColor(bg = "limegreen")
                    cubeColorData[face][row][col] = 'g'         
                elif faceInitialColor[face] == 'b':
                    FaceButtons[face][row][col].changeBackgroundColor(bg = "blue")
                    cubeColorData[face][row][col] = 'b'

def clickStartButton():
    #功能：按下開始執行按鈕的事件，轉回魔術方塊之前，簡單檢查一下魔術方塊能不能成功轉回來
    
    #1.錯誤檢查：每面的中間格子顏色是否重複出現
    centerBlock = []
    for i in range(6):
        centerBlock.append(cubeColorData[i][1][1])
    if len(set(centerBlock))!=len(centerBlock):
        result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子的顏色不能重複!")
        return
    
    #2.錯誤檢查：每面的中間格子的對面格子顏色是否符合
    if(True):
        if(centerBlock[0] == 'w' and centerBlock[5] != 'y'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：上面(第1面)與下面(第6面)\n-情況：「白」沒對到「黃」")
            return
        if(centerBlock[0] == 'r' and centerBlock[5] != 'o'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：上面(第1面)與下面(第6面)\n-情況：「紅」沒對到「橘」")
            return
        if(centerBlock[0] == 'o' and centerBlock[5] != 'r'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：上面(第1面)與下面(第6面)\n-情況：「紅」沒對到「橘」")
            return
        if(centerBlock[0] == 'y' and centerBlock[5] != 'w'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：上面(第1面)與下面(第6面)\n-情況：「白」沒對到「黃」")
            return
        if(centerBlock[0] == 'g' and centerBlock[5] != 'b'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：上面(第1面)與下面(第6面)\n-情況：「綠」沒對到「藍」")
            return
        if(centerBlock[0] == 'b' and centerBlock[5] != 'g'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：上面(第1面)與下面(第6面)\n-情況：「綠」沒對到「藍」")
            return
        if(centerBlock[1] == 'w' and centerBlock[3] != 'y'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：左面(第2面)與右面(第4面)\n-情況：「白」沒對到「黃」")
            return
        if(centerBlock[1] == 'r' and centerBlock[3] != 'o'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：左面(第2面)與右面(第4面)\n-情況：「紅」沒對到「橘」")
            return
        if(centerBlock[1] == 'o' and centerBlock[3] != 'r'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：左面(第2面)與右面(第4面)\n-情況：「紅」沒對到「橘」")
            return
        if(centerBlock[1] == 'y' and centerBlock[3] != 'w'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：左面(第2面)與右面(第4面)\n-情況：「白」沒對到「黃」")
            return
        if(centerBlock[1] == 'g' and centerBlock[3] != 'b'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：左面(第2面)與右面(第4面)\n-情況：「綠」沒對到「藍」")
            return
        if(centerBlock[1] == 'b' and centerBlock[3] != 'g'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：左面(第2面)與右面(第4面)\n-情況：「綠」沒對到「藍」")
            return
        if(centerBlock[2] == 'w' and centerBlock[4] != 'y'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：前面(第3面)與後面(第5面)\n-情況：「白」沒對到「黃」")
            return
        if(centerBlock[2] == 'r' and centerBlock[4] != 'o'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：前面(第3面)與後面(第5面)\n-情況：「紅」沒對到「橘」")
            return
        if(centerBlock[2] == 'o' and centerBlock[4] != 'r'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：前面(第3面)與後面(第5面)\n-情況：「紅」沒對到「橘」")
            return
        if(centerBlock[2] == 'y' and centerBlock[4] != 'w'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：前面(第3面)與後面(第5面)\n-情況：「白」沒對到「黃」")
            return
        if(centerBlock[2] == 'g' and centerBlock[4] != 'b'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：前面(第3面)與後面(第5面)\n-情況：「綠」沒對到「藍」")
            return
        if(centerBlock[2] == 'b' and centerBlock[4] != 'g'):
            result = tk.messagebox.showerror(title ="錯誤",message="每一面中間格子與它對面的中間格子顏色必須對到!\n\n-位置：前面(第3面)與後面(第5面)\n-情況：「綠」沒對到「藍」")
            return

    #3.錯誤檢查：每個顏色必須恰好出現9次
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
                    if(cubeColorData[i][j][k][0]== 'w'):
                        whiteNum += 1
                    if(cubeColorData[i][j][k][0]== 'r'):
                        redNum += 1
                    if(cubeColorData[i][j][k][0]== 'o'):
                        orangeNum += 1
                    if(cubeColorData[i][j][k][0]== 'y'):
                        yellowNum += 1
                    if(cubeColorData[i][j][k][0]== 'g'):
                        greenNum += 1
                    if(cubeColorData[i][j][k][0]== 'b'):
                        blueNum += 1   
        nineColorErrorMessage = "每個顏色必須剛好9格!\n"  
        nineColorIsOK = 1
        if(whiteNum != 9):
            nineColorErrorMessage = nineColorErrorMessage +"\n-(白色：{}格)".format(whiteNum)
            nineColorIsOK = 0
        if(redNum != 9):
            nineColorErrorMessage = nineColorErrorMessage +"\n-(紅色：{}格)".format(redNum)
            nineColorIsOK = 0
        if(orangeNum != 9):
            nineColorErrorMessage = nineColorErrorMessage +"\n-(橘色：{}格)".format(orangeNum)
            nineColorIsOK = 0
        if(yellowNum != 9):
            nineColorErrorMessage = nineColorErrorMessage +"\n-(黃色：{}格)".format(yellowNum)
            nineColorIsOK = 0
        if(greenNum != 9):
            nineColorErrorMessage = nineColorErrorMessage +"\n-(綠色：{}格)".format(greenNum)
            nineColorIsOK = 0
        if(blueNum != 9):
            nineColorErrorMessage = nineColorErrorMessage +"\n-(藍色：{}格)".format(blueNum)
            nineColorIsOK = 0
        if nineColorIsOK == 0: 
            result = tk.messagebox.showerror(title ="錯誤",message=nineColorErrorMessage)
            return
  
    #4.將魔術方塊資料輸出成字串
    cubeColorDataToString()      
    
    #5.透過演算法得出解，並執行旋轉
    solveString = sv.solve(string_covert(cubeColorDataString))
    print(solveString)
   # s_motor.startRotation(solveString)

def string_covert(color_str):
    result = ''
    color_dict = {color_str[ 4]: 'U',
                  color_str[31]: 'R',
                  color_str[22]: 'F',
                  color_str[49]: 'D',
                  color_str[13]: 'L',
                  color_str[40]: 'B'}
    for i in range(0, 9):
        result += color_dict[color_str[i]]
    for i in range(27, 36):
        result += color_dict[color_str[i]]
    for i in range(18, 27):
        result += color_dict[color_str[i]]
    for i in range(45, 54):
        result += color_dict[color_str[i]]
    for i in range(9, 18):
        result += color_dict[color_str[i]]
    for i in range(36, 45):
        result += color_dict[color_str[i]]
    return result

def imageRecognition():
    #功能:將圖片中的魔術方塊讀出，並存入到陣列
    from rubikscolorresolver.solver import resolve_colors as color
    from rubikscubetracker import RubiksVideo as rbvideo
    from rubikscubetracker import RubiksImage as rbimg
    rba=rbvideo(0)
    #rbb=rbimg()
    #rbb.analyze_file("F:107334.jpg",3)
    #print(dir(rba))
    rba.analyze_webcam()
    
    arg=["",'--filename', 'webcam.json']
    ans=color(arg)
    ir=squ.imageRecognitioner()
    for i in range(6):
        for row in range(3):
            for col in range(3):
                # cubeColorData[i][col][row]=ir.getColor('img/'+str(i+1)+'.jpg')[row][col]
                cubeColorData[i][col][row]=ans[col*3+row+i*9]
    print(cubeColorData)
    cubeColorDataToString()
    updateGUIcube()

def updateGUIcube():
    #功能:更新視窗裡的魔術方塊
    long_color_name_dict={'r':'red','g':'limegreen','o':'orange','b':'blue','y':'yellow','w':'white'}
    for face in range(6):
        for row in range(3):
            for col in range(3):
                FaceButtons[face][row][col].changeBackgroundColor(bg = long_color_name_dict[cubeColorData[face][row][col]])

def solveCube():
    #功能:將字串交給solver並給出解答
    # print(cubeColorDataString)
    print(cubeColorDataString)
    cube1 = Cube.Cube3x3(cubeColorDataString)
    print(cube1.solve())

def imageRecognitionShow():
    #功能:show出找到的圖
    ir=squ.imageRecognitioner()
    ir.example()
##########################################################
#                         主程式          
##########################################################

#產生視窗
window = tk.Tk()
window.title('解魔術方塊工具')
windowWidth = standardPixelSize*windowWidthMultiple
windowHeight = standardPixelSize*windowHeightMultiple+20
window.geometry('{}x{}'.format(windowWidth,windowHeight))
window.geometry("+%d+%d" % (window.winfo_screenwidth()/2 - windowWidth/2, window.winfo_screenheight()/2 - windowHeight/2))
#window.iconbitmap('cubeGUI_iocn.ico')
cubeColorDataToString()

#視窗字體樣式設定
fontstyle1 = tkFont.Font(family="微軟正黑體", size=14)

#window下的子視窗元件
spaceBelowTitle             = tk.Frame(window, width = standardPixelSize*windowWidthMultiple, height = standardPixelSize*0.5)    #空白
sixFaceOfCubeArea           = tk.Frame(window, width = standardPixelSize*12, height = standardPixelSize*9)    #魔術方塊每一面的九宮格
spaceBelowsixFaceOfCubeArea = tk.Frame(window, width = standardPixelSize*windowWidthMultiple, height = standardPixelSize*0.5)    #空白
functionArea                = tk.Frame(window, width = standardPixelSize*windowWidthMultiple, height = standardPixelSize*10,bg=functionBackgroundColor)      #功能區
spaceBelowTitle.grid(row=1,column=0)
sixFaceOfCubeArea.grid(row=2,column=0)
spaceBelowsixFaceOfCubeArea.grid(row=3,column=0) 
functionArea.grid(row=4,column=0)

#window -> sixFaceOfCubeArea(為了讓6個面呈十字排列，此區域裡可放3*4個九宮格)
sixFaceOfCubeArea.rowconfigure((0,1,2), weight = 1)
sixFaceOfCubeArea.columnconfigure((0,1,2,3), weight = 1)
sixFaceOfCubeArea.grid_propagate(0)
sixFaceOfCubeArea_faces = [0 for i in range(6)]    #魔術方塊的6個面


#window -> sixFaceOfCubeArea -> row 0(第0面)
sixFaceOfCubeArea_faces[0] = tk.Frame(sixFaceOfCubeArea, width = standardPixelSize*3, height =standardPixelSize*3)
sixFaceOfCubeArea_faces[0].grid(row=0,column=1)
for row in range(3):
    for col in range(3):
        FaceButtons[0][row][col] = rcf.RoundedCornerFrame(sixFaceOfCubeArea_faces[0],width=standardPixelSize,height=standardPixelSize,bd=2,borderColor="black",bg="white",cornerRadius=1)
        FaceButtons[0][row][col].bind('<Button-1>',lambda event,temprow = row,tempcol = col: clickFaceButton(event,FaceButtons,0,temprow,tempcol))
        FaceButtons[0][row][col].bind('<Enter>',lambda event,temprow = row,tempcol = col:mouseEnterFaceButton(event,FaceButtons,0,temprow,tempcol))
        FaceButtons[0][row][col].bind('<Leave>',lambda event,temprow = row,tempcol = col:mouseLeaveFaceButton(event,FaceButtons,0,temprow,tempcol))
        FaceButtons[0][row][col].grid(row = int(row), column = int(col))
        
#window -> sixFaceOfCubeArea -> row 1(第1~4面)  
for face in range(1,5):
    sixFaceOfCubeArea_faces[face] = tk.Frame(sixFaceOfCubeArea, width = standardPixelSize*3, height =standardPixelSize*3)
    sixFaceOfCubeArea_faces[face].grid(row=1,column=face-1)
    for row in range(3):
        for col in range(3):
            FaceButtons[face][row][col] = rcf.RoundedCornerFrame(sixFaceOfCubeArea_faces[face],width=standardPixelSize,height=standardPixelSize,bd=2,borderColor="black",bg="white",cornerRadius=1)
            FaceButtons[face][row][col].bind('<Button-1>',lambda event,tempface = face,temprow = row,tempcol = col: clickFaceButton(event,FaceButtons,tempface,temprow,tempcol))
            FaceButtons[face][row][col].bind('<Enter>',lambda event,tempface = face,temprow = row,tempcol = col:mouseEnterFaceButton(event,FaceButtons,tempface,temprow,tempcol))
            FaceButtons[face][row][col].bind('<Leave>',lambda event,tempface = face,temprow = row,tempcol = col:mouseLeaveFaceButton(event,FaceButtons,tempface,temprow,tempcol))
            FaceButtons[face][row][col].grid(row = int(row), column = int(col))
            
#window -> sixFaceOfCubeArea -> row 2(第5面)
sixFaceOfCubeArea_faces[5] = tk.Frame(sixFaceOfCubeArea, width = standardPixelSize*3, height =standardPixelSize*3)
sixFaceOfCubeArea_faces[5].grid(row=2,column=1)
for row in range(3):
    for col in range(3):
        FaceButtons[5][row][col] = rcf.RoundedCornerFrame(sixFaceOfCubeArea_faces[5],width=standardPixelSize,height=standardPixelSize,bd=2,borderColor="black",bg="white",cornerRadius=1)
        FaceButtons[5][row][col].bind('<Button-1>',lambda event,temprow = row,tempcol = col: clickFaceButton(event,FaceButtons,5,temprow,tempcol))
        FaceButtons[5][row][col].bind('<Enter>',lambda event,temprow = row,tempcol = col:mouseEnterFaceButton(event,FaceButtons,5,temprow,tempcol))
        FaceButtons[5][row][col].bind('<Leave>',lambda event,temprow = row,tempcol = col:mouseLeaveFaceButton(event,FaceButtons,5,temprow,tempcol))
        FaceButtons[5][row][col].grid(row = int(row), column = int(col))
resetSixFaceColor()

#window -> functionArea
spaceAtTopOfFunctionArea = tk.Frame(functionArea, width = standardPixelSize*windowWidthMultiple, height = standardPixelSize*0.5,bg=functionBackgroundColor)    #空白
spaceAtTopOfFunctionArea.grid(row=0,column=0,columnspan=5)

setColorArea_titleFrame = tk.Frame(functionArea,width = standardPixelSize*3, height = standardPixelSize*1,bg=functionBackgroundColor)
setColorArea_titleFrame.rowconfigure(0, weight = 1)
setColorArea_titleFrame.columnconfigure(0, weight = 1)
setColorArea_titleFrame.grid_propagate(0)
setColorArea_titleLabel = tk.Label(setColorArea_titleFrame,fg='black',font=fontstyle1,bg=functionBackgroundColor,text='手動填色')
setColorArea_titleLabel.grid(row = 0, column = 0)#Label填滿整個Frame，使得Frame的長寬等於Button長寬
manuallyChoosedColorBlock = tk.Frame(setColorArea_titleFrame,width = standardPixelSize*0.7, height = standardPixelSize*0.7,bg='white',highlightbackground="black",highlightthickness=1)
manuallyChoosedColorBlock.grid(row = 0, column = 1)
setColorArea_titleFrame.grid(row = 1, column = 1,columnspan=2)


manuallySetColorButtonsBlock = tk.Frame(functionArea,width = standardPixelSize*5, height = standardPixelSize*2.5,bg="Khaki")
manuallySetColorButtonsBlock.config(highlightthickness=2,highlightbackground="black")
manuallySetColorButtonsBlock.grid(row = 2, column = 1,rowspan=2,columnspan=2)
manuallySetColorButtonsBlock.rowconfigure((0,1), weight = 1)
manuallySetColorButtonsBlock.columnconfigure((0,1,2), weight = 1)
manuallySetColorButtonsBlock.grid_propagate(0)
manuallySetColorButtons = [0 for i in range(6)]    
manuallySetColorButtonBackgroundColor = ['white','red','orange','yellow','limegreen','blue'] 
for i in range(6):
    #為了改用像素單位調整Button長寬，所以才把Button塞在Frame裡面，Frame的長寬即Button長寬
    manuallySetColorButtons[i] = tk.Frame(manuallySetColorButtonsBlock,cursor="hand2",width=standardPixelSize,height=standardPixelSize,bg=manuallySetColorButtonBackgroundColor[i])
    manuallySetColorButtons[i].config(highlightthickness=2,highlightbackground="black")
    manuallySetColorButtons[i].bind('<Button-1>',lambda event,tempi = i: clickManuallySetColorButton(event,manuallyChoosedColorBlock,tempi))
    manuallySetColorButtons[i].bind('<Enter>',lambda event,tempi = i: mouseEnterManuallySetColorButton(event,manuallySetColorButtons,tempi))
    manuallySetColorButtons[i].bind('<Leave>',lambda event,tempi = i: mouseLeaveManuallySetColorButton(event,manuallySetColorButtons,tempi))
    manuallySetColorButtons[i].grid(row = int(i/3), column = int(i%3))


setColorByCameraButtonFrame = tk.Frame(functionArea,width=standardPixelSize*6,height=standardPixelSize)
setColorByCameraButtonFrame.rowconfigure(0, weight = 1)
setColorByCameraButtonFrame.columnconfigure(0, weight = 1)
setColorByCameraButtonFrame.grid_propagate(0)
setColorByCameraButton = tk.Button(setColorByCameraButtonFrame,cursor="hand2",font = fontstyle1,bg = 'lightblue',text='影像辨識自動填色',anchor="center",command=imageRecognition)
setColorByCameraButton.bind("<Enter>",lambda event:mouseEnterFunctionButton(event,setColorByCameraButton))     
setColorByCameraButton.bind("<Leave>",lambda event:mouseLeaveFunctionButton(event,setColorByCameraButton))    
setColorByCameraButton.grid(sticky = "NSWE")
setColorByCameraButtonFrame.grid(row = 1, column = 3)

resetButtonFrame = tk.Frame(functionArea,width=standardPixelSize*6,height=standardPixelSize)
resetButtonFrame.rowconfigure(0, weight = 1)
resetButtonFrame.columnconfigure(0, weight = 1)
resetButtonFrame.grid_propagate(0)
resetButton = tk.Button(resetButtonFrame,cursor="hand2",font = fontstyle1,bg = 'lightblue',text='重設魔方顏色',anchor="center",command = lambda : resetSixFaceColor())
resetButton.bind("<Enter>",lambda event:mouseEnterFunctionButton(event,resetButton))     
resetButton.bind("<Leave>",lambda event:mouseLeaveFunctionButton(event,resetButton))  
resetButton.grid(sticky = "NSWE")
resetButtonFrame.grid(row=2,column=3)

startButtonFrame = tk.Frame(functionArea,width=standardPixelSize*6,height=standardPixelSize*1.2)
startButtonFrame.rowconfigure(0, weight = 1)
startButtonFrame.columnconfigure(0, weight = 1)
startButtonFrame.grid_propagate(0)
startButton = tk.Button(startButtonFrame,cursor="hand2",font = fontstyle1,bg = 'pink',text='開始',anchor="center",command = lambda : clickStartButton())
startButton.bind("<Enter>",lambda event:mouseEnterFunctionButton(event,startButton,"red"))     
startButton.bind("<Leave>",lambda event:mouseLeaveFunctionButton(event,startButton))  
startButton.grid(sticky = "NSWE")
startButtonFrame.grid(row=3,column=3)

spaceAtBottomOfFunctionArea = tk.Frame(functionArea, width = standardPixelSize*windowWidthMultiple, height = standardPixelSize*0.5,bg=functionBackgroundColor)    #空白
spaceAtBottomOfFunctionArea.grid(row=4,column=0,columnspan=5)

window.mainloop()


