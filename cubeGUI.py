import tkinter
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

cube_color_data = [[[Color.WHITE for col in range(3)] for row in range(3)] for face in range(6)]#儲存每個魔術方塊格子的顏色資料
input_set_color = Color.WHITE    #手動填色功能中，目前選中的顏色 
face_btn_size = 35    #魔術方塊中，一格的邊大小(會影響到畫面上許多東西的大小)

##########################################################
#                          函式         
##########################################################
def face_block_btn_clicked(six_cube_face_faces_btns,face,row,col):
    #功能:被按的魔術方塊格子會改變顏色，同時也會更改對應格子的顏色的資料(cube_color_data[face][row][col])
    #參數:six_cube_face_faces_btns：所有魔術方塊格子按鈕  face:在魔術方塊的哪一面  num:是同一面中的第幾格
    global cube_color_data
    if input_set_color == Color.WHITE:
        six_cube_face_faces_btns[face][row][col].configure(bg = "white")
        cube_color_data[face][row][col] = Color.WHITE
    elif input_set_color == Color.RED:
        six_cube_face_faces_btns[face][row][col].configure(bg = "red")
        cube_color_data[face][row][col] = Color.RED
    elif input_set_color == Color.ORANGE:
        six_cube_face_faces_btns[face][row][col].configure(bg = "orange")
        cube_color_data[face][row][col] = Color.ORANGE
    elif input_set_color == Color.YELLOW:
        six_cube_face_faces_btns[face][row][col].configure(bg = "yellow")
        cube_color_data[face][row][col] = Color.YELLOW
    elif input_set_color == Color.GREEN:
        six_cube_face_faces_btns[face][row][col].configure(bg = "green")
        cube_color_data[face][row][col] = Color.GREEN
    elif input_set_color == Color.BLUE:
        six_cube_face_faces_btns[face][row][col].configure(bg = "blue")
        cube_color_data[face][row][col] = Color.BLUE

def set_color_input_block_btn_clicked(set_color_choosed_color,set_color_by_input_btns,i):
    #功能:按下調色盤的格子後，會改變input_set_color的值
    #參數:set_color_by_input_btns[i]:被按的那個格子
    global input_set_color
    if i == 0:
        input_set_color = Color.WHITE 
        set_color_choosed_color.configure(bg = "white")
    elif i == 1:
        input_set_color = Color.RED 
        set_color_choosed_color.configure(bg = "red")
    elif i == 2:
        input_set_color = Color.ORANGE
        set_color_choosed_color.configure(bg = "orange")
    elif i == 3:
        input_set_color = Color.YELLOW 
        set_color_choosed_color.configure(bg = "yellow")
    elif i == 4:
        input_set_color = Color.GREEN 
        set_color_choosed_color.configure(bg = "green")
    elif i == 5:
        input_set_color = Color.BLUE 
        set_color_choosed_color.configure(bg = "blue")

def start_btn_clicked():
    #功能：在開始執行轉回魔術方塊之前，簡單檢查一下魔術方塊能不能成功轉回來
    
    #1.判斷每面的中間格子顏色是否重複出現
    center_block = []
    for i in range(6):
        center_block.append(cube_color_data[i][1][1])
    if len(set(center_block))!=len(center_block):
        print("輸入格式有誤!(每一面中間的格子顏色不能重複)")
        return
    
    #2.判斷每面的中間格子的對面格子顏色是否符合
    if(True):
        if(center_block[0] == Color.WHITE and center_block[5] != Color.YELLOW):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[0] == Color.RED and center_block[5] != Color.ORANGE):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[0] == Color.ORANGE and center_block[5] != Color.RED):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[0] == Color.YELLOW and center_block[5] != Color.WHITE):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[0] == Color.GREEN and center_block[5] != Color.BLUE):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[0] == Color.BLUE and center_block[5] != Color.GREEN):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[1] == Color.WHITE and center_block[3] != Color.YELLOW):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[1] == Color.RED and center_block[3] != Color.ORANGE):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[1] == Color.ORANGE and center_block[3] != Color.RED):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[1] == Color.YELLOW and center_block[3] != Color.WHITE):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[1] == Color.GREEN and center_block[3] != Color.BLUE):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[1] == Color.BLUE and center_block[3] != Color.GREEN):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[2] == Color.WHITE and center_block[4] != Color.YELLOW):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[2] == Color.RED and center_block[4] != Color.ORANGE):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[2] == Color.ORANGE and center_block[4] != Color.RED):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[2] == Color.YELLOW and center_block[4] != Color.WHITE):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[2] == Color.GREEN and center_block[4] != Color.BLUE):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return
        if(center_block[2] == Color.BLUE and center_block[4] != Color.GREEN):
            print("輸入格式有誤!(每一面中間格子的對面格子顏色不符合)")
            return

    #3.每個顏色必須恰好出現9次
    if(True):
        white_num = 0
        red_num = 0
        orange_num = 0
        yellow_num = 0
        green_num = 0
        blue_num = 0
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if(cube_color_data[i][j][k]== Color.WHITE):
                        white_num += 1
                    if(cube_color_data[i][j][k]== Color.RED):
                        red_num += 1
                    if(cube_color_data[i][j][k]== Color.ORANGE):
                        orange_num += 1
                    if(cube_color_data[i][j][k]== Color.YELLOW):
                        yellow_num += 1
                    if(cube_color_data[i][j][k]== Color.GREEN):
                        green_num += 1
                    if(cube_color_data[i][j][k]== Color.BLUE):
                        blue_num += 1   
        if(white_num != 9):
            print("輸入格式有誤!(同個顏色必須總共剛好9格)")
            return
        if(red_num != 9):
            print("輸入格式有誤!(同個顏色必須總共剛好9格)")
            return
        if(orange_num != 9):
            print("輸入格式有誤!(同個顏色必須總共剛好9格)")
            return
        if(yellow_num != 9):
            print("輸入格式有誤!(同個顏色必須總共剛好9格)")
            return
        if(green_num != 9):
            print("輸入格式有誤!(同個顏色必須總共剛好9格)")
            return
        if(blue_num != 9):
            print("輸入格式有誤!(同個顏色必須總共剛好9格)")
            return
        
                    
##########################################################
#                         主程式          
##########################################################

#產生視窗
window = tkinter.Tk()
window.title('cubeGUI')
window.geometry('{}x{}'.format(face_btn_size*16, face_btn_size*15))

#視窗字體樣式設定
fontstyle_0 = tkFont.Font(family="Helvetica", size=10, weight = tkFont.BOLD)
fontstyle_1 = tkFont.Font(family="Helvetica", size=12)

#window's child
window_child_width = 13
title                 = tkinter.Label(window,bg='green', fg='yellow',font=('Arial', 25), width=15, text='解魔術方塊工具')    #主標題
space_below_title     = tkinter.Frame(window, width = face_btn_size*window_child_width, height = face_btn_size*0.2)    #空白
six_cube_face         = tkinter.Frame(window, width = face_btn_size*13, height = face_btn_size*9.5)    #魔術方塊每一面的九宮格
space_above_set_color = tkinter.Frame(window, width = face_btn_size*window_child_width, height = face_btn_size*0.2)    #空白
set_color             = tkinter.Frame(window, width = face_btn_size*window_child_width, height = face_btn_size*1)    #填色區
start                 = tkinter.Frame(window, width = face_btn_size*window_child_width, height = face_btn_size*2)    #開始按鈕
title.grid(row=0,column=0)
space_below_title.grid(row=1,column=0)
six_cube_face.grid(row=2,column=0)
space_above_set_color.grid(row=3,column=0) 
set_color.grid(row=4,column=0)
start.grid(row=5,column=0)

#window -> six_cube_face
six_cube_face_faces = [0 for i in range(6)]    #6個面的九宮格
six_cube_face_faces_btns = [[[0 for col in range(3)] for row in range(3)] for face in range(6)]    #每一面的9個格子按鈕

#window -> six_cube_face(row 0)
six_cube_face_faces[0] = tkinter.Frame(six_cube_face, width = face_btn_size*3, height =face_btn_size*3)
six_cube_face_faces[0].grid(row=0,column=1)
for j in range(3):#每個九宮格裡有3列
    for k in range(3):#每列有3格
        face_block = tkinter.Frame(six_cube_face_faces[0],width=face_btn_size,height=face_btn_size)
        six_cube_face_faces_btns[0][j][k] = tkinter.Button(face_block,font = fontstyle_0,bg = "white",command=lambda tempj = j,tempk = k: face_block_btn_clicked(six_cube_face_faces_btns,0,tempj,tempk))
        face_block.grid(row = int(j), column = int(k))
        #為了方便調整格子按鈕長寬，每個格子按鈕都各放在face_block裡面並填滿，所以face_block長寬即格子按鈕長寬，如果看到下面有類似的程式碼，也是一樣的概念
        face_block.rowconfigure(0, weight = 1)
        face_block.columnconfigure(0, weight = 1)
        face_block.grid_propagate(0)#固定face_block的大小
        six_cube_face_faces_btns[0][j][k].grid(sticky = "NSWE")
        
#window -> six_cube_face(row 1)    
for i in range(1,5):#創建六個九宮格的視窗元件
    six_cube_face_faces[i] = tkinter.Frame(six_cube_face, width = face_btn_size*3, height =face_btn_size*3)
    six_cube_face_faces[i].grid(row=1,column=i-1)
    for j in range(3):#每個九宮格裡有3列
        for k in range(3):#每列有3格
            face_block = tkinter.Frame(six_cube_face_faces[i],width=face_btn_size,height=face_btn_size)
            six_cube_face_faces_btns[i][j][k] = tkinter.Button(face_block,font = fontstyle_0,bg = "white",command=lambda tempi = i,tempj = j,tempk = k: face_block_btn_clicked(six_cube_face_faces_btns,tempi,tempj,tempk))
            face_block.grid(row = int(j), column = int(k))
            face_block.rowconfigure(0, weight = 1)
            face_block.columnconfigure(0, weight = 1)
            face_block.grid_propagate(0)#固定face_block的大小
            six_cube_face_faces_btns[i][j][k].grid(sticky = "NSWE")

#window -> six_cube_face(row 2)
six_cube_face_faces[5] = tkinter.Frame(six_cube_face, width = face_btn_size*3, height =face_btn_size*3)
six_cube_face_faces[5].grid(row=2,column=1)
for j in range(3):#每個九宮格裡有3列
    for k in range(3):#每列有3格
        face_block = tkinter.Frame(six_cube_face_faces[5],width=face_btn_size,height=face_btn_size)
        six_cube_face_faces_btns[5][j][k] = tkinter.Button(face_block,font = fontstyle_0,bg = "white",command=lambda tempj = j,tempk = k: face_block_btn_clicked(six_cube_face_faces_btns,5,tempj,tempk))
        face_block.grid(row = int(j), column = int(k))
        face_block.rowconfigure(0, weight = 1)
        face_block.columnconfigure(0, weight = 1)
        face_block.grid_propagate(0)#固定face_block的大小
        six_cube_face_faces_btns[5][j][k].grid(sticky = "NSWE")
        
six_cube_face.rowconfigure((0,1,2), weight = 1)
six_cube_face.columnconfigure((0,1,2,3), weight = 1)
six_cube_face.grid_propagate(0)


#window -> set_color
set_color_by_input_btns = [0 for i in range(6)]    
set_color_by_input_btn_text =['white','red','orange','yellow','green','blue'] 

set_color_title_frame = tkinter.Frame(set_color,width = face_btn_size*2.5, height = face_btn_size*1)
set_color_title_label = tkinter.Label(set_color_title_frame,fg='black',font=fontstyle_1,text='手動填色')
set_color_title_frame.rowconfigure(0, weight = 1)
set_color_title_frame.columnconfigure(0, weight = 1)
set_color_title_frame.grid_propagate(0)
set_color_title_frame.grid(row = 0, column = 0)
set_color_title_label.grid(sticky = "NSWE")

set_color_choosed_color = tkinter.Frame(set_color,width = face_btn_size*0.7, height = face_btn_size*0.7,bg='white',highlightbackground="black",highlightthickness=1)
set_color_choosed_color.grid(row = 0, column = 1)

set_color_space1 = tkinter.Frame(set_color,width=face_btn_size*0.5,height=face_btn_size)
set_color_space1.grid(row = 0, column = 2)
                                               
for i in range(6):
    color_input_block = tkinter.Frame(set_color,width=face_btn_size,height=face_btn_size)
    set_color_by_input_btns[i] = tkinter.Button(color_input_block,font = fontstyle_1,bg = set_color_by_input_btn_text[i],command=lambda tempi = i: set_color_input_block_btn_clicked(set_color_choosed_color,set_color_by_input_btns,tempi))
    color_input_block.rowconfigure(0, weight = 1)
    color_input_block.columnconfigure(0, weight = 1)
    color_input_block.grid_propagate(0)
    color_input_block.grid(row = 0, column = int(i)+3)
    set_color_by_input_btns[i].grid(sticky = "NSWE")
    
set_color_space2 = tkinter.Frame(set_color,width=face_btn_size*1,height=face_btn_size)
set_color_space2.grid(row = 0, column = 9)

set_color_by_camera_block = tkinter.Frame(set_color,width=face_btn_size*5,height=face_btn_size)
set_color_by_camera_btn = tkinter.Button(set_color_by_camera_block,font = fontstyle_1,bg = 'lightblue',text='影像辨識自動填色')
set_color_by_camera_block.rowconfigure(0, weight = 1)
set_color_by_camera_block.columnconfigure(0, weight = 1)
set_color_by_camera_block.grid_propagate(0)
set_color_by_camera_block.grid(row = 0, column = 10)
set_color_by_camera_btn.grid(sticky = "NSWE")

#window -> start
start_space = tkinter.Frame(start,width=face_btn_size*1.5,height=face_btn_size*1)
start_space.grid(row = 0, column = 0)

start_block = tkinter.Frame(start,width=face_btn_size*6,height=face_btn_size*1.5)
start_btn = tkinter.Button(start_block,font = fontstyle_1,bg = 'pink',text='START',command = start_btn_clicked)
start_block.rowconfigure(0, weight = 1)
start_block.columnconfigure(0, weight = 1)
start_block.grid_propagate(0)
start_block.grid(row=1,column=0)
start_btn.grid(sticky = "NSWE")

window.mainloop()


