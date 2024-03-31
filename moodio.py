from flask import Flask,request,render_template,app,send_from_directory,jsonify
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from deepEmotion import Deep_Emotion_3Classes
import json,base64,io

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
app = app = Flask(__name__, static_url_path='/static', static_folder='static')

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
        data = request.json
        # Decode base64-encoded image data
        image_bytes = base64.b64decode(data["image"])
    

        # Create PIL Image object from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        image.save("quickSave.jpg")
        imgPath="quickSave.jpg"
        
        model=Deep_Emotion_3Classes()
        model.load_state_dict(torch.load('model_weights_3class.pth', map_location=torch.device('cpu')))
        model.eval()

        img=cv2.imread(imgPath)
        cropped=cropFace(img)
        output=getPredict(model,cropped)
        outDict={0:1,1:0,2:-1}
        print(output)
        return jsonify({'message': 'Image Upload was Success', 'mood_value': output})
    else:
        return render_template("admin.html")

@app.route("/activities.html")
def start_activities():
    return render_template("activities.html")


@app.route("/webcam.js")
def webcam_js_handler():
    return send_from_directory('static', 'webcam.js')

@app.route("/about.html") 
def start_about():
    return render_template("about.html")


@app.route("/mediadevices.html") 
def start_media():
    return render_template("mediadevices.html")

@app.route("/webcamanalysis.html") 
def start_webcamanalysis():
    return render_template("webcamanalysis.html")





