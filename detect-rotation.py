# This script reads in a file and tries to determine which orientation is correct 
# by looking for faces in the photos
# It starts with the existing orientation, then rotates it 90 degrees at a time until
# it has either tried all 4 directions or until it finds a face

# INSTALL: Put the xml files in /usr/local/share, or change the script. Put whatsup somewhere in your path

# Usage: whatsup [--debug] filename
# Returns the number of degrees it should be rotated clockwise to orient the faces correctly

# Some code came from here: http://blog.jozilla.net/2008/06/27/fun-with-python-opencv-and-face-detection/
# The rest was cobbled together by me from the documentation here [1] and from snippets and samples found via Google
# [1] http://opencv.willowgarage.com/documentation/python/core_operations_on_arrays.html#createmat

import sys
import os
import cv

def detectFaces(small_img,loadedCascade):
    tries = 0 # 4 shots at getting faces. 

    while tries < 4:
	faces = cv.HaarDetectObjects(small_img, loadedCascade, cv.CreateMemStorage(0), scale_factor =1.2, min_neighbors =2, flags =cv.CV_HAAR_DO_CANNY_PRUNING)
	if(len(faces) > 0):
	    if(sys.argv[1] == '--debug'):
		for i in faces:
		    cv.Rectangle(small_img, (i[0][0],i[0][1]),(i[0][0] + i[0][2],i[0][1] + i[0][3]), cv.RGB(255,255,255), 3, 8, 0)
		cv.NamedWindow("Faces")
		cv.ShowImage("Faces",small_img)
		cv.WaitKey(1000)
	    return tries * 90

	# The rotation routine:  
	tmp_mat = cv.GetMat(small_img)
	tmp_dst_mat = cv.CreateMat(tmp_mat.cols,tmp_mat.rows,cv.CV_8UC1) # Create a Mat that is rotated 90 degrees in size (3x4 becomes 4x3)
	dst_mat = cv.CreateMat(tmp_mat.cols,tmp_mat.rows,cv.CV_8UC1) # Create a Mat that is rotated 90 degrees in size (3x4 becomes 4x3)

	# To rotate 90 clockwise, we transpose, then flip on Y axis
	cv.Transpose(small_img,tmp_dst_mat) # Transpose it
	cv.Flip(tmp_dst_mat,dst_mat,flipMode=1) # flip it

	# put it back in small_img so we can try to detect faces again
	small_img = cv.GetImage(dst_mat) 
	tries = tries + 1
    return False 


# Detect which side of the photo is brightest. Hopefully it will be the sky.
def detectBrightest(image):
    image_scale = 4 # This scale factor doesn't matter much. It just gives us less pixels to iterate over later
    newsize = (cv.Round(image.width/image_scale), cv.Round(image.height/image_scale)) # find new size
    small_img = cv.CreateImage(newsize, 8, 1) 
    cv.Resize( image, small_img, cv.CV_INTER_LINEAR )

    # Take the top 1/3, right 1/3, etc. to compare for brightness
    width = small_img.width
    height = small_img.height
    top = small_img[0:height/3,0:width]  
    right = small_img[0:height,(width/3*2):width]
    left = small_img[0:height,0:width/3]
    bottom = small_img[(height/3*2):height,0:height]

    sides = {'top':top,'left':left,'bottom':bottom,'right':right}

    # Find the brightest side
    greatest = 0
    winning = 'top'
    for name in sides:
	sidelum = 0
	side = sides[name]
	for x in range(side.rows - 1):
	    for y in range(side.cols - 1):
		sidelum = sidelum + side[x,y]
	sidelum = sidelum/(side.rows*side.cols)
	if sidelum > greatest:
	    winning = name

    if(sys.argv[1] == '--debug'):
	if winning == 'top':
	    first = (0,0)
	    second = (width,height/3)
	elif winning == 'left':
	    first = (0,0)
	    second = (width/3,height)
	elif winning == 'bottom':
	    first = (0,(height/3*2))
	    second = (width,height)
	elif winning == 'right':
	    first = ((width/3*2),0)
	    second = (width,height)
	cv.Rectangle(small_img,first,second,cv.RGB(125,125,125),3,8,0)
	cv.NamedWindow("Faces")
	cv.ShowImage("Faces",small_img)
	cv.WaitKey(3000)

    returns = {'top':0,'left':90,'bottom':180,'right':270}
    
    # return the winner
    if sys.argv[1] == '--debug':
	print "The " + winning + " side was the brightest!"
    return returns[winning]

# Try a couple different detection methods
def trydetect():
    # Load some things that we'll use during each loop so we don't keep re-creating them
    grayscale = cv.LoadImageM(os.path.abspath(sys.argv[-1]),cv.CV_LOAD_IMAGE_GRAYSCALE) # the image itself

    # Get more at: https://code.ros.org/svn/opencv/tags/latest_tested_snapshot/opencv/data/haarcascades/
    cascades = ( # Listed in order most likely to appear in a photo
	    '/usr/local/share/haarcascade_frontalface_alt.xml',
	    '/usr/local/share/haarcascade_profileface.xml',
	    '/usr/local/share/haarcascade_fullbody.xml',
	    )

    for cascade in cascades:
	loadedCascade = cv.Load(cascade) 
	image_scale = 4 
	while image_scale > 0: # Try 4 different sizes of our photo
	    newsize = (cv.Round(grayscale.width/image_scale), cv.Round(grayscale.height/image_scale)) # find new size
	    small_img = cv.CreateImage(newsize, 8, 1 ) 
	    cv.Resize( grayscale, small_img, cv.CV_INTER_LINEAR )
	    returnme = detectFaces(small_img,loadedCascade)
	    if returnme is not False:
		return returnme
		
	    image_scale = image_scale - 1
    return detectBrightest(grayscale) # no faces found, use the brightest side for orientation instead


# Usage Check
if ((len(sys.argv) != 2 and len(sys.argv) != 3) or (len(sys.argv) == 3 and sys.argv[1] != '--debug')):
    print "USAGE: whatsup [--debug] filename"
    sys.exit(-1)

# Sanity check
if not os.path.isfile(sys.argv[-1]):
    print "File '" + sys.argv[-1] + "' does not exist"
    sys.exit(-1)

# Make it happen
print str(trydetect()),