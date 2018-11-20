import numpy as np
import cv2 as cv
from tkinter import *
from image_util import *
from tkinter import Tk, font
from tkinter.filedialog import askopenfilename

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
    

def drawHomeScreen(canvas, data):
    #sets up graphics of Home Screen
    f = font.families()[179] #18 is nice, 31is cool,92,137/42/179
    f = f.replace(" ","")
    canvas.create_rectangle(0,0,data.width,data.height,fill="light pink")
    canvas.create_text(data.width/2,data.height/4-100,text="Mathmatical Beauty",\
        font="%s 65"%str(f), fill="white")
    canvas.create_rectangle(10,data.height/5,data.width/3,data.height/2,fill="white",outline="white")
    canvas.create_text(data.width/3-140,data.height/2-140,text="Calculate Face Ratios",\
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
    i = 0
    goldenratio = 1.618
    goldenAvg = []
    for key in data.ReportRatios:
        goldenAvg.append(data.ReportRatios[key]/goldenratio)
        i+=70
        ratioStr = "The "+key+" ratio is "+ str(round(data.ReportRatios[key],2))
        canvas.create_text(data.width/2,data.height/4+100+i,text=ratioStr,\
        font="%s 25"%str(f), fill="white")
    avgGoldenNum= sum(goldenAvg)/len(goldenAvg)
    fibNum = "The fibbonacci grade is "+ str(round(100*avgGoldenNum))
    canvas.create_text(data.width/2,data.height/4,text=fibNum,\
        font="%s 25"%str(f), fill="white")
    canvas.create_rectangle(0,data.height-120,120,data.height,fill="plum1")
    canvas.create_text(60,data.height-60,text="Back",\
        font="%s 25"%str(f), fill="white")


def timerFired(data):
    pass

def mousePressed(event, data):
    if event.x>=10 and event.x<=data.width/3 and event.y>=data.height/5 and event.y<=data.height/2:
        data.programStatus= "calculateFaceRatios"
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        data.filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        calculateFaceRatios(data,data.filename)
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

def redrawAll(canvas, data):
    if data.programStatus == "Home Screen":
        drawHomeScreen(canvas,data)
    elif data.programStatus == "calculateFaceRatios":
        drawMainScreen(canvas,data)
    elif data.programStatus == "reportScreen":
        drawReportScreen(canvas,data)

def calculateFaceRatios(data,picture):

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
        HW = -(h+14)/width
        ratios["Head's Length to Width"]=HW
        chin = y+h
        pupil = 0
        eyes = eye_cascade.detectMultiScale(roi_gray,1.3)
        for (ex,ey,ew,eh) in eyes:
            cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2) 
            cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh-eh//4),(0,255,0),2)
            cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh//2),(255,255,0),2)
            pupil= ey+eh//2
            if ex<-width/2:
                H1=1+(-width)/(x+w-(w//8)-ex-ew)
                ratios["Side of face to inside eye"]=H1
        print(eyes)
        if len(eyes)>1:
            if eyes[0][0]>eyes[1][0]:
                H2 = 1+(eyes[0][0]-(x+(w//8)))/((eyes[1][0]+eyes[1][2])-(x+(w//8)))
            else:
                H2 = 1+(eyes[1][0]-(x+(w//8)))/((eyes[0][0]+eyes[0][2])-(x+(w//8)))
            ratios["Inside of eyes to face width"]= H2

        mouths = mouth_cascade.detectMultiScale(roi_gray,1.3)
        for (mx,my,mw,mh) in mouths:
            if my > 165 and my>300:
                cv.rectangle(roi_color,(mx,my),(mx+mw,my+3*mh//4),(500,500,0),2)
                cv.rectangle(roi_color,(mx,my),(mx+mw,my+(mw//6)),(500,500,0),2)

        noses = nose_cascade.detectMultiScale(roi_gray,1.3)
        for (nx,ny,nw,nh) in noses:
            cv.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh*3//4),(100,100,100),2)
            bottomNose= ny+nh*3//4
            V2=(chin-pupil)/(chin-bottomNose)
            V3= (ny+nh*3//4-(eyes[0][1]+eyes[0][3]//2))/(ny-(eyes[0][1]+eyes[0][3]//2))
            ratios["Pupils to nostril to chin"]=V2
            ratios["Pupils to nose flare to nose bottom"]=V3
    i = 0
    for key in ratios:
        i+=50
        ratioStr = "The "+key+" ratio is "+ str(round(ratios[key],2))
        cv.putText(res,ratioStr,(20,400+i),0,.5,(0,0,0))
    print(ratios)
    data.ReportRatios = ratios
    print("More ratios to come!")
    cv.imshow('res',res)
    cv.waitKey(0)
    cv.destroyAllWindows()

run(900,900)
