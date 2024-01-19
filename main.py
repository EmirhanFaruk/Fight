
# Modification date: Wed Feb  9 16:45:26 2022

# Production date: Sun Sep  3 15:42:51 2023

import pygame
from random import randint, choice
from math import sqrt


ww = 600
wh = 600
win = pygame.display.set_mode((ww, wh))
pygame.init()


class Human:
	def __init__(self, x, y, team):
		self.x = x
		self.y = y
		self.team = team
		if self.team == "blue":
			self.tc = (0, 0, 255)
		elif self.team == "red":
			self.tc = (255, 0, 0)
		self.dahp = randint(50, 300)
		self.hp = self.dahp
		self.maxhp = self.dahp
		self.hc = [0, 255, 0]
		self.color = randint(0, 150)
		self.skin = (45 + self.color, 34 + self.color, 30 + self.color)
		self.vel = randint(3, 7)
		self.walkvel = self.vel - 2
		self.dmg = randint(1, 10)
		self.direction = "right"
		self.tdir = "right"
		self.directions = ["right", "left", "up", "down"]
		self.cd = True
		self.target = None
	
	
	def distance(self, sh):
		return sqrt(((sh.x + 8) - (self.x + 8)) ** 2 + ((sh.y + 8) - (self.y + 8)) ** 2)
	
	def ctarget(self, humans):
		dhs = []
		for human in humans:
			if self != human and human.team != self.team:
				dhs.append([self.distance(human), human])
		if len(dhs) > 0:
			closest = 0
			for couple in range(len(dhs)):
				if dhs[closest][0] > dhs[couple][0]:
					closest = couple
			self.target = dhs[closest][1]
		else:
			self.target = None
		
	
	def mover(self):
		if self.x < 0 or self.x > ww or self.y < 0 or self.y > wh:
				self.x = randint(0, ww)
				self.y = randint(0, wh)
		if self.target and self.distance(self.target) > 32:
			if self.target.x >= self.x + 8:
				self.x += self.vel
				self.direction = "right"
				return
			if self.target.x + 16 <= self.x + 8:
				self.x -= self.vel
				self.direction = "left"
				return
			if self.target.y >= self.y + 8:
				self.y += self.vel
				self.direction = "down"
				return
			if self.target.y + 16 <= self.y + 8:
				self.y -= self.vel
				self.direction = "up"
				return
		elif self.target and self.distance(self.target) < 32:
			self.target.hp -= self.dmg
			pygame.draw.rect(win, (self.dmg * 20, 100, 100), pygame.Rect(self.target.x, self.target.y - 8, 8, 8))
			return #attack
		if randint(0, 300) == 1 or self.cd:
			self.tdir = self.direction
			self.directions.remove(self.direction)
			self.direction = choice(self.directions)
			self.directions.append(self.tdir)
			self.tdir = self.direction
			self.cd = False
		else:
			if self.direction == "right" and self.x < ww - 16:
				self.x += self.walkvel
			elif self.direction == "right":
				self.cd = True
			if self.direction == "left" and self.x > 0:
				self.x -= self.walkvel
			elif self.direction == "left":
				self.cd = True
			if self.direction == "up" and self.y > 0:
				self.y -= self.walkvel
			elif self.direction == "up":
				self.cd = True
			if self.direction == "down" and self.y < wh - 16:
				self.y += self.walkvel
			elif self.direction == "down":
				self.cd = True
			
	
	
	def draw(self, win):
		if self.hp == 0:
			self.hp = -1
		self.hc = [int(abs(((self.maxhp / self.hp) * 255) - 255)), int(abs((self.hp / self.maxhp) * 255)), 0]
		for colour in self.hc:
			if colour > 254:
				colour = 255
		if self.hc[0] > 255:
			self.hc[0] = 255
		self.hc = tuple(self.hc)

		self.hpbl = int(abs(self.hp / self.maxhp) * 24)
			
		if self.direction == "right" or self.direction == "left":
			#pygame.draw.rect(win, (30, 20, 170), pygame.Rect(self.x + 4, self.y - 8, 8, 8))
			#pygame.draw.rect(win, (30, 20, 170), pygame.Rect(self.x + 4, self.y + 16, 8, 8))
			pygame.draw.rect(win, self.tc, pygame.Rect(self.x + 4, self.y - 8, 8, 8))
			pygame.draw.rect(win, self.tc, pygame.Rect(self.x + 4, self.y + 16, 8, 8))
			pygame.draw.rect(win, self.skin, pygame.Rect(self.x, self.y, 16, 16))
			#print(self.hc)
			pygame.draw.rect(win, self.hc, pygame.Rect(self.x - 8, self.y - 8, self.hpbl, 4))
		if self.direction == "up" or self.direction == "down":
			#pygame.draw.rect(win, (30, 20, 170), pygame.Rect(self.x - 8, self.y + 4, 8, 8))
			#pygame.draw.rect(win, (30, 20, 170), pygame.Rect(self.x + 16, self.y + 4, 8, 8))
			pygame.draw.rect(win, self.tc, pygame.Rect(self.x - 8, self.y + 4, 8, 8))
			pygame.draw.rect(win, self.tc, pygame.Rect(self.x + 16, self.y + 4, 8, 8))
			pygame.draw.rect(win, self.skin, pygame.Rect(self.x, self.y, 16, 16))
			pygame.draw.rect(win, self.hc, pygame.Rect(self.x - 8, self.y - 8, self.hpbl, 4))
		self.hc = list(self.hc)

		



humans = []
for i in range(100):
	dax = randint(0, ww - 16)
	day = randint(0, wh - 16)
	if i % 2 == 0:
		humans.append(Human(dax, day, "red"))
	else:
		humans.append(Human(dax, day, "blue"))		



clock = pygame.time.Clock()
running = True
while running:
	clock.tick(20)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
			break
	if not running:
		break
	win.fill((150, 200, 70))
	
	
	
	for human in humans:
		if human.hp <= 0:
			humans.remove(human)
			continue
		human.ctarget(humans)
	for human in humans:
		human.mover()
		human.draw(win)
	
	
	pygame.draw.rect(win, (0, 0, 0), pygame.Rect(0, 0, ww, wh), 2)
	pygame.display.flip()

