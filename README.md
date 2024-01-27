# Facial Detection From Scratch
Python; Facial detection; OpenCV

! WARNING: ONLY THE FACE MUST BE PRESENT IN THE PHOTOS. BACKDROP PIXELS MAY CAUSE FALSE MATCHES / MISMATCHES; ALL PHOTOS USED MUST ALSO BE OF THE SAME SIZE !

Usage example:
  1. Create a folder for the desired face we wish to detect, name it 'database'. Make sure this folder is in the same directory as 'main.py' .
  2. Take a reference photo of the face we wish to detect, make sure only the face is present in the photo and that the person is looking straight ahead at the camera.
     Name it 'prime.png' and add it to our database folder.
  3. Take 9x additional reference photos from slightly different angles and in different lighting effects. Add these photos to our database folder as well.

  4. Run 'main.py' from the command line interface.
  5. '>> Test photo: ' - enter the filepath to the photo we wish to determine 'match' or 'mismatch' for.
  6. '>> Evaluating similarity threshold for reference database.' - If a similarity threshold has not already been computed (first time usage), evaluate a similarity threshold.
     The similarity threshold is a number dictating how similar our inputted photo has to be in comparison to our reference photo in order to return a positive match.
     The similarity threshold is the average similarity value between each of our additional reference photos in comparison to our initial reference photo.

  8. If the returned similarity percentile for the inputted photo is lesser than the similarity threshold, return 'Faces are not a match.' .
  9. Else if the percentage is greater than or equal to the threshold, return 'Faces are a match.' .

Required modules / libraries:
	* cv2
	* math
	* numpy
	* os
	* pygame
	* random
	* termcolor
