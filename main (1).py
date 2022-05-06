from ast import Try
import pygame
import math
from PIL import Image
import asyncio

pos = (250,250)
image = Image.open('pixil-frame-0.png')
image = image.load()

async def frame(time):
	await asyncio.sleep(time)

def raycast(angle, position):
	distance = 0
	poll_pos = position
	right = round(math.cos(angle*deg), 4)
	forward = round(math.sin(angle*deg), 4)
	gval = ()
	while 1:
		gval = image[poll_pos[0],poll_pos[1]]
		poll_pos = (poll_pos[0]+right*2, poll_pos[1]+forward*2)
		distance += 1
		if gval == (0, 0, 0, 255):
			break
	
	return distance

pygame.init()

surface = pygame.display.set_mode((500,500))
deg = (math.pi/180)
#pygame.draw.rect(surface, (255,0,0), pygame.Rect(0,0, 640, 640))
player_angle = 0

while 1:
	facingx = round(math.sin(player_angle*deg), 4)
	facingy = round(math.cos(player_angle*deg), 4)
	
	k = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.MOUSEMOTION:
			player_angle += event.rel[0]

	pygame.draw.rect(surface, (255, 255, 255), [0,0,surface.get_height(), surface.get_width()])

	if k[pygame.K_LEFT]:
		player_angle -= 1

	elif k[pygame.K_RIGHT]:
		player_angle += 1

	if k[pygame.K_w]:
		pos = (pos[0]+facingy/2, pos[1]+facingx/2)

	elif k[pygame.K_s]:
		pos = (pos[0]-facingy/2, pos[1]-facingx/2)

	if player_angle == -1:
		player_angle = 359

	if player_angle == 360:
		player_angle = 0

	size = 1
	
	for i in range(-45+player_angle, 45+player_angle):
		# add 250 to x coordinate to draw in the middle at 0
		# width should be 90/screen width, 90 deg fov, half of view is 45
		# height should be 250 * distance
		wt = 630/90
		try:
			lri = raycast(i-1, pos)
		except:
			lri = 0

		try:
			nri = raycast(i+1, pos)
		except:
			nri = 0
			
		try:
			ri = raycast(i, pos)
		except:
			ri = 0

		if ri != 0:
			pcolor = (abs(255-ri*1.25), 0, abs(255-ri*1.25))
		
		else:
			pcolor = (255,255,255)
				
		
		corner_threshold = 2

		if ri < nri-corner_threshold or ri < lri-corner_threshold:
			pcolor = (0, 0, 0)
			
			
		pygame.draw.rect(surface, 
						pygame.Color(pcolor),
						pygame.Rect(
							250 + (wt*(i-player_angle)),
							50 + (0.5*ri), #change this
							wt,
							(250 - ri)*size, #change this to be dynamic
						))

		pygame.event.pump()
	
	pygame.display.update()
	
	asyncio.run(frame(1/120))


	
#print(image[511,0])	
