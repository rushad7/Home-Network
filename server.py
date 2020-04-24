from flask import Flask, render_template, Response, request, redirect, url_for
import pandas as pd
import datetime
import hashlib
import cv2
import os

camera = cv2.VideoCapture(0)
app = Flask(__name__)

def get_my_ip():
    log = open("user_logs.log", "a")
    log_data = str(datetime.datetime.now()) + "," +  str(username) + "," + str(request.remote_addr) + "\n"
    if login_status:
        log.write(log_data)
        log.close()

def gen_frames():
    while True:
        success, frame = camera.read()
        frame = cv2.flip(frame, 1)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
@app.route('/home')
def home():
    """Login page."""
    return render_template('home.html')

@app.route('/register',  methods=['POST'])
def register():
    """Registration page."""
    path = request.form['reg']
    if path == "REGISTER":
        return render_template('registration.html')

@app.route('/add_user',  methods=['POST'])
def add_user():
    """Add user to data base"""
    username = request.form['reg_username']
    password = request.form['reg_password']
    username_sha256 = hashlib.sha256(bytes(username, 'utf-8')).hexdigest()
    password_sha256 = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
    user_details = pd.read_csv('pass.enc')
    if len(username) > 4 and len(password) > 7:
        if username_sha256 not in list(user_details["username"]):
            user_details = open("pass.enc", "a")
            user_details.write(username_sha256 + "," + password_sha256 + "\n")
            user_details.close()
        else:
            return "<h1>Username already taken. Please try again with a different username</h1>"
        return render_template('reg_conf.html')
    
    else:
        return "<h1>Please maintain the minimum charactar requirenment</h1>"

@app.route('/reg_conf',  methods=['POST'])
def reg_conf():
    path = request.form['login']
    if path == "LOGIN":
        return render_template("home.html")

@app.route('/login_pswd',  methods=['POST'])
def login_pswd():
    """Login page via password."""
    path = request.form['login_pswd']
    if path == "LOGIN WITH USERNAME AND PASSWORD":
        return render_template('login_pswd.html')

@app.route('/login_facial',  methods=['POST'])
def login_facial():
    """Login page via face id."""
    path = request.form['login_facial']
    if path == "LOGIN USING FACE ID":
        return "Face ID under development"

@app.route('/dashboard',  methods=['POST'])
def dashboard():
    """Password Verification and access to dashboard"""
    global username
    global password
    global login_status
    
    username = request.form['username']
    password = request.form['password']
    
    username_sha256 = hashlib.sha256(bytes(username, 'utf-8')).hexdigest()
    password_sha256 = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
    user_details = pd.read_csv('pass.enc')
    password_extract = pd.read_csv("pass.enc", index_col ="username")
    
    if username_sha256 in list(user_details["username"]):
        if password_sha256 == password_extract["password"][username_sha256]:
            login_status = True
            get_my_ip()
            return render_template('front.html')
        else:
            return "<h1>Wrong Login credentials. Please try again</h1>"
    else:
        return "<h1>User does not exist. Please register first</h1>"

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    if login_status :
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/live_stream', methods=['POST'])
def live_stream():
    path = request.form['vid_stream']
    if path == "OPEN LIVE STREAM":
        return render_template('stream_page.html')

@app.route('/file_upload', methods=['POST'])
def file_upload():
    path = request.form['file_upload']
    if path == "UPLOAD DOCUMENT":
        return render_template('upload_file.html')

@app.route('/document_network', methods=['POST'])
def document_network():
    path = request.form['file_sharing']
    if path == "OPEN DOCUMENT NETWORK":
        return "<h1>ALL DOCUMENTS WILL BE VISIBLE HERE. UNDER DEVELOPMENT</h1>"

@app.route("/handleUpload", methods=['POST'])
def handleUpload():
    if 'files' in request.files:
        file = request.files['files']
        if file.filename != '':            
            file.save(os.path.join('C:/Users/Rushad/Desktop/Home-Network/file_storage', file.filename))
            return render_template('dash_return.html')
        else:
            return "<h1>Upload Failed<h1>"
    return render_template('upload_file.html')

@app.route('/return', methods=['POST'])
def return_home():
    path = request.form['ret_dash']
    if path == "return":
        return render_template('home.html')


@app.errorhandler(400)
def bad_request(e):
    """Bad request."""
    return render_template("400.html"), 400

@app.errorhandler(404)
def not_found(e):
    """Page not found."""
    return render_template("404.html"), 404

@app.errorhandler(405)
def server_error(e):
    """Access denied"""
    return render_template("405.html"), 405

@app.errorhandler(500)
def server_error(e):
    """Internal server error."""
    return render_template("500.html"), 500

if __name__ == '__main__':
    app.run(host='192.168.43.81')
