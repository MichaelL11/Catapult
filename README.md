# Catapult Project - Emojication

## description of Project
The goal of this project was to adjust difficulty of learning based off of facial expressions. Our program looks at the facial expressions of the client, sends that image to the server every second, and our model looks at that image to find out whether the face looks happy, sad, or nuetral. Then, our server sends that back to the client. This is the end to where we got in our implementation, but the goal would be to change the difficulty of the problems for the students based on their mood over time. 

We believe our project is scalable and modular, and has great potential.



![IMG_F0851A9218B8-1](https://github.com/MichaelL11/Catapult/assets/143101596/8376866f-e3eb-4f92-8dfc-bbfa219b1bb7)



Dependencies
Flask==3.0.2
opencv_python==4.9.0.80
Pillow==10.2.0
torch==2.2.2
torchvision==0.17.2
Python==3.11.5



## Run Instructions for proof of concept

Open Terminal in Catapult directory and run the following commands

1. export FLASK_APP=moodio.py
2. flask run --port 5001
3. Finally, connect to host with client.
























Source: https://www.geeksforgeeks.org/how-to-send-a-json-object-to-a-server-using-javascript/
