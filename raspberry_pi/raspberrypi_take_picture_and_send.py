from picamera import PiCamera
import time
import datetime
import RPi.GPIO as GPIO
import requests
import socket
import ast

#GPIO_15
button_pin = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = PiCamera()
#picamera2.configure(picam2.create_still_configuration())

def take_picture():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_path = f"./image_{timestamp}.png"
    camera.capture(file_path)
    print(f"Image saved to {file_path}")
    return file_path

def send_image(image_path, server_url, sock):
    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}
        #print(image_file)
        response = requests.post(server_url, files=files)
        send_info(response, sock)
    return response

def send_info(response, sock):
    try:
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.connect((raspi_ip, target_port))
        dt = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        data = ""
        
        response = ast.literal_eval(response.text)
        print(response)
        
        data += str(dt.year)
        data += " "
        data += str(response[0])
        data += " "
        data += response[2]
        data += " "
        data += response[1]
        
        print(data)
        
        sock.sendall(data.encode('utf-8'))
        
    except Exception as e:
        print(f"an error occurred: {e}")
    
def main():
    try:
        camera.start_preview()
        print("Camera started. Press the button to take a picture.")
        server_url = "http://192.168.156.87:8000/api/upload/"
        #server_url = "192.168.156.87:8000/api"
        
        raspi_ip = "192.168.151.44"
        target_port = 10000
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((raspi_ip, target_port))
        
        while True:
            button_state = GPIO.input(button_pin)
            if button_state == GPIO.LOW:
                image_path = take_picture()
                response = send_image(image_path, server_url, sock)
                print(f"Response from server: {response.status_code}, {response.text}")
                while GPIO.input(button_pin) == GPIO.LOW:
                    time.sleep(0.8)
                print("Waiting for the next button press...")
    
    except KeyboardInterrupt:
        print("Program terminated.")
        
    finally:
        camera.stop_preview()
        GPIO.cleanup()
        sock.close()
        
        
if __name__ == "__main__":
    main()
