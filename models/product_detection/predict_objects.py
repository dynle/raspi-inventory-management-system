from ultralytics import YOLO
import math
import sys

# Load a model
# model = YOLO("./runs/exp3/weights/best.pt")  # load the trained model
# model = YOLO("./weights/yolov8n.pt")  # load an official model
model = YOLO("weights/train5/weights/best.pt")  # load the trained model

# Test image
test_image = sys.argv[1]

# Predict with the model
# results = model("dataset-new/test/images/LINE_ALBUM_Test-201_240515_61_jpg.rf.cadb43bfb8c68245c54d00b8616724cf.jpg")  # predict on an image
# results = model("dataset-faces/test.jpg")  # predict on an image
results = model(test_image)  # predict on an image

# for result in results:
#     print(result["name"], result["confidence"], result["box"])
names = model.names

for r in results:
    boxes = r.boxes

    for box in boxes:
        # bounding box
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values
        print(f"Bounding box: {x1, y1, x2, y2}")

        # class name
        print(f"Detected: {names[int(box.cls)]}")

        # confidence
        print(f"Confidence: {math.ceil((box.conf[0]*100))/100}")