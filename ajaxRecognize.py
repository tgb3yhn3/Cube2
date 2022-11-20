from flask import *
from rubikscolorresolver.solver import resolve_colors as color
from rubikscubetracker import RubiksVideo as rbvideo
from rubikscubetracker import RubiksImage as rbimg
from tracker import RubiksImage
import cv2
import io,base64,os
import threading
from PIL import Image
import numpy as np
import cubeGUI
count=0
rubik=RubiksImage()
data={}
ansstr=''
app = Flask(__name__)
def append_dict(source:dict={},beappend:dict={})->dict:
    res = {**source, **beappend} 
    return res 
@app.route("/")
def home():
    global rubik,count
    count=0
    rubik=RubiksImage()
    return render_template("CubeUploadImageWebPage.html")
@app.route("/data",methods=['POST'])
def get_data_one():
    global data
    global count
    global rubik
    if request.method == 'POST':
        analyze_method=1
        if analyze_method==1:
            rowimg=request.files['img'].read()
            img=base64.b64encode(rowimg).decode()
            # print(img)
            img=base64.b64decode(img)
            nparr=np.frombuffer(img,np.uint8)
            img=cv2.imdecode(nparr,cv2.IMREAD_ANYCOLOR)
            rubik.image=img
            rubik.reset()
            try:
                rubik.analyze(webcam=False,cube_size=3)
                data=append_dict(data,rubik.data)
                count += 1
                
            except:
                return "error"
            # img = cv2.resize(img, (540, 540)) 
            # cv2.imshow('test',img)
            # cv2.waitKey(0) 
            if(count==6):
                rubik=RubiksImage()
                count=0
                arg=["",'--filename', 'webcam.json']
                with open("webcam.json", "w") as fh:
                    json.dump(data, fh, sort_keys=True, indent=4)
                ans=color(arg)
                print(ans+"AAAAAAAAAAAA")
                data={}
                cubeGUI.web_to_raspberry(ans)
                return "end-"+ans
        else:
            img=request.files.get('img')
            name=request.form.get('name')
            print(name)
            Basepath=os.path.abspath(os.path.dirname(__file__))
            path=Basepath+'/static/source/'
            img_path=path+img.filename
            img.save(img_path)
            count += 1
            if(count==6):
                count=0
                data={}
                files = os.listdir(Basepath)
                files.sort(key=lambda x: int(x.split('.')[0]))
                for path in files:
                    full_path = os.path.join(Basepath, path)
                    # print(full_path)
                    rubik.analyze_file(full_path,3)
                    data=append_dict(data,rubik.data)
                arg=["",'--filename', 'webcam.json']
                
                with open("webcam.json", "w") as fh:
                    json.dump(data, fh, sort_keys=True, indent=4)
                ans=color(arg)
                print(ans)
                rubik=RubiksImage()
        # cv2.imshow('test',img)
        # print("AA")
        
        return 'success'
def start_web():
    app.debug=False
    rubik=RubiksImage()
    # rubik.debug=True
    app.run('172.20.10.3')
    #app.run('192.168.1.120')
if __name__=='__main__':
    #app.debug=False
    #rubik=RubiksImage()
    # rubik.debug=True
    #app.run('192.168.1.120')
    t2 = threading.Thread(target = start_web)
    t2.start()
    cubeGUI.window.mainloop()
    
    
