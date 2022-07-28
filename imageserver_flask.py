# Image Server Implemented in Python Flask

# Libraries 
from flask import Flask, redirect, url_for, render_template, request


# Creating the app 
app = Flask(__name__)

# Landing Page
@app.route("/")
def home():
	return render_template('index.html')

@app.route("/upload",methods=["POST","GET"])
def upload():
	if request.method == "POST": 
		image = request.files['upload']
		if not image:
			return render_template('noimage.html')
		path = './images/result.jpg'
		image.save(path)
		return render_template('uploaded.html')
	else:
		return render_template('index.html') 

@app.route("/result")
def result():
	path = 'images/result.jpg'
	return f'<img src={path}/>'


# Debug if the same file as run
if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0',port=80)
