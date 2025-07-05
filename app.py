from flask import Flask, render_template, Response
import cv2
import Volume_Control as vc  # This file contains your hand tracking logic
import threading
import webbrowser

app = Flask(__name__)

def generate_frames():
    cap = cv2.VideoCapture(0)  # ✅ Open camera ONLY here
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = vc.process_frame(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()  # ✅ Release when done

@app.route('/')
def index():
    return render_template('index.html')  # ✅ HTML load first

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # ✅ Auto-open browser AFTER Flask starts
    threading.Timer(1.25, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(debug=True)


