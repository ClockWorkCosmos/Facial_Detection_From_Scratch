import cv2
import math as m
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

result = str("")

def zoom_effect(image_path, zoom_factor):
	img = cv2.imread(image_path)

	height, width = img.shape[:2]
	center = (width // 2, height // 2)

	zoom_matrix = cv2.getRotationMatrix2D(center, 1, zoom_factor)

	zoomed_img = cv2.warpAffine(img, zoom_matrix, (width, height))
	cv2.imwrite(image_path, zoomed_img)

def reverse_zoom_effect(image_path, original_data):
	cv2.imwrite(image_path, original_data)

def copy_image_data(image_path):
	img = cv2.imread(image_path)	
	return img

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
			similarity_score += 1
		else:
			similarity_score += 0

	similarity_percentile = (similarity_score / len(REFERENCE)) * 100
	return abs(similarity_percentile)

def prRed(skk): 
	print("\033[91m {}\033[00m" .format(skk)) 

def prGreen(skk): 
	print("\033[92m {}\033[00m" .format(skk))


comparison_path = input(">> Test Photo: ")

while True:
	reference_path = "database/prime.jpg"
	original_reference_data = [0]
	reference_image = fetch_image_data(reference_path)

	reference_directory = "database"

	if os.path.exists("similarity_threshold.txt"):
		with open("similarity_threshold.txt", "r") as file:
			similarity_threshold = float(file.read())
	else:
		original_reference_data = copy_image_data(reference_path)
		
		zoom_factor = 0.33
		zoom_effect(reference_path, zoom_factor)
		
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
				solutions_set.append(find_similarity(reference_image, additional_image_data))

				additional_image_data = fetch_blackwhite_data(additional_image_path)
				solutions_set.append(find_similarity(reference_image, additional_image_data))

				additional_image_data = fetch_greyscale_data(additional_image_path)
				solutions_set.append(find_similarity(reference_image, additional_image_data))
				
				original_image_data = copy_image_data(additional_image_path)
				zoom_effect(additional_image_path, zoom_factor)
				additional_image_data = fetch_greyscale_data(additional_image_path)
				solutions_set.append(find_similarity(reference_image, additional_image_data))
				reverse_zoom_effect(additional_image_path, original_image_data)

				misc_counter += 1

		similarity_threshold = sum(solutions_set) / len(solutions_set) * 3

		reverse_zoom_effect(reference_path, original_reference_data)
		
		prGreen(">> Done.")

		with open("similarity_threshold.txt", "w") as file:
			file.write(str(similarity_threshold))

	try:
		prGreen(">> Working...")

		reference_path = "database/prime.jpg"

		comparison_image = fetch_image_data(comparison_path)
		similarity_percentile += find_similarity(reference_image, comparison_image)

		comparison_image = fetch_blackwhite_data(comparison_path)
		similarity_percentile += find_similarity(reference_image, comparison_image)

		comparison_image = fetch_greyscale_data(comparison_path)
		similarity_percentile += find_similarity(reference_image, comparison_image)

		original_image_data = copy_image_data(comparison_path)
		original_reference_data = copy_image_data(reference_path)

		zoom_effect(reference_path, zoom_factor)
		zoom_effect(comparison_path, zoom_factor)

		comparison_image = fetch_image_data(comparison_path)
		similarity_percentile += find_similarity(reference_image, comparison_image)

		reverse_zoom_effect(comparison_path, original_image_data)
		reverse_zoom_effect(reference_path, original_reference_data)

		similarity_threshold = similarity_threshold / 4

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
