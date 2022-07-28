# PhotoLab.py: PhotoLab in Python with OpenCV

# Libraries
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import numpy as np

wc = cv2.VideoCapture(0)
seg = SelfiSegmentation(0)

# Set Resolution & FPS
width = 1280 
height = 720
wc.set(3,width)
wc.set(4,height)
wc.set(cv2.CAP_PROP_FPS,60)
fps = cvzone.FPS()

# Toggle Variables and Config
toggleBG = False
toggleEdge = False
toggleSharp = False
toggleThresh = False
loop = True
thresh = 0.5
edge = np.array([[0.0, -1.0, 0.0], 
                   [-1.0, 4.0, -1.0],
                   [0.0, -1.0, 0.0]])
sharp = np.array([[0.0, -1.0, 0.0], 
                   [-1.0, 5.0, -1.0],
                   [0.0, -1.0, 0.0]])

# Loop to Feed the Video
while(loop):
	ret, res = wc.read()
	if(toggleBG == True): # Remove Background
		res = seg.removeBG(res,(0,0,0),threshold=thresh)
	res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY) # Converting Input to Gray Scale3
	if(toggleEdge == True): # Edge Detection
		res = cv2.filter2D(res,-1,edge)
	if(toggleSharp == True): # Sharpen
		res = cv2.filter2D(res,-1,sharp)
	if(toggleThresh == True): # Threshold GLT
		for i in range(height):
			for j in range(width):
				if(res[i,j] > 127): 
					res[i,j] = 255
				else:
					res[i,j] = 0

	fps.update(res)
	cv2.imshow('Result',res)

	# Key Conditions
	if cv2.waitKey(1) & 0xFF == ord('q'): # Quit
		loop = False
	elif cv2.waitKey(1) & 0xFF == ord('b'): # Turn On/Off Removing Background
		toggleBG = not toggleBG
		if(toggleBG == True):
			print('Switched to Removing Background')
		else:
			print('Switched to Original')	
		cv2.destroyAllWindows()
	elif cv2.waitKey(1) & 0xFF == ord('1'): # Turn On/Off Edge Detection
		toggleEdge = not toggleEdge 
		if(toggleEdge == True):
			print('Turned on Edge Detection')
		else:
			print('Turned off Edge Detection')
		cv2.destroyAllWindows()
	elif cv2.waitKey(1) & 0xFF == ord('2'): # Turn On/Off Sharpen
		toggleSharp = not toggleSharp 
		if(toggleSharp == True):
			print('Turned on Sharpen')
		else:
			print('Turned off Sharpen')
		cv2.destroyAllWindows()
	elif cv2.waitKey(1) & 0xFF == ord('3'): # Turn On/Off Thresholding
		toggleThresh = not toggleThresh
		if(toggleThresh == True):
			print('Turned on Thresholding')
		else:
			print('Turned off Thresholding')
		cv2.destroyAllWindows()
	elif cv2.waitKey(1) & 0xFF == ord('u'): # Increase the Threshold if Removing Background
		if(thresh < 1 and toggleBG == True):
			thresh = thresh + 0.1
		print('Increasing threshold to ' + str(thresh))
	elif cv2.waitKey(1) & 0xFF == ord('d'): # Decrease the Threshold if Removing Background
		if(thresh > 0 and toggleBG == True):
			thresh = thresh - 0.1
		print('Increasing threshold to ' + str(thresh))

# Clean Stop
cv2.destroyAllWindows()
wc.release()
print('*****************************************************************')
print('Thank you for Using PhotoLab.py!')
print('*****************************************************************')