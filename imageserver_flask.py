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
		if(not os.path.exists(os.getcwd() + '\\results')):
			os.makedirs(os.getcwd() + '\\results')
		name = name.replace(' ','_')
		path = f'./results/{name}'
		image.save(path)
		isVideo = name.endswith('.mp4') or name.endswith('.mkv') or name.endswith('.avi')
		nl = '\n'
		html = f"<h1 style='font-family:Courier'>Your Uploaded Video ({name})</h1>{nl}<br>{nl}" if isVideo else f"<h1 style='font-family:Courier'>Your Uploaded Image ({name})</h1>{nl}<br>{nl}" 
		html = html + (f"<a href={path}><video controls autoplay width='50%' title={name}/><source src={path}></video></a>" if isVideo else f"<a href={path}><img width='50%' src={path} title={name}/></a>")
		html = html + f"<h1 style='font-family:Courier'><a href='/'>Return to Homepage</a></h1>{nl}"
		return html
	else:
		return redirect(url_for('home'))

@app.route("/clear")
def clear():
	try:
		for file in os.listdir('./results'):
			os.remove(os.path.join('./results',file))
		nl = '\n'
		return f'<script>{nl}alert("Cleared Results");{nl}window.location.href="/";{nl}</script>'
	except FileNotFoundError:
		return 'No Results'
		
@app.route("/results/<name>")
def results(name):
	path = f'./results/{name}' 
	return send_file(path,mimetype='image/gif')

@app.route("/collage")
def collage():
	images = os.listdir('./results')
	if not images:
		nl = '\n'
		return f'<script>{nl}alert("No Results.");{nl}window.location.href="/";{nl}</script>'
	html = "<h1 style='font-family:Courier'>Collage of Results:</h1>\n<br>"
	for image in os.listdir('./results'):
		path = os.path.join('./results',image)
		isVideo = path.endswith('.mp4') or path.endswith('.mkv') or path.endswith('.avi')
		nl = '\n'
		html = html +  (f"<a href={path}><video controls autoplay width='10%' title={path}/><source src={path}></video></a>" if isVideo else f"<a href={path}><img width='50%' src={path} title={path}/></a>")
	html = html + "<h1 style='font-family:Courier'><a href='/'>Return to Homepage</a></h1>\n"
	return html


# Debug if the same file as run
if __name__ == "__main__":
	clear()
	app.run(debug=True,host='0.0.0.0',port=8080)
