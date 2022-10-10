'''
參考網站：
    1.https://codingshiksha.com/python/python-tkinter-button-with-rounded-border-and-edges-gui-desktop-app-full-project-for-beginners/
    2.https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
    3.https://www.tutorialspoint.com/python/tk_canvas.htm
    4.https://www.runoob.com/python/python-func-super.html
'''
import tkinter as tk

class RoundedCornerFrame(tk.Canvas):
    
    def __init__(self,master,width=100,height=100,cornerRadius=1,bg="white",bd=2,borderColor="black"):
        super().__init__(master=master,width=width,height=height,bd=0,highlightthickness=0,cursor="hand2")
        self.width = width
        self.height = height
        self.cornerRadius = cornerRadius
        self.bg = bg
        self.bd = bd
        self.borderColor = borderColor
        roundedCornerRectangle = self.roundPolygon([bd/3, width-bd/3, width-bd/3,bd/3], [bd/3, bd/3, height-bd/3, height-bd/3], cornerRadius , width=bd, outline=borderColor, fill=bg) 
        tt = 8
    
    def changeBackgroundColor(self,bg = "white"):
        self.delete(tk.ALL)
        roundedCornerRectangle = self.roundPolygon([self.bd/3, self.width-self.bd/3, self.width-self.bd/3,self.bd/3], [self.bd/3, self.bd/3, self.height-self.bd/3, self.height-self.bd/3], self.cornerRadius , width=self.bd, outline=self.borderColor, fill=bg)
        self.bg = bg
        
    def roundPolygon(self,x, y, sharpness, **kwargs):
        if sharpness < 2:
            sharpness = 2
    
        ratioMultiplier = sharpness - 1
        ratioDividend = sharpness
    
        # Array to store the points
        points = []
    
        # Iterate over the x points
        for i in range(len(x)):
            # Set vertex
            points.append(x[i])
            points.append(y[i])
    
            # If it's not the last point
            if i != (len(x) - 1):
                # Insert submultiples points. The more the sharpness, the more these points will be
                # closer to the vertex. 
                points.append((ratioMultiplier*x[i] + x[i + 1])/ratioDividend)
                points.append((ratioMultiplier*y[i] + y[i + 1])/ratioDividend)
                points.append((ratioMultiplier*x[i + 1] + x[i])/ratioDividend)
                points.append((ratioMultiplier*y[i + 1] + y[i])/ratioDividend)
            else:
                # Insert submultiples points.
                points.append((ratioMultiplier*x[i] + x[0])/ratioDividend)
                points.append((ratioMultiplier*y[i] + y[0])/ratioDividend)
                points.append((ratioMultiplier*x[0] + x[i])/ratioDividend)
                points.append((ratioMultiplier*y[0] + y[i])/ratioDividend)
                # Close the polygon
                points.append(x[0])
                points.append(y[0])
    
        return self.create_polygon(points, **kwargs, smooth=True)




if __name__ == '__main__':#測試用
    root = tk.Tk()
    root.geometry('500x500')
    
    FaceButtonFrame = RoundedCornerFrame(root)
    FaceButtonFrame.grid(row = 0, column = 0)        
    FaceButtonFrame.rowconfigure(0, weight = 1)
    FaceButtonFrame.columnconfigure(0, weight = 1)
    FaceButtonFrame.grid_propagate(0)#固定FaceButtonFrame的大小 
    
    root.mainloop()