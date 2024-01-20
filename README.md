# Facial_Detection_From_Scratch
Python; Machine Vision; Facial Detection

!WARNING ALL PHOTOS MUST BE OF THE SAME SIZE; OVERALL SIMILARITY IS BASED ON COLOR SIMILARITIES, NOT FACIAL FEATURES, THEREFORE THIS NOT A 100% RELIABLE PROGRAM! 

Compares a face to a prime reference of the desired face to detect and returns the similarity percentile. If the similarity percentile is greather than or equal to the similarity threshold, return a positive match 
to the face inputted.

Usage example:
  Note - Make sure face is centered in the photo and room is well lit. Prone to micro-distortions.
  1. Create a subfolder (within this program's directory) containing some reference photos of a face you wish to detect. Have at least five hundred reference photos taken from
     slightly different angles and with different backgrounds (helps significantly increase accuracy of facial detection). Name the prime reference photo 'prime' with the '.png' or '.jpg' extension (change usage
     reference in program). Call this folder 'database'. Your prime photo should be of the desired face to detect looking straight ahead, against a solid, not white or black, background (helps face stand out).
     
  3. Use the 'augment.py' program (small program to automatically edit photos randomly; turns small seed dataset into big dataset) to expand database image diversity (aids in computing precise similarity thresholds)
  4. '>> Test Photo: ' input the file path to the face you wish to use.
  5. '>> Evaluating similarity threshold from reference database.' indicates that the program is computing how similar a photo, in various formats, has to be in comparison to the prime photo to return a positive match.

Required modules / libraries:
  1. OS
  2. Random
  3. Math
  4. Termcolor
  5. PyGame
  6. CV2
