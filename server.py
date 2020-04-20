from flask import Flask, render_template, Response, request
import cv2

pass_dict = {"Rushad": "rushad", "shirin": "10011970", "Behzad": "behzad"}

camera = cv2.VideoCapture(0)
app = Flask(__name__)

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
def home():
    """Login page."""
    return render_template('home.html')

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
    username = request.form['username']
    password = request.form['password']
    if str(pass_dict[str(username)]) == str(password):
        return render_template('front.html')
    
#@app.route('/home')
#def home():
#    """Home page."""
#    return render_template('front.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/live_stream',methods=['POST'])
def live_stream():
    path = request.form['vid_stream']
    if path == "OPEN LIVE STREAM":
        return render_template('stream_page.html')

@app.route('/file_sharing', methods=['POST'])
def file_sharing():
    path = request.form['file_sharing']
    if path == "OPEN DOCUMENT NETWORK":
        return "You have entred the Knowledge centre !"


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
