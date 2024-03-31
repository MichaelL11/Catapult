from flask import Flask,request,render_template,app
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from deepEmotion import Deep_Emotion_3Classes
#export FLASK_APP=moodio.py
#flask run --port 5001

def cropFace(img):
    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        out=gray[y:y+h, x:x+w]
        break
    cv2.imshow('crop',out)
    cv2.waitKey(0)
    return out


# 0=Happy, 1=Neutral, 2=Sad
def getPredict(model,img):
    #emotionDict={0:'Happy', 1:'Neutral', 2:'Sad'}
    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((48, 48)),
        transforms.ToTensor(),
    ])
    img = Image.fromarray(img)
    inputTensor = transform(img).unsqueeze(0)  # Add a batch dimension
    outputs = model(inputTensor)
    _, pred = torch.max(outputs,1)
    predIdx=pred.item()
    return predIdx



#Server Stuff (model stuff ends)
app = Flask(__name__) 

@app.route("/") 
def start():
    return render_template("homepage.html")

@app.route("/login.html")
def start_login():
    return render_template("login.html")

@app.route("/resources.html")
def start_Resources():
    return render_template("Resources.html")

@app.route("/admin.html", methods=['GET', 'POST'])
def start_admin():
    if request.method == 'POST':
        imgPath="quickSave.jpg"
        
        model=Deep_Emotion_3Classes()
        model.load_state_dict(torch.load('model_weights_3class.pth', map_location=torch.device('cpu')))
        model.eval()
        
        img=cv2.imread(imgPath)
        cropped=cropFace(img)
        out=getPredict(model,cropped)
        print(out)



        return 1
    else:
        return render_template("admin.html")

@app.route("/activities.html")
def start_activities():
    return render_template("activities.html")

@app.route("/about.html") 
def start_about():
    return render_template("about.html")


@app.route("/mediadevices.html") 
def start_media():
    return render_template("mediadevices.html")

@app.route("/webcamanalysis.html") 
def start_webcamanalysis():
    return render_template("webcamanalysis.html")





