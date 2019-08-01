# Ben Ryan
# Where's Wally?
# This program will attepmpt to find Wally in an a Where's Wally image, based on his red and white strips.
# It will also draw a bounding rectangle around Wally and "WALLY" on top of him.

import numpy as np
import cv2
import easygui

h,w = 0,0
stepByStep = False
		
#Processes the image to find wally
def process(imgOrig):
	img = imgOrig.copy()
	
	#select desired colour ranges
	red1 = cv2.inRange(img, (10,15,80), (85,75,177))
	red2 = cv2.inRange(img, (132,127,175), (201,180,255))
	red = red1+red2

	white = cv2.inRange(img, (210, 210, 230), (255, 255, 255))

	#erode the 2 masks with horizonatal structEl
	structElErode = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
	redErode = cv2.erode(red, structElErode, 1)
	whiteErode = cv2.erode(white, structElErode, 1)

	#filter out unimportant pixels from the 2 masks
	filteredMask = filter(redErode, whiteErode)

	#open the image using square structuring element
	structEl = cv2.getStructuringElement(cv2.MORPH_RECT, (2,3))
	opened = cv2.morphologyEx(filteredMask, cv2.MORPH_OPEN, structEl)

	#find the biggest contour, should be Wally
	contours, _ = cv2.findContours(opened,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	
	#showing step by step output
	if stepByStep == True:
		print("\nPress any key to continue")
		showImage("Original", imgOrig, True)
		
		showImage("Red Mask", red, True)
		showImage("White Mask", white, True)
		
		#show just red and white section together just for display purposes
		nofilter = red + white
		showImage("Red + White no Filter", nofilter, True)
		
		showImage("Eroded Red Mask", redErode, True)
		showImage("Eroded White Mask", whiteErode , True)
			
		#apply the mask just for step by step display purposes
		filtered = cv2.bitwise_and(img, img, mask=filteredMask) 
		showImage("Filtered Mask", filteredMask, True)
		showImage("Filtered Image", filtered, True)
		
		showImage("Opened", opened, True)
	
	try:
		#get largest contour bounding rect
		c = max(contours, key = cv2.contourArea)
		
		x, y, w, h = cv2.boundingRect(c)

		#get coords
		topLeft = (x - 10, y - 20)
		bottomRight = (x + w + 10, y + h + 20)
		
		#draw bounding rect and label on copy 
		processed = imgOrig.copy()
		cv2.rectangle(processed, topLeft, bottomRight , (0,255,0), 2)
		cv2.putText(processed, "WALLY", topLeft, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
		
	except ValueError:
		print("No contours found after filtering")
		return None
		
	return processed
	
#filters the red and white masks based on each other
def filter(red, white):
	#create a new blank 2D image for forming the combined mask
	comb = np.zeros((h,w), np.uint8)

	#loop through the pixels 1 by 1
	for x in range(0, w):
		for y in range(0, h):
		
			#if pixel is white
			if white[y,x] == 255:
				redTot, whiteTot = checkSurrounding((x,y),red,white)

				#add the current pixel to combined if its surrounding pixels meet the following conditions
				if redTot >= (int(w*0.008)) and redTot < (int(w*0.02)) and whiteTot < (int(w*0.008)):
					comb[y,x] = 255
					
			#if pixel is red
			elif red[y,x] == 255:
				redTot, whiteTot = checkSurrounding((x,y),red,white)

				#add the current pixel to combined if its surrounding pixels meet the following conditions
				if whiteTot >= (int(w*0.002)) and whiteTot < (int(w*0.02)) and redTot < (int(w*0.02)):
					comb[y,x] = 255		
				
	return comb

#checks the amount of pixels set in the red, and white masks surrounding provided point
def checkSurrounding(coords, red, white):	
	x, y = coords
	redTot, whiteTot = 0,0
	
	#loop through surrounding pixels
	for x2 in range(x-(int(w*0.003)), x+(int(w*0.003))+1):
		for y2 in range(y-(int(w*0.003)), y+(int(w*0.003))+1):
			
			#if not the pixel being considered inc counter bases on colour
			if x2 != x and y2 != y:
				
				#Correct values when on the edge so we don't fall off
				if x2 >= w: x2 -= (x2-w)+1
				if y2 >= h: y2 -= (y2-h)+1
			
				if red[y2,x2] == 255:
					redTot += 1
				elif white[y2,x2] == 255:
					whiteTot += 1
	
	return redTot, whiteTot
	
#Retrieves the image specified by the user. Also gets the shape parameters and stores them globally for ease of access later
def getImage():
	img = None
	
	while img is None:
		fileName = easygui.fileopenbox()
		img = cv2.imread(fileName)
		
		global h, w
		h, w, _ = np.shape(img)

		#if a very large image resize to help with performance
		#really should use percentages to resize properly, but most
		#sample images are approximately the same ratio.
		if h > 1300 or w > 1300:
			img = cv2.resize(img, (1024, 724))
			h, w, _ = np.shape(img)
		
		if img is None:
			print("Error retrieving file. Please try again")
	
	return img
	
# Used for easy display of images, can specify title, image and a boolean that controls whether to wait for input before continuing
def showImage(title, img, hold):
	cv2.imshow(title, img)
	
	if hold == True:
		cv2.waitKey(0)
		
#used to check whether the user wants to see the output at each step, or just the final output
def checkStepByStep():
	ans = input('Show image step by step?(y/n)')

	if ans == 'y' or ans == 'Y':
		return True
	else:
		return False
				
# controls flow of the program
def main():
	global stepByStep
	stepByStep = checkStepByStep()

	img = getImage()
	
	print("\nThis may take a few seconds.\nProcessing...")
	processed = process(img)
	
	if processed is not None:
		showImage("Wally is in the green box.", processed, True)

if __name__ == '__main__':
	main()