from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ImageUploadSerializer
from PIL import Image
from ultralytics import YOLO
import math
import face_recognition
import numpy as np
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime

class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            # Process the image
            results = self.process_image(image)

            #find image
            #buyer_face = '

            #async to display
            channel_layer = get_channel_layer()

            #match user and image path
            face_names = [
                "Barack Obama",
                "Joe Biden",
                "Aidana Baimbetova",
                "Doyoon Lee",
                "Hibiki Yoshizaki",
                "Yui Maruyama"
            ]
            face_pathes = [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/President_Barack_Obama.jpg/440px-President_Barack_Obama.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Joe_Biden_presidential_portrait.jpg/1280px-Joe_Biden_presidential_portrait.jpg",
                "https://images.microcms-assets.io/assets/1909f44556aa4db1802e23ba78dbc874/679d88d775f64fd2bd3e8aa7052f376d/a-baimbetova.jpeg?fm=webp&w=250&q=50",
                "https://images.microcms-assets.io/assets/1909f44556aa4db1802e23ba78dbc874/7a8015bba32f46d38b752a45c746a029/d-lee.jpg?fm=webp&w=250&q=50",
                "https://images.microcms-assets.io/assets/1909f44556aa4db1802e23ba78dbc874/5572d38833d24962883da3778445e9ef/IMG_4507.jpg?fm=webp&w=250&q=50",
                "https://images.microcms-assets.io/assets/1909f44556aa4db1802e23ba78dbc874/b7dbaa6f9b214ab4b9e5559c256c2282/y-maruyama.PNG?fm=webp&w=250&q=50"
            ]
            product_names = [
                "chips-sio,",
                "coffee-black",
                "coffee-latte"
            ]
            product_pathes = [
                'https://store.nissin.com/cdn/shop/files/97377_800x.png?v=1689059105',
                'https://m.media-amazon.com/images/I/514aXqXpTyL.jpg',
                'https://image1.shopserve.jp/e-fujiyakuhin.jp/pic-labo/llimg/4901085613597.jpg?t=20200407085326'

            ]
            #match names
            name_path_display = ''
            i = 0
            for face_name in face_names:
                i += 1
                if results[2].lower() in face_name.lower():
                    name_path_display = face_pathes[i-1]

            #match prods
            product_path_display = ''
            i = 0
            for prod_name in product_names:
                i += 1
                if results[1].lower() in prod_name.lower():
                    product_path_display = product_pathes[i - 1]
                    print('yay')
            print(product_path_display)
            print('yo')
            async_to_sync(channel_layer.group_send)(
                'info_group',
                {
                    'type': 'send_message',
                    'message': name_path_display,
                    'product': product_path_display,
                }
            )
            return Response(results, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_image(self, image):
        # Convert PIL image to tensor
        img = Image.open(image)
        img = img.convert("RGB")

        # Run YOLOv8 inference
        product = self.detect_product(img)
        face_name = self.face_recog(img)
        results = []
        current_month = datetime.now().month
        results.append(current_month)
        results.append(product)
        results.append(face_name)
        print(results)
        return results

    def detect_product(self, image):
        model = YOLO("./iic_api/yolov-model/best.pt")
        # Predict with the model
        results = model(image)  # predict on an image
        # for result in results:
        #     print(result["name"], result["confidence"], result["box"])
        names = model.names
        for r in results:
            boxes = r.boxes
            for box in boxes:
                return names[int(box.cls)]

    def face_recog(self, image):
        # Load a sample picture and learn how to recognize it.
        obama_image = face_recognition.load_image_file("iic_server/dataset-faces/obama.jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        # Load a second sample picture and learn how to recognize it.
        biden_image = face_recognition.load_image_file("iic_server/dataset-faces/biden.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

        a_baimbetova = face_recognition.load_image_file("iic_server/dataset-faces/a-baimbetova.jpg")
        a_baimbetova_encoding = face_recognition.face_encodings(a_baimbetova)[0]

        d_lee = face_recognition.load_image_file("iic_server/dataset-faces/d-lee.jpg")
        d_lee_encoding = face_recognition.face_encodings(d_lee)[0]

        h_yoshizaki = face_recognition.load_image_file("iic_server/dataset-faces/h-yoshizaki.jpg")
        h_yoshizaki_encoding = face_recognition.face_encodings(h_yoshizaki)[0]

        y_maruyama = face_recognition.load_image_file("iic_server/dataset-faces/y-maruyama.png")
        y_maruyama_encoding = face_recognition.face_encodings(y_maruyama)[0]

        # # Test
        # unknown_image = face_recognition.load_image_file("doyoon.jpg")
        # unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

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
            "Barack Obama",
            "Joe Biden",
            "Aidana Baimbetova",
            "Doyoon Lee",
            "Hibiki Yoshizaki",
            "Yui Maruyama"
        ]

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []

        # Test (Put the received image data by raspberry pi here)

        #unknown_image = face_recognition.load_image_file(image)
        unknown_image = np.array(image)
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        face_names = []
        name = "Unknown"
        for face_encoding in unknown_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
            print(face_names)
        return name