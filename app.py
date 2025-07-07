from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import Volume_Control as vc

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image'}), 400

    img_data = data['image'].split(',')[1]
    img_bytes = base64.b64decode(img_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # 🔁 Your volume control logic here
    processed_img = vc.process_frame(img)
    result = "Volume adjusted (simulated)"

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
