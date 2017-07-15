import pygame, sys
from pygame.locals import *
from unit import user, enemy
import random

#constant initialize
FPS = 60
BLOCK_SIZE = 24
WIDTH = 29
HEIGHT = 15
WINDOW_WIDTH = WIDTH * BLOCK_SIZE
WINDOW_HEIGHT = HEIGHT * BLOCK_SIZE
MAP_NAME = "./material/map.maze"
BGM_NAME = "./material/bgm.ogg"
BLOCK_IMAGE = "./material/block.png"
FOOD_IMAGE = "./material/food.png"
GAMEOVER_IMAGE = "./material/gameover.png"
SERVER_PORT = 30000
ENEMY_COUNT = 4
OX = 1
OY = 1
DELAY = 8

#pygame initialize
pygame.init()
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
block_image = pygame.image.load(BLOCK_IMAGE)
food_image = pygame.image.load(FOOD_IMAGE)
gameover_image = pygame.image.load(GAMEOVER_IMAGE)
bgm = pygame.mixer.music.load(BGM_NAME)
scene = "game"
unit_list = []
game_map = []

#map initialize
def load_map(filename):
	global game_map
	game_map.clear()
	file = open(filename, 'r')
	for line in file.readlines():
		game_map.append(list(line.strip()))
		pass
	pass

#set passport
def through(position):
	x = position[0]
	y = position[1]
	in_range = (x >= 0 and x < WIDTH) and (y >= 0 and y < HEIGHT)
	in_space = (not game_map[y][x] == '1')
	return (in_range and in_space)
	pass

#gameover?
def check_gameover(user_pos, enemy_pos):
	global scene
	gameover = (enemy_pos[0] == user_pos[0] and enemy_pos[1] == user_pos[1])
	if gameover:
		scene = "gameover"
		pass
	return gameover
	pass

#gameover
def gameover():
	pygame.mixer.music.stop()
	keys = pygame.key.get_pressed()
	if keys[K_RETURN]:
		initialize()
		pass
	display.fill((0, 0, 0))
	x = (WINDOW_WIDTH-gameover_image.get_width())/2
	y = (WINDOW_HEIGHT-gameover_image.get_height())/2
	display.blit(gameover_image, (x, y))
	pygame.display.update()
	pass

#unit initialize
def initialize_unit():
	unit_list.clear()
	ox = random.randint(1, WIDTH - 2)
	oy = random.randint(1, HEIGHT - 2)
	while not through((ox, oy)):
		ox = random.randint(1, WIDTH - 2)
		oy = random.randint(1, HEIGHT - 2)
	unit_list.append(user(OX, OY))
	for i in range(0, ENEMY_COUNT):
		enemy_color = i % 4
		ox = random.randint(1, WIDTH - 2)
		oy = random.randint(1, HEIGHT - 2)
		while not through((ox, oy)):
			ox = random.randint(1, WIDTH - 2)
			oy = random.randint(1, HEIGHT - 2)
		unit_list.append(enemy(enemy_color, ox, oy))
		pass
	pass

#initialize
def initialize():
	global scene
	load_map(MAP_NAME)
	initialize_unit()
	scene = "game"
	pygame.mixer.music.play(-1)

#system update
def system_update():
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	pass

#update control
control_clock = [0, DELAY]
def control_update():
	#user control
	if control_clock[0] > control_clock[1]:
		user = unit_list[0]
		keys = pygame.key.get_pressed()
		passport = False
		pos = user.position
		if keys[K_UP]: 
			pos = user.move(through(user.next(0)))
		elif keys[K_RIGHT]: 
			pos = user.move(through(user.next(1)))
		elif keys[K_DOWN]:
			pos = user.move(through(user.next(2)))
		elif keys[K_LEFT]:
			pos = user.move(through(user.next(3)))
			pass
		game_map[pos[1]][pos[0]] = '0'
		#enemy control
		u_pos = unit_list[0].position
		for index in range(1, len(unit_list)):
			enemy = unit_list[index]
			if check_gameover(u_pos, enemy.position): break
			enemy.track(u_pos)
			passport = through(enemy.next())
			enemy.move(passport)
			while not passport:
				enemy.clockwise()
				passport = through(enemy.next())
				enemy.move(passport)
			pass
		control_clock[0] = 0
		pass
	else:
		control_clock[0] += 1
		pass
	pass

#update screen
def screen_update():
	display.fill((0, 0, 0))
	for i in range(0, HEIGHT):
		for j in range(0, WIDTH):
			x = j * BLOCK_SIZE
			y = i * BLOCK_SIZE
			if game_map[i][j] == '1':
				display.blit(block_image, (x, y))
			elif game_map[i][j] == '4':
				display.blit(food_image, (x, y))
				pass
			pass
		pass
	for unit in unit_list:
		unit.update()
		x = unit.position[0] * BLOCK_SIZE
		y = unit.position[1] * BLOCK_SIZE
		display.blit(unit.image, (x, y), unit.image_rect())
	pygame.display.update()
	pass

#first
initialize()

#main loop
while True:
	system_update()
	if scene == "game":
		control_update()
		screen_update()
	else:
		gameover()
		pass
	pass