from flask import Flask, render_template, Response, request
import cv2

camera = cv2.VideoCapture(0)
app = Flask(__name__)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def home():
    """Home page."""
    return render_template('front.html')

@app.route('/stream_page')
def stream_page():
    return render_template('stream_page.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/live_stream', methods=['POST'])
def live_stream():
    path = request.form['vid_stream']
    if path == "OPEN LIVE STREAM":
        return stream_page()

@app.route('/file_sharing', methods=['POST'])
def file_sharing():
    path = request.form['file_sharing']
    if path == "OPEN DOCUMENT NETWORK":
        return "You have entred the Knowledge centre !"

if __name__ == '__main__':
    app.run(host='192.168.43.81')
