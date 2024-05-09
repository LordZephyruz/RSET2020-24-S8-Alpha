from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import math

app = Flask(__name__)

# model
model = YOLO(r"C:\Users\Asus\Downloads\best1.pt")

# object classes
classNames = [
    "aquila", "bootes", "canis_major", "canis_minor", "cassiopeia", "cygnus", "gemini", "leo",
    "lyra", "moon", "orion", "pleiades", "sagittarius", "scorpius", "taurus", "ursa_major"
]

def detect_objects():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    while True:
        success, img = cap.read()
        results = model(img, stream=True)

        # dictionary to store highest confidence detection for each class
        max_confidence = {cls: -1 for cls in range(len(classNames))}
        best_box = {cls: None for cls in range(len(classNames))}

        # process detections
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                # class name
                cls = int(box.cls[0])

                # update max confidence if higher confidence detection found
                if box.conf[0] > max_confidence[cls]:
                    max_confidence[cls] = box.conf[0]
                    best_box[cls] = (x1, y1, x2, y2)

        # draw the best boxes with confidence above 70
        for cls, box in best_box.items():
            if box is not None and max_confidence[cls] > 0.7:  # Only draw if confidence is above 70
                x1, y1, x2, y2 = box
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                # confidence
                confidence = math.ceil((max_confidence[cls]*100))/100
                print("Confidence --->", confidence)
                # class name
                print("Class name -->", classNames[cls])
                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(detect_objects(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
