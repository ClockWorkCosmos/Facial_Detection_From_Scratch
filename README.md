# Facial_Detection_From_Scratch
Python; Machine Vision; Facial Detection

!WARNING ALL PHOTOS MUST BE OF THE SAME SIZE!

Compares a face to a reference database of the desired face to detect and returns the similarity percentile. If the similarity percentile is greather than or equal to the similarity threshold, return a positive match 
to the face.

Usage example:
  Note - Make sure face is centered in the photo and room is well lit. Prone to micro-distortions.
  1. Create a subfolder (within this program's directory) containing some reference photos of a face you wish to detect. Have at least ten photos taken from slightly different angles. Name the prime reference photo 'face'. Call this folder 'database'.
  2. '>> Test Photo: ' input the file path to the face you wish to use.

Required modules / libraries:
  1. OS
  2. Random
  3. Math
  4. Termcolor
  5. PyGame

