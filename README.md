<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/dynle/raspi-inventory-management-system">
    <img src="images/logo.png" alt="Logo" width="160" height="160">
  </a>
<h3 align="center">Raspberry Pi Inventory Management System</h3>
  <p align="center">
    A system to automate accounting in the IIC purchasing department using Raspberry Pi and image recognition.
    <br />
    <a href="https://github.com/dynle/raspi-inventory-management-system"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot1]](https://github.com/dynle/raspi-inventory-management-system)
[![Product Name Screen Shot][product-screenshot2]](https://github.com/dynle/raspi-inventory-management-system)

The Raspbeery Pi Inventory Management System project was initiated to improve the current purchasing system in our lab's IIC department. The traditional method required individuals to leave money for the items they took, which made it difficult to track who bought what and whether payments were accurately made. Our project aimed to solve this problem by developing a system that automatically records purchases using Raspberry Pi and image recognition technology.

### Key Features:
- **Automated Purchase Recording**: The system uses Raspberry Pi to take photos of the item and the person buying it.
- **Image Recognition**: The captured images are processed using a Django server, which employs a face recognition model and a YOLOv8 object detection model to identify the buyer and the product.
- **Slack Integration**: The system includes a Slack chatbot that summarizes the monthly purchases for each user and notifies them of the total amount due.
- **Database Management**: All transaction data is stored in a SQLite3 database on the Raspberry Pi, making it easy to manage and retrieve records.

### Project Challenges:
- **Raspberry Pi Limitations**: The team faced difficulties due to the lower-than-expected performance of the Raspberry Pi, particularly in image processing tasks.
- **System Stability**: Ensuring the operating system on the Raspberry Pi remained stable was a significant challenge.
- **Learning Experience**: The project provided valuable experience in building IoT systems and highlighted the need for considering the computational limits of IoT devices in model design.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [Raspberry Pi](https://www.raspberrypi.org/)
* [Django](https://www.djangoproject.com/)
* [Slack API](https://api.slack.com/)
* [SQLite3](https://www.sqlite.org/index.html)
* [YOLOv8](https://github.com/ultralytics/yolov5)
* [Face Recognition](https://github.com/ageitgey/face_recognition)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites

* Python 3.7 or 3.8
* Raspberry Pi 3 * 3
* Raspberry Pi Camera Module
* 7" Raspberry Pi Touch Display
* Laptop

### Installation

1. Get a free API key at [Slack](https://slack.com)
2. Clone the Repo
  ```sh
  git clone https://github.com/dynle/raspi-inventory-management-system
  ```
3. Create `.env ` file and enter your API and slack channel ID
  ```js
  SLACK_BOT_TOEKN = 'ENTER YOUR API'
  CHANNEL_ID = 'ENTER YOUR CHANNEL ID'
  ```
4. Install necessary packages with pip
5. Train a product detection model with dataset/proudcts (`train.ipynb`)
  ```sh
  yolo task=detect mode=train model=./weights/yolov8s.pt data=./dataset-new-3cls/data.yaml epochs={100} imgsz=640 device=mps patience=100
  ```
6. Set IP address and run `raspberrypi_take_picture_and_send.py` file on a raspberry pi with a camera module
  ```sh
  python raspberrypi_take_picture_and_send.py
  ```
7. Set IP address and run `database_Data_in.py` and `database_Output_data.py` files on another raspberry pi
  ```sh
  python database_Data_in.py
  python database_Output_data.py
  ```
8. Run django server with a laptop to run two detection models and open HMTL page
9. Connect three raspberry pi devices and the laptop on the same network
10. Open the HTML page using the django server ip address with the other raspberry pi with the touch display to see detection results

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To use the system, deploy the Django server, and ensure the Raspberry Pi cameras are connected and running. The Slack chatbot will automatically notify users at the end of the month about their purchase totals.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot1]: images/project1.png
[product-screenshot2]: images/project2.png
