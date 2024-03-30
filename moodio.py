from flask import Flask,request 
app = Flask(__name__) 
@app.route('/', methods=['GET', 'POST']) 
def mood_io():
     if request.method == 'POST': 
        return inc(request.form['input']) 
     else: return -1 


def inc(x): 
    x += 1 
    return x 


app.run(port=5000)