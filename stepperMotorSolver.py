import RPi.GPIO as GPIO
import time, threading
from pynput import keyboard

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

'''全域變數'''
isPause = False
stepPerRound = 64 * 64 #使用8步模式旋轉馬達(未減速前轉一圈需64步，考慮減速比後轉一圈需64*64步)
pinHighLowCycle =[[1,0,0,0],
                  [1,1,0,0],
                  [0,1,0,0],
                  [0,1,1,0],
                  [0,0,1,0],
                  [0,0,1,1],
                  [0,0,0,1],
                  [1,0,0,1]]  #8步模式(8個電位模式)下每個pin腳輪流切換高低電位

class RotationThread(threading.Thread):
    def __init__(self,solveSteps=[]):
        
        super().__init__()
         
        self.solveSteps = solveSteps
        self.isRunning = True
        
        #__flag判斷執行緒是否暫停(.set()為繼續，.clear()為暫停)
        self.__flag = threading.Event()
        self.__flag.set()
        
        #__running判斷執行緒是否結束(.set()為執行中，.clear()為結束)
        self.__running = threading.Event()
        self.__running.set()

    def run(self):      
        i = 0   
        self.isRunning = True
        while self.__running.isSet():
            self.__flag.wait()    
            if(i>=len(self.solveSteps)-1):
                self.stop() 
            else:   
                blockRotation(self.solveSteps[i])
                i+=1        
                if(i>=len(self.solveSteps)-1):
                    self.stop()                         
            if isPause == True:              
                self.pause()
                print("暫停旋轉中...(請按「空白鍵」繼續)") 
            
    def pause(self):
        self.__flag.clear() 
                
    def resume(self):
        self.__flag.set()                       
    
    def stop(self):                         
        self.__flag.set()   
        self.__running.clear()        
        self.isRunning = False
        
        
rotationThread = RotationThread()  #建立開始旋轉的執行緒      
    
def on_release(key):
    global isPause    
    if key == keyboard.Key.space:             
        isPause = not isPause
        if rotationThread.isRunning == True and isPause ==True:
            print("當前步驟旋轉完後將暫停") 
        elif rotationThread.isRunning == True and isPause == False:
            rotationThread.resume()
            print("繼續旋轉...") 
    if key == keyboard.Key.esc:         
        # Stop listener    
        rotationThread.stop()
        return False 

def run(face,angleNum):

    '''初始化'''
    pin_stepper = [-1, -1, -1, -1]
    global stepPerRound
    global pinHighLowCycle
        
    '''設定pin腳位，決定哪一面要旋轉'''
    if face == "U":#上
        pin_stepper = [9, 11, 0, 5]
    elif face == "D":#下
        pin_stepper = [17, 27, 22, 10]
    elif face == "L":#左
        pin_stepper = [12, 16, 20, 21]
    elif face == "R":#右
        pin_stepper = [15, 18, 23, 24]
    elif face == "F":#前
        pin_stepper = [25, 8, 7, 1] 
    elif face == "B":#後
        pin_stepper = [6, 13, 19, 26]
    else:
        print('input error!!!')
        return     
    
    '''根據旋轉幾度設定馬達旋轉步數及方向'''
    stepsNeeded = 0    #旋轉一次所需步數(預設為0，代表不旋轉)
    direction = 1   #1為順時針，-1為逆時針(預設為順時針) 
    
    if angleNum == "1":     #90度
        stepsNeeded  = int(stepPerRound / 4)
        direction = -1
    elif angleNum == "2":   #180度
        stepsNeeded  = int(stepPerRound / 2)
        direction = -1
    elif angleNum == "3":   #270度(逆時針90度)
        stepsNeeded  = int(stepPerRound / 4)
        direction = 1
    else:
        print('input error!!!')
        return
    if face == "L" or face == "U":
        direction *=-1
    
    '''4個pin腳切到輸出模式，一開始設為低電位'''
    for pin in pin_stepper:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        
    '''設定馬達每一步的間隔時間'''
    waitingTime = 1/float(1000) #間隔1毫秒，經實測沒辦法再更短了
    
    '''開始旋轉'''
    cycleLength = len(pinHighLowCycle)
    pinsCount = len(pin_stepper)
    cycleIndex = 0 #在8步模式下，紀錄pin腳電位目前在第幾個電位模式
    
    while stepsNeeded > 0 :#while迴圈內做的事情是：馬達旋轉一步
        for pin in range(0, pinsCount):#根據目前的電位模式，設定每個pin腳的電位
            GPIO.output(pin_stepper[pin], pinHighLowCycle[cycleIndex][pin])  
        
        '''旋轉完畢後的動作'''
        stepsNeeded -= 1           #所需步數-1
        cycleIndex += direction    #根據旋轉方向變換電位方向
        cycleIndex %= cycleLength #根據旋轉方向變換電位方向
        
        time.sleep(waitingTime)
        
           
def blockRotation(step):
    #旋轉一個步驟
    face = step[0]
    angleNum = step[1]
    try:    
        run(face,angleNum)
    finally:
        print('{}{}旋轉ok!'.format(face,angleNum))     
        
def startRotation(solveString):
    '''利用演算法得出的解來解魔術方塊'''
    print("開始旋轉! (可按「空白」鍵暫停，「Esc」鍵強制結束程式)") 
    
    #將解法的字串轉成陣列
    solveResult = solveString.split('(')    
    solveResult = solveResult[0]
    solveSteps = solveResult.split(' ')
    
    #建立按鍵監聽的執行緒(按鍵監聽目的：可指定按鍵來暫停或強制停止旋轉)
    keyboard_listener=keyboard.Listener(on_release=on_release) 
    
    #開始執行旋轉與按鍵監聽  
    keyboard_listener.start()
    #rotationThread = RotationThread()  #建立開始旋轉的執行緒     
    rotationThread.solveSteps = solveSteps
    rotationThread.start()
        
    #旋轉結束
    rotationThread.join()
    print('全部旋轉完畢!請按Esc鍵結束程式')    
    #keyboard_listener.join()
    #print('程式結束')
     #print('全部旋轉完畢!請按Esc鍵結束程式') 

if __name__ == '__main__':
    startRotation('U3 D3 L3 R3 F3 B3 (9f)')#t測試用                                 
