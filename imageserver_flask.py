# Image Server Implemented in Python Flask

# Libraries 
from flask import Flask, redirect, url_for, render_template, request, send_file
import os


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
		name = request.form['filename']
		if not image or not name:
			return render_template('noimage.html')
		path = f'./results/{name}'
		image.save(path)
		return redirect(url_for('uploaded',resultname=name,path=path))
	else:
		return render_template('index.html')
		
@app.route("/uploaded")
def uploaded(resultname,path):
	return render_template('uploaded.html',resultname=resultname,path=path) 


@app.route("/results/<name>")
def results(name):
	path = f'./results/{name}' 
	return send_file(path,mimetype='image/gif')

# Debug if the same file as run
if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0',port=80)
