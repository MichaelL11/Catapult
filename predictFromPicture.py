import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from deepEmotion import Deep_Emotion_3Classes

model=Deep_Emotion_3Classes()
model.load_state_dict(torch.load('model_weights_3class.pth', map_location=torch.device('cpu')))
model.eval()

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

def getPredict(img):
    emotionDict={0:'Happy', 1:'Neutral', 2:'Sad'}
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
    emotion=emotionDict[predIdx]
    return emotion


if __name__ == "__main__":
    imgPath="wrong.jpg"
    img = cv2.imread(imgPath)
    try:
        cropped=cropFace(img)
        out=getPredict(cropped)
    except:
        print("Something is wrong")
        out="Neutral"
    print(out)