import face_recognition
import numpy as np
import sys

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("../../dataset/faces/obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("../../dataset/faces/biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

a_baimbetova = face_recognition.load_image_file("../../dataset/faces/a-baimbetova.jpeg")
a_baimbetova_encoding = face_recognition.face_encodings(a_baimbetova)[0]

d_lee = face_recognition.load_image_file("../../dataset/faces/d-lee.jpg")
d_lee_encoding = face_recognition.face_encodings(d_lee)[0]

h_yoshizaki = face_recognition.load_image_file("../../dataset/faces/h-yoshizaki.jpg")
h_yoshizaki_encoding = face_recognition.face_encodings(h_yoshizaki)[0]

y_maruyama = face_recognition.load_image_file("../../dataset/faces/y-maruyama.png")
y_maruyama_encoding = face_recognition.face_encodings(y_maruyama)[0]

# # Test image
test_image = sys.argv[1]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    a_baimbetova_encoding,
    d_lee_encoding,
    h_yoshizaki_encoding,
    y_maruyama_encoding
]
known_face_names = [
    "Barack_Obama",
    "Joe_Biden",
    "Aidana_Baimbetova",
    "Doyoon_Lee",
    "Hibiki_Yoshizaki",
    "Yui_Maruyama"
]

# Initialize some variables
face_locations = []
face_encodings = []

# Test (Put the received image data by raspberry pi here)
unknown_image = face_recognition.load_image_file(test_image)
unknown_encodings = face_recognition.face_encodings(unknown_image)

name = "unknown"
for face_encoding in unknown_encodings:
    # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    # If a match was found in known_face_encodings, just use the first one.
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    # Or instead, use the known face with the smallest distance to the new face
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]


print("Detected: ", name)