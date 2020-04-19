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

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    path = request.form['vid_stream']
    #path = request.form['FILE SHARING']
    return path
    
if __name__ == '__main__':
    app.run(host='192.168.43.81')
