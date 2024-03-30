from flask import Flask,request,render_template,app
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

@app.route("/admin.html")
def start_admin():
    return render_template("admin.html")

@app.route("/activities.html")
def start_activities():
    return render_template("activities.html")

@app.route("/about.html") 
def start_about():
    return render_template("about.html")

@app.route("/nodes.html") 
def start_nodes():
    return render_template("nodes.html")


"""
#Sample for later
@app.route("/", methods=['GET', 'POST']) 
def mood_io():
     print("hi")
     if request.method == 'POST': 
        render_template("nodes.html")
        return inc(request.form['input']) 
     else: 
        render_template("nodes.html")
        return "<p>Hello, World!</p>"
"""



