import cv2
import math as m
import numpy as np
import os
import pygame
import random as r
import termcolor
from termcolor import colored, cprint
from pygame.locals import *

pygame.init()

reference_path = str("")
reference_image = [0.00]

comparison_path = str("")
comparison_image = [0.00]

similarity_score = int(0)
similarity_percentile = float(0.00)
similarity_threshold = float(0.00)

additional_images = [""]
additional_image_data = [0.00]
solutions_set = [0.0, 0.0, 0.0, 0.0]

solutions_set_ii = [0.00]

image_size = int(300)

result = str("")

def fetch_image_data(IMAGE_PATH):
	image = pygame.image.load(IMAGE_PATH)
	width, height = image.get_size()

	rgb_data = []
	for y in range(height):
		for x in range(width):
			pixel = image.get_at((x, y))
			rgb_values = (pixel.r, pixel.g, pixel.b)
			rgb_data.append(rgb_values)
	return rgb_data

def fetch_greyscale_data(IMAGE_PATH):
	image = pygame.image.load(IMAGE_PATH)

	width, height = image.get_size()

	greyscale_data = []

	for y in range(height):
		for x in range(width):
			pixel = image.get_at((x, y))
			greyscale_value = int(0.3 * pixel.r + 0.59 * pixel.g + 0.11 * pixel.b)
			greyscale_data.append(greyscale_value)
	return greyscale_data

def fetch_blackwhite_data(IMAGE_PATH, threshold=128):
	image = pygame.image.load(IMAGE_PATH)

	width, height = image.get_size()

	blackwhite_data = []

	for y in range(height):
		for x in range(width):
			pixel = image.get_at((x, y))
			average_value = (pixel.r + pixel.g + pixel.b) // 3
			blackwhite_value = 0 if average_value < threshold else 255
			blackwhite_data.append(blackwhite_value)
	return blackwhite_data

def find_similarity(REFERENCE, COMPARISON):
	similarity_score = 0
	similarity_percentile = 0.00

	for x, _ in enumerate(REFERENCE):
		ref_value = round(sum(REFERENCE[x]), 10) if isinstance(REFERENCE[x], tuple) else round(REFERENCE[x], 10)
		comp_value = round(sum(COMPARISON[x]), 10) if isinstance(COMPARISON[x], tuple) else round(COMPARISON[x], 10)

		if comp_value == ref_value:
			similarity_score += 2
		else:
			similarity_score += -1

	if similarity_score < 0:
		similarity_score = 0

	similarity_percentile = (similarity_score / ((image_size * image_size) * 3)) * 100
	return abs(similarity_percentile)

def remove_background_and_save(image_path):
	if not os.path.exists(image_path):
		print(f"Error: Image file does not exist at {image_path}")
		return

	image = cv2.imread(image_path)

	if image is None:
		print(f"Error: Unable to load image at {image_path}")
		return

	image = cv2.imread(image_path)

	lower_skin = np.array([0, 10, 40], dtype=np.uint8)
	upper_skin = np.array([30, 255, 255], dtype=np.uint8)

	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	mask_skin = cv2.inRange(hsv, lower_skin, upper_skin)

	result = cv2.bitwise_and(image, image, mask=mask_skin)

	cv2.imwrite(image_path, result)

def prRed(skk): 
	print("\033[91m {}\033[00m" .format(skk)) 

def prGreen(skk): 
	print("\033[92m {}\033[00m" .format(skk))


comparison_path = input(">> Test Photo: ")
remove_background_and_save(comparison_path)

while True:
	reference_path = "database/prime.png"
	reference_image = fetch_image_data(reference_path)

	remove_background_and_save(reference_path)

	reference_directory = "database"

	if os.path.exists("similarity_threshold.txt"):
		with open("similarity_threshold.txt", "r") as file:
			similarity_threshold = float(file.read())
	else:
		additional_images = []
		solutions_set = []
		
		prGreen(">> Evaluating similarity threshold for reference database.")

		misc_counter = 0
		misc_counter_ceil = 0

		for filename in os.listdir(reference_directory):
			if filename.endswith((".jpg", ".png")):
				misc_counter_ceil += 1
			else:
				misc_counter_ceil += 0

		misc_counter_ceil += -1

		for filename in os.listdir(reference_directory):
			if filename.endswith((".jpg", ".png")):

				prGreen(">> " + str(misc_counter) + "/" + str(misc_counter_ceil))

				additional_image_path = os.path.join(reference_directory, filename)
				additional_images.append(additional_image_path)

				additional_image_data = fetch_image_data(additional_image_path)
				reference_image = fetch_image_data(reference_path)
				solutions_set.append(find_similarity(reference_image, additional_image_data))

				additional_image_data = fetch_blackwhite_data(additional_image_path)
				reference_image = fetch_blackwhite_data(reference_path)
				solutions_set.append(find_similarity(reference_image, additional_image_data))

				additional_image_data = fetch_greyscale_data(additional_image_path)
				reference_image = fetch_greyscale_data(reference_path)
				solutions_set.append(find_similarity(reference_image, additional_image_data))

				remove_background_and_save(additional_image_path)

				misc_counter += 1

		similarity_threshold = sum(solutions_set) / len(solutions_set)

		similarity_threshold = (similarity_threshold + 50.0) / 2

		prGreen(">> Done.")

		with open("similarity_threshold.txt", "w") as file:
			file.write(str(similarity_threshold))

	try:
		prGreen(">> Working...")

		reference_path = "database/prime.png"

		comparison_image = fetch_image_data(comparison_path)
		reference_image = fetch_image_data(reference_path)
		solutions_set_ii.append(find_similarity(reference_image, comparison_image))

		comparison_image = fetch_blackwhite_data(comparison_path)
		reference_image = fetch_blackwhite_data(reference_path)
		solutions_set_ii.append(find_similarity(reference_image, comparison_image))

		comparison_image = fetch_greyscale_data(comparison_path)
		reference_image = fetch_greyscale_data(reference_path)
		solutions_set_ii.append(find_similarity(reference_image, comparison_image))
		
		similarity_percentile = sum(solutions_set_ii) / len(solutions_set_ii)

		if similarity_percentile >= similarity_threshold:
			similarity_percentile = 100
			result = "Faces are a match."
			break
		else:
			break
	except:
		prRed(">> Error: File Not Found.")
		exit()

print(">> Face Similarity: ", similarity_percentile, "%")
print(">> Similarity Threshold: ", similarity_threshold, "%")

if result == "":
	result = "Faces are not a match."

if result != "Faces are not a match.":
	prGreen(">> Result: " + result)
else:
	prRed(">> Result: " + result)

input("")
