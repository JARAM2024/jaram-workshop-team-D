from flask import Flask, render_template, Response, jsonify
import cv2
import trial_b  # Ensure trial_b.py is in the same directory as app.py

app = Flask(__name__)

@app.route('/')
def main_home():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/distance')
def distance():
    return jsonify(trial_b.distance_measurements)

@app.route('/led_status')
def led_status():
    return jsonify(trial_b.led_status)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('./static', path)

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    # Start the sensor in a separate thread
    trial_b.start_sensor()
    app.run(host='0.0.0.0', port=5003, debug=True, use_reloader=False)
