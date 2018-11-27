import module_manager
module_manager.review()

import numpy as np
import cv2 as cv
from tkinter import *
from image_util import *
from tkinter import Tk, font
from tkinter.filedialog import askopenfilename
import PIL
from bs4 import BeautifulSoup
from PIL import Image
from PIL import ImageTk
import requests

panelA = None



def run(width, height): #taken from course notes
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) 
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop() 
    print("bye!")

def init(data):
    data.programStatus = "Home Screen"
    data.i=-1
    data.t=0
    data.filename= None
    data.goldenratio = 1.618
    data.advice = {}
    

def drawHomeScreen(canvas, data):
    #sets up graphics of Home Screen
    f = font.families()[179] #18 is nice, 31is cool,92,137/42/179
    f = f.replace(" ","")
    margin = 25
    canvas.create_rectangle(0,0,data.width,data.height,fill="light pink")
    canvas.create_text(data.width/2,data.height/4-100,text="Mathmatical Beauty",\
        font="%s 65"%str(f), fill="white")

    canvas.create_rectangle(margin,data.height/5+margin,data.width/2-margin/2,3*data.height/5-margin/2,fill="white",outline="white")
    canvas.create_text(data.width/4,data.height/3,text="Calculate Face Ratios",\
        font="%s 25"%str(font.families()[18].replace(" ","")), fill="light pink")

    canvas.create_rectangle(margin,3*data.height/5+margin/2,data.width/2-margin/2,data.height-margin,fill="white",outline="white")
    canvas.create_text(data.width/5,3*data.height/5,text="Hi More",\
        font="%s 25"%str(font.families()[18].replace(" ","")), fill="light pink")

    canvas.create_rectangle(data.width/2+margin/2,data.height/5+margin,data.width-margin,3*data.height/5-margin/2,fill="white",outline="white")
    canvas.create_text(data.width/5,3*data.height/5+3*margin,text="Learn More",\
        font="%s 25"%str(font.families()[18].replace(" ","")), fill="light pink")

    canvas.create_rectangle(data.width/2+margin/2,3*data.height/5+margin/2,data.width-margin,data.height-margin,fill="white",outline="white")
    canvas.create_text(data.width/3+200,3*data.height/4,text="Your Celeb Look-Alike",\
        font="%s 25"%str(font.families()[18].replace(" ","")), fill="light pink")
    #canvas.create_text(data.width/2,data.height/4+300,text="Mathmatical Beauty",\
        #font="%s 100"%str(font.families()[142].replace(" ","")), fill="black")

def drawMainScreen(canvas,data):
    #sets up graphics of Home Screen
    f = font.families()[179] #18 is nice, 31is cool,92,137/42/179
    f = f.replace(" ","")
    canvas.create_rectangle(0,0,data.width,data.height,fill="light blue")
    canvas.create_text(data.width/2,data.height/4-100,text="Mathmatical Beauty",\
        font="%s 65"%str(f), fill="white")
    canvas.create_rectangle(10,data.height/5,data.width/3,data.height/2,fill="white",outline="white")
    canvas.create_text(data.width/3-140,data.height/2-140,text="Choose Another",\
        font="%s 25"%str(font.families()[18].replace(" ","")), fill="light blue")
    canvas.create_text(data.width/3-140,data.height/2-120,text="Image",\
        font="%s 25"%str(font.families()[18].replace(" ","")), fill="light blue")
    canvas.create_rectangle(50+data.width/3,data.height/5,data.width/3*2+60,data.height/2,fill="white",outline="white")
    canvas.create_text(data.width/3+200,data.height/2-140,text="Get Report",\
        font="%s 25"%str(font.families()[18].replace(" ","")), fill="light blue")

def drawReportScreen(canvas,data):
    f = font.families()[179] #18 is nice, 31is cool,92,137/42/179
    f = f.replace(" ","")
    canvas.create_rectangle(0,0,data.width,data.height,fill="thistle")
    canvas.create_text(data.width/2,data.height/4-100,text="Mathmatical Beauty",\
        font="%s 65"%str(f), fill="white")
    symStr = "The symmertry is "+ str(round(data.symmertry,2))
    canvas.create_text(data.width/2,data.height/4+75,text=symStr,\
        font="%s 20"%str(f), fill="white")
    i = 0
    goldenratio = 1.618
    goldenAvg = []
    for key in data.ReportRatios:
        goldenAvg.append(data.ReportRatios[key]/goldenratio)
        i+=70
        ratioStr = "The "+key+" ratio is "+ str(round(data.ReportRatios[key],2))
        canvas.create_text(data.width/2,data.height/4+100+i,text=ratioStr,\
        font="%s 20"%str(f), fill="white")
    avgGoldenNum= sum(goldenAvg)/len(goldenAvg)
    fibNum = "The fibbonacci grade is "+ str(round(100*avgGoldenNum))
    canvas.create_text(data.width/2,data.height/4,text=fibNum,\
        font="%s 20"%str(f), fill="white")
    canvas.create_rectangle(0,data.height-120,120,data.height,fill="plum1")
    canvas.create_text(60,data.height-60,text="Back",\
        font="%s 20"%str(f), fill="white")
    Label(root, image=data.hi).pack(side=tk.LEFT,fill=tk.Y)
def reportScreen2(canvas,data):
    pass


def timerFired(data):
    pass

def mousePressed(event, data):
    if event.x>=10 and event.x<=data.width/3 and event.y>=data.height/5 and event.y<=data.height/2:
        data.programStatus= "calculateFaceRatios"
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        data.filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        calculateFaceRatios(data,data.filename)
        calculateFaceSymmetry(data,data.filename)
    if data.programStatus== "calculateFaceRatios" and event.x >= 50+data.width/3 \
        and event.x <= data.width/3*2+60 and \
        event.y >= data.height/5 and event.y <=data.height/2:
        data.programStatus= "reportScreen"
    if event.x>= 0 and event.y >= data.height-120 and event.x <= 120\
        and event.y <= data.height and data.programStatus== "reportScreen":
        data.programStatus= "calculateFaceRatios"
   

def keyPressed(event,data):
    if event.keysym == "X":
        cv.destroyWindow('res')
    if event.keysym == "N":
        data.programStatus = "reportScreen2"

def redrawAll(canvas, data):
    if data.programStatus == "Home Screen":
        drawHomeScreen(canvas,data)
    elif data.programStatus == "calculateFaceRatios":
        drawMainScreen(canvas,data)
    elif data.programStatus == "reportScreen":
        drawReportScreen(canvas,data)
    elif data.programStatus == "reportScreen2":
        drawReportScreen2(canvas,data)

def calculateFaceRatios(data,picture):
    #Most of Lines 140-156 are unoriginal: 
    #https://docs.opencv.org/3.4.3/d7/d8b/tutorial_py_face_detection.html

    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')
    nose_cascade = cv.CascadeClassifier('haarcascade_mcs_nose.xml')
    mouth_cascade = cv.CascadeClassifier('haarcascade_mcs_mouth.xml')
    img = cv.imread(picture) #ex angelina-jolie.jpg
    res = cv.resize(img,None,fx=.25, fy=.25, interpolation = cv.INTER_CUBIC)
    gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
    goldenratio = 1.618
    ratios = {}

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x,y,w,h) in faces:
        cv.rectangle(res,(x+(w//8),y),(x+w-(w//8),y+h),(255,0,0),2)
        cv.rectangle(res,(x+(w//8),y),(x+w-(w//8),y+h//2),(255,0,0),2)
        cv.rectangle(res,(x+(w//2),y),(x+w-(w//8),y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = res[y:y+h, x:x+w]

        width = (x+(w//8))- (x+w-(w//8))
        leftFace = (x+(w//8))
        rightFace = (x+w-(w//8))

        print(leftFace,rightFace)
        HW = -(h+14)/width
        ratios["Head's Length to Width"]=HW
        chin = h
        pupil = 0
        eyes = eye_cascade.detectMultiScale(roi_gray,1.3)
        for (ex,ey,ew,eh) in eyes:
            cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2) 
            cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh-eh//4),(0,255,0),2)
            cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh//2),(255,255,0),2)
            pupil= ey+eh//2
            if ex<-width/2:
                H1=(-width)/(ex+ew)
                ratios["Side of face to inside eye"]=H1
        if len(eyes)>1:
            if eyes[0][0]>eyes[1][0]:
                H2 = (eyes[0][0])/((eyes[1][0]+eyes[1][2]))
            else:
                H2 = (eyes[1][0])/((eyes[0][0]+eyes[0][2]))
            ratios["Inside of eyes to face width"]= H2

        
        noses = nose_cascade.detectMultiScale(roi_gray,1.3)
        for (nx,ny,nw,nh) in noses:
            cv.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh*3//4),(100,100,100),2)
            bottomNose= ny+nh*3//4
            V2=(h-pupil)/(bottomNose-pupil)
            V3= (bottomNose-pupil)/(ny-pupil)
            rNose = nx+nw
            ratios["Pupils to nostril to chin"]=V2
            ratios["Pupils to nose flare to nose bottom"]=V3
        mouths = mouth_cascade.detectMultiScale(roi_gray,1.1)
        for (mx,my,mw,mh) in mouths:
            if my > bottomNose:
                cv.rectangle(roi_color,(mx,my),(mx+mw,my+3*mh//4),(0,0,0),2)
                cv.rectangle(roi_color,(mx,my),(mx+mw,my+(mw//6)),(0,0,0),2)
                midLips=my+(mw//6)
                V1= (h-pupil)/(midLips-pupil)
                ratios["V1"]=V1
                H6=(mw/2)/(rNose-mx-mw/2)
                ratios["H6"]=H6



    # cv.putText(res,"Press X to Exit",(20,400),0,.5,(0,0,0))
    print(ratios)
    data.ReportRatios = ratios
    for key in ratios:
        data.advice[key]= None
    # print("More ratios to come!")
    # cv.imshow('res',res)
    #b,g,r = cv.split(res)
    #res = cv.merge((r,g,b))
    data.hi = select_image(res)


    #cv.waitKey(0)
    #cv.destroyAllWindows()

def select_image(image):
    # grab a reference to the image panels
    global panelA

    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
 
    # convert the images to PIL format...
    image = Image.fromarray(image)
    # ...and then to ImageTk format
    image = ImageTk.PhotoImage(image)
    # if the panels are None, initialize them
    if panelA is None:
        # the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)
 
        # otherwise, update the image panels
    else:
            # update the pannels
            panelA.configure(image=image)
            panelA.image = image
    return panelA


def calculateFaceSymmetry(data,picture):

    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')
    nose_cascade = cv.CascadeClassifier('haarcascade_mcs_nose.xml')
    mouth_cascade = cv.CascadeClassifier('haarcascade_mcs_mouth.xml')
    img = cv.imread(picture) #ex angelina-jolie.jpg
    res = cv.resize(img,None,fx=.25, fy=.25, interpolation = cv.INTER_CUBIC)
    gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
    symRatios = []
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    roi_gray = gray[faces[0][1]:faces[0][1]+faces[0][3], \
        faces[0][0]:faces[0][0]+faces[0][2]]
    roi_color = res[faces[0][1]:faces[0][1]+faces[0][3], \
        faces[0][0]:faces[0][0]+faces[0][2]]
    w = faces[0][2]
    eyes = eye_cascade.detectMultiScale(roi_gray,1.3)
    if len(eyes)>1:
        if eyes[0][0]>eyes[1][0]:
            a = 0
            b = 1
        else:
            a = 1
            b = 0
        print(eyes[0][0],eyes[1][0],w//2,"whar")
        eyeSymX = -(eyes[a][0]-w//2)/(eyes[b][0]+eyes[b][2]-w//2)
        symRatios.append(eyeSymX)
        eyeSymW = (eyes[0][2])/(eyes[1][2])
        symRatios.append(eyeSymW)
        eyeSymY = (eyes[0][1])/(eyes[1][1])
        symRatios.append(eyeSymY)
        eyeSymH = (eyes[0][3])/(eyes[1][3])
        symRatios.append(eyeSymH) 
    noses = nose_cascade.detectMultiScale(roi_gray,1.3)
    bottomNose = noses[0][1]+noses[0][3]*3//4
    noseSym = -(noses[0][0]-w//2)/((noses[0][0]+noses[0][2])-w//2)
    symRatios.append(noseSym)
    mouths = mouth_cascade.detectMultiScale(roi_gray,1.1)
    for (mx,my,mw,mh) in mouths:
        if my > bottomNose:
            mouthSym =  -(mouths[0][0]-w//2)/((mouths[0][0]+mouths[0][2])-w//2)
            symRatios.append(mouthSym)
            print(mouthSym)
    print(symRatios)
    data.symmertry = (sum(symRatios)/len(symRatios))*100

def determineAdvice():
    errorPercent = 15 #percent
    errorBound = data.goldenratio*(errorPercent/100)
    ratios = data.ReportRatios
    if math.abs(ratios["Head's Length to Width"]-data.goldenratio) > errorBound:
        if ratios["Head's Length to Width"]-data.goldenratio > 0:
            data.advice["Head's Length to Width"] = "Long Face"
        else:
            data.advice["Head's Length to Width"] = "Short Face"
    # if math.abs(ratios["Side of face to inside eye"]-data.goldenratio) > errorBound:
    #     if ratios["Side of face to inside eye"]-data.goldenratio > 0:
    #         data.advice["Side of face to inside eye"] = 
    #     else:
    if math.abs(ratios['Inside of eyes to face width']-data.goldenratio) > errorBound:
        if ratios['Inside of eyes to face width']-data.goldenratio > 0:
            data.advice['Inside of eyes to face width'] = "Eyes far apart"
        else:
            data.advice['Inside of eyes to face width'] = "Eyes close together"
    else:
        data.advice['Inside of eyes to face width'] = "Eye seperation good"
    if math.abs(ratios['Pupils to nostril to chin']-data.goldenratio) > errorBound:
        if ratios['Pupils to nostril to chin']-data.goldenratio > 0:
            data.advice['Pupils to nostril to chin'] = "Long Nose"
        else:
            data.advice['Pupils to nostril to chin'] = "Short Nose"
    else:
        data.advice['Pupils to nostril to chin'] = "Good length of nose"
    if math.abs(ratios['Pupils to nose flare to nose bottom']-data.goldenratio) > errorBound:
        if ratios['Pupils to nose flare to nose bottom']-data.goldenratio > 0:
            data.advice['Pupils to nose flare to nose bottom'] = "Wide Nose"
        else:
            data.advice['Pupils to nose flare to nose bottom'] = "Narrow Nose"
    else:
        data.advice['Pupils to nose flare to nose bottom'] = "Good width of nose"
    if math.abs(ratios["V1"]-data.goldenratio) > errorBound:
        if ratios["V1"]-data.goldenratio > 0:
            data.advice["V1"]= "Narrow Chin"
        else:
            data.advice["V1"]= "Wide Chin"
    else:
        data.advice["V1"]= "Good Chin"
    if math.abs(ratios["H6"]-data.goldenratio) > errorBound:
        if ratios["H6"]-data.goldenratio > 0:
            data.advice["H6"] = "Wide Mouth"
        else:
            data.advice["H6"] = "Narrow Mouth"
    else:
        data.advice["H6"] = "Good Mouth"
    

run(900,800)
