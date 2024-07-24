import subprocess

def run_script(script_name, test_image):
    result = subprocess.run(["python", script_name, test_image], stdout=subprocess.PIPE)
    print(result.stdout.decode("utf-8"))

test_image = ""

run_script("product_detection/predict_objects.py", test_image)
run_script("face_recognition/predict_faces.py", test_image)
