
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import json
import cv2
import datetime
import time
from azure.storage.blob import BlockBlobService
import os

#initialize Config file
conf=json.load(open('conf.json'))

#initalize Azure Storage
blob = BlockBlobService(
	account_name = conf['azure_account'],
	account_key = conf['azure_key'])

#init camera
camera = PiCamera()
camera.resolution = tuple(conf['resolution'])
camera.rotation = conf['rotation']
camera.framerate = conf['fps']
rawCapture = PiRGBArray(camera, size=tuple(conf['resolution']))


# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print "[INFO] warming up..."
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0
print('[INFO] talking raspi started !!')

#capture logic
for f in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
	timestamp = datetime.datetime.now()
	frame=f.array
	timestamp = datetime.datetime.now()
	text = "unoccupied"
	
	grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	grey = cv2.GaussianBlur(grey, tuple(conf['blur_size']), 0)	
	
	if avg is None:
		print '[INFO] starting background model...'	
		avg = grey.copy().astype('float')
		rawCapture.truncate(0)
		continue

	frameDelta = cv2.absdiff(grey, cv2.convertScaleAbs(avg))
	cv2.accumulateWeighted(grey, avg, 0.5)
	thresh = cv2.threshold(frameDelta, conf["delta_thresh"] , 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	im2 ,cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < conf["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"

# draw the text and timestamp on the frame
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

# check to see if the room is occupied
	if text == "Occupied":
                # save occupied frame
                #cv2.imwrite("/tmp/talkingraspi_{}.jpg".format(motionCounter), frame);
		filename = "PiCam-" + datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")
		
                # check to see if enough time has passed between uploads
                if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:

                        # increment the motion counter
                        motionCounter += 1;

                        # check to see if the number of frames with consistent motion is
                        # high enough
                        if motionCounter >= int(conf["min_motion_frames"]):
                 		camera.capture(filename)         
                                #f2 = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
				#f3 = camera.start_recording(f2)
				#sleep(10)
				#f3.stop_recording()
				blob.create_blob_from_path(conf['container_name'], filename, filename)
				# update the last uploaded timestamp and reset the motion
                                # counter
                                lastUploaded = timestamp
                                motionCounter = 0
				
				os.remove(filename)
	# otherwise, the room is not occupied
	else:
		motionCounter = 0

#show the frame
	if conf["show_video"]:
	
		cv2.imshow('Original', frame)
		cv2.imshow('Output' , thresh)
	
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	rawCapture.truncate(0)