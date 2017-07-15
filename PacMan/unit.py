import pygame
import math
import random

USER_IMAGE = "./material/user.png"
ENEMY_IMAGE = [("./material/enemy%d.png" % i) for i in range(1, 5)]

class unit():
	def __init__(self, filename):
		super(unit, self).__init__()
		self.image = pygame.image.load(filename)
		self.clock = [0, 5]
		self.direction = 0
		self.position = [1, 1, 1, 1]
		self.index = 0
		self.source_rect = 0
		pass

	def update(self):
		self.animation_update()
		pass

	def animation_update(self):
		self.clock[0] += 1
		if self.clock[0] > self.clock[1]:
			if self.index < 4:
				self.index += 4
			else:
				self.index -= 4
			self.source_rect = self.image_rect()
			self.clock[0] = 0
			pass
		pass

	def move(self, passport):
		if passport:
			pos = self.position[:]
			self.position[0] = self.position[2]
			self.position[1] = self.position[3]
		else:
			self.position[2] = self.position[0]
			self.position[3] = self.position[1]
			pos = self.position
			pass
		return pos
		pass

	def next(self):
		self.ahead()
		return (self.position[2], self.position[3])
		pass

	def turn(self, direction):
		self.direction = direction % 4
		self.index = self.direction
		pass

	def ahead(self):
		if self.direction == 0:
			self.position[3] -= 1
		elif self.direction == 1:
			self.position[2] += 1
		elif self.direction == 2:
			self.position[3] += 1
		elif self.direction  == 3:
			self.position[2] -= 1
		pass

	def image_rect(self):
		w = self.image.get_width()
		h = self.image.get_height()
		ox = math.floor(w / 4 * (self.index % 4)) 
		oy = math.floor(h / 2 * math.floor(self.index / 4))
		return pygame.Rect((ox, oy), (24, 24))

class user(unit):
	def __init__(self, x, y):
		super(user, self).__init__(USER_IMAGE)
		self.position = [x, y, x, y]
		pass

	def next(self, direction):
		self.turn(direction)
		self.ahead()
		return (self.position[2], self.position[3])
		pass

class enemy(unit):
	def __init__(self, id, x, y):
		filename = ENEMY_IMAGE[id]
		super(enemy, self).__init__(filename)
		self.position = [x, y, x, y]
		pass

	def track(self, user_pos):
		rand_dir = [1,2,3,4]
		self.turn(random.choice(rand_dir))
		pass

	def clockwise(self):
		self.turn(self.direction + 1)
		pass

class enemy_user(unit):
	def __init__(self, x, y):
		filename = ENEMY_IMAGE[0]
		super(enemy_user, self).__init__(filename)
		self.position = [x, y, x, y]
		pass

	def move(self, x, y):
		self.position[0] = x
		self.position[1] = y
		pass