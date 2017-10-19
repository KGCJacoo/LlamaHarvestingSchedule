import sys
import time
import glob
import random

import pygame
from pygame.locals import *

# takes the size of the screen, and the size of the image, and scales the image down proportionally
def findOptimumSize(screensize, imagesize):
	screenratio = screensize[0]/screensize[1]
	imageratio = imagesize[0]/imagesize[1]

	if imageratio > screenratio:
		# scale down width
		result = (screensize[0], int(imagesize[1] * (screensize[0] / imagesize[0])))
	elif imageratio == screenratio:
		result = screensize
	else:
		# scale by height
		result = (int(imagesize[0] * (screensize[1] / imagesize[1])), screensize[1])

	#print("Sceen Ratio: {}    Image Ratio: {}       Orig: {},{}   Scaled: {},{}".format(screenratio, imageratio, imagesize[0], imagesize[1], result[0], result[1]))

	return result

# generate list of images
base = 'photos'
types = [ 'jpg', 'png', 'gif' ]
images = []
for filetype in types:
	images += glob.glob("{}/*.{}".format(base, filetype))

# pygame segment
pygame.init()

# get display parameters
display_params = pygame.display.Info()
WIDTH = display_params.current_w
HEIGHT = display_params.current_h
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)

keeplooping = True
max_picture_age = 3
last_switch_time = time.time() - max_picture_age
while True:
	# process events
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			#print(event.key)
			#skip forward and backward
			if event.key == 275:
				last_switch_time -= max_picture_age
			if event.key == 276:
				pass# backwards doesn't work on random...

			# faster and slower
			if event.key == 273:
				max_picture_age += 1
			if event.key == 274:
				max_picture_age -= 1

			# quit
			if event.key == 113:
				print("Exiting cleanly")
				pygame.display.quit()
				pygame.quit()
				sys.exit()

	# only switch pictures if enough time has passed
	if time.time() - last_switch_time > max_picture_age:
		# reset last_switch_time
		last_switch_time = time.time()

		# load a random image
		img = pygame.image.load(random.choice(images))

		# get the size of the image.  If it's too large, shrink it to fit.  If it's too small, center it.
		coords = (0,0)
		image_size = img.get_rect().size
		if image_size[0] > WIDTH or image_size[1] > HEIGHT:
			image_size = findOptimumSize((WIDTH, HEIGHT), image_size)
			img = pygame.transform.smoothscale(img, image_size)

		# center the image on the screen, via the upper-left corner
		coords = ((WIDTH / 2) - (image_size[0] / 2), (HEIGHT / 2) - (image_size[1] / 2))
	
		# fill the screen with black, and then blit the image onto it.
		windowSurface.fill((0,0,0))
		windowSurface.blit(img, coords)
		pygame.display.flip()

	# don't murder the CPU
	time.sleep(.1)

pygame.display.quit()
pygame.quit()
sys.exit()
