# raspi_serverless
Code for motion detection  using Raspberry Pi, pushing the images to Azure Blob, running serverless code to analyze those images via Azure Cognitive

The Raspi folder has code that you will need to run on the Raspberry Pi. This code will reference the conf.json file for camera related settings. When motion is detected Raspi takes an image and uploads it to Azure Blob. For the code to work you will need to install the cv2 library

The Azure Serverless folder contains Python Code that runs on the Azure Blob container, when image is uploaded to Blob the URL of the image is sent to Azure Cognitive service which analyzes the image and returns the findings. Part of those findings are parsed and then sent via Twilio to a text message.

Instructions on how to setup Python Functions for Azure
https://gist.github.com/ashfondu/ac5395dcb45829d39cb1bb7362131614

Tutorial on how to install OpenCV (cv2)
https://www.deciphertechnic.com/install-opencv-python-on-raspberry-pi/
