# HTTP Web Server Using the Bottle Implementation #
# Author: Timothy Do
# Last Revision: 7/16/22

# Libraries
from bottle import *
from time import *

# Server Variables
serverIP = '0.0.0.0'
serverPort = 80 

server = Bottle()

# Simple Get Responses
@server.route('/<file>')
def index(file):
    if not file:
        file = "index.html"
    g = open('./' + file)
    content = g.read()
    if(file == 'imageserver.py'): # No Reading Source Code
        content = "Permission Denied."
    return content

# Handle POST stuff
@route('/upload', method=['GET','POST'])
def do_upload():
    category = request.forms.get('category')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return "File extension not allowed."

    save_path = "/tmp/{category}".format(category=category)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path)
    return "File successfully saved to '{0}'.".format(save_path)

# Simple 404 Error Handling
@server.error(404)
def error404(error):
    fourofour = open('./404.html')
    content = fourofour.read()
    return content

# Simple 500 Error Handling
@server.error(500)
def error500(error):
    fourofour = open('./404.html')
    content = fourofour.read()
    return content

if __name__ == '__main__': #Check if file is run as main file
    # Running Actual Server
    run(server,host=serverIP, port=serverPort)