import pygame as pg
from pygame.locals import *
import os
from random import randint

class Player:
	def __init__(self, x=0, y=0, level=1, enemy=False, img=None, effect=None):
		self.x = x
		self.y = y
		self.vel_x = 0
		self.vel_y = 0
		self.enemy = enemy
		self.level = level
		self.hp = 50 * self.level
		scale = 0
		try:
			if not enemy:
				scale = 20
				self.image = pg.image.load(os.path.join("data","plane"+str(self.level)+".png"))
				self.effect = pg.mixer.Sound(os.path.join("data","shoot.ogg")) 
			else:
				scale = 10
				self.image = img
				self.effect = effect
				self.vel_y = 2 * (self.level-2)
		except:
			raise UserWarning("Cannot load required files!")
		self.width = self.image.get_size()[0] // scale
		self.height = self.image.get_size()[1] // scale
		self.image = pg.transform.smoothscale(self.image, (self.width, self.height))

	def set_pos(self, x, y):
		self.x = x
		self.y = y

	def move(self, direction):
		if direction == "LEFT":
			self.vel_x = -5*self.level
		elif direction == "RIGHT":
			self.vel_x = 5*self.level
		else:
			self.vel_x = 0

	def displayHP(self, surface):
		w = self.hp / (50 * self.level) * self.width
		h = 2
		pg.draw.rect(surface, (0, 255, 0), pg.Rect(self.x, self.y - h * 2, w, h))


	def shoot(self, vel, scale, img, audio):
		result = []
		if self.level == 1 or self.enemy:
			missile = Shoot(img=img, audio=audio, vel_y=vel, scale=scale)
			missile.x = self.x + self.width / 2 - missile.width / 2
			if not self.enemy:
				missile.y = self.y - missile.height
			else:
				missile.y = self.y + self.height 
			result.append(missile)
		elif self.level == 2 and not self.enemy:
			missile_1 = Shoot(img = img, audio=audio, vel_y=vel, scale=scale)
			missile_2 = Shoot(img = img, audio=audio, vel_y=vel, scale=scale)
			missile_1.x = self.x + self.width / 4 - missile_1.width / 2
			missile_2.x = self.x + self.width * 3 / 4 - missile_2.width / 2
			missile_1.y = self.y - missile_1.height
			missile_2.y = self.y - missile_2.height
			result.append(missile_1)
			result.append(missile_2)
		elif self.level == 3 and not self.enemy:
			missile_1 = Shoot(img = img, audio=audio, vel_y=vel, scale=scale)
			missile_2 = Shoot(img = img, audio=audio, vel_y=vel, scale=scale)
			missile_3 = Shoot(img = img, audio=audio, vel_y=vel, scale=scale)
			missile_4 = Shoot(img = img, audio=audio, vel_y=vel, scale=scale)

			missile_1.x = self.x + self.width * 2 / 8 - missile_1.width / 2
			missile_2.x = self.x + self.width * 3 / 8 - missile_2.width / 2
			missile_3.x = self.x + self.width * 5 / 8 - missile_3.width / 2
			missile_4.x = self.x + self.width * 6 / 8 - missile_4.width / 2
			missile_1.y = self.y
			missile_2.y = self.y - missile_2.height
			missile_3.y = self.y - missile_3.height
			missile_4.y = self.y
			result.append(missile_1)
			result.append(missile_2)
			result.append(missile_3)
			result.append(missile_4)
		return result

class Shoot:
	def __init__(self, img, audio, x=0, y=0, vel_y=0, scale=10):
		self.x = x
		self.y = y
		self.vel_y = vel_y
		self.remove = False
		self.image = img
		self.boom = audio
		self.width = self.image.get_size()[0] // scale
		self.height = self.image.get_size()[1] // scale
		self.image = pg.transform.smoothscale(self.image, (self.width, self.height))

class Power:
	def __init__(self, x, y):
		try:
			self.image = pg.image.load(os.path.join("data","oil.png"))
			self.effect = pg.mixer.Sound(os.path.join("data","spring.wav"))
		except:
			raise UserWarning("Cannot load required files!")
		self.width = self.image.get_size()[0] // 20
		self.height = self.image.get_size()[1] // 20
		self.x = randint(0, x-self.width)
		self.y = randint(0, y-self.height)
		self.image = pg.transform.smoothscale(self.image, (self.width, self.height))
		self.power = randint(0, 30)
		self.score = randint(0, 200)


class App:
	def __init__(self, width=525, height=323, fps=30):
		#initialize pygame, window, background, font...
		pg.mixer.pre_init(44100, -16, 2, 2048)
		pg.init()
		#pg.display.set_caption("Press ESC to quit")
		folder = "data"
		try:
			bgpic = pg.image.load(os.path.join(folder, "background.jpg"))
			pg.mixer.music.load(os.path.join(folder, "bg.mp3"))
			self.levelup = pg.mixer.Sound(os.path.join(folder, "wormhole.ogg"))
			boom = pg.image.load(os.path.join(folder, "boom.png"))
			self.missile = pg.image.load(os.path.join(folder, "missile.png"))
			self.missile_effect = pg.mixer.Sound(os.path.join(folder, "explode.ogg"))
			self.nuclear = pg.image.load(os.path.join(folder, "nuclear.png"))
			self.nuclear_effect = pg.mixer.Sound(os.path.join(folder, "boom.wav"))
			self.alien = pg.image.load(os.path.join(folder, "alien.png"))
			self.alien_effect = pg.mixer.Sound(os.path.join(folder, "beep.ogg"))
		except:
			raise UserWarning("Error loading required files!")
		pg.mixer.music.play(-1)
		self.width = width
		self.height = height
		self.screen = pg.display.set_mode((self.width, self.height), pg.HWSURFACE|pg.DOUBLEBUF)
		bgpic = pg.transform.smoothscale(bgpic,(self.width, self.height))
		sizes = boom.get_size()
		boom = pg.transform.smoothscale(boom, (sizes[0]//10, sizes[1]//10))
		self.background = bgpic
		self.background = self.background.convert()
		self.boom = boom
		#self.boom = self.boom.convert()
		self.clock = pg.time.Clock()
		self.fps = fps
		self.playtime = 0.0
		self.font = pg.font.SysFont('mono',20,bold=True)
		
	def run(self):
		running = True
		startGame = False
		mouseMode = False
		gameover = False
		shooting = []
		enemies = []
		nuclear = []
		countdown = 5
		score = 0
		level = 1
		oil = None
		while running:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = False
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						running = False
					elif event.key == pg.K_SPACE and startGame == False:
						self.width = 400
						self.height = 500
						self.screen = pg.display.set_mode((self.width, self.height), pg.HWSURFACE|pg.DOUBLEBUF)
						gameover = False
						startGame = True
						countdown = 5
						score = 0
						level = 1
						shooting.clear()
						enemies.clear()
						nuclear.clear()
						oil = None
						self.background = pg.Surface(self.screen.get_size())
						p = Player(level=level)
						p.set_pos(self.width/2-p.width/2, self.height-p.height-5)
						p.image = p.image.convert()
					elif event.key == pg.K_UP and startGame == True and mouseMode == False:
						p.effect.play()
						shooting.extend(p.shoot(-2*p.level, 50, self.missile, self.missile_effect))
					elif event.key == pg.K_LEFT and startGame == True and mouseMode == False:
						p.move("LEFT")
					elif event.key == pg.K_RIGHT and startGame == True and mouseMode == False:
						p.move("RIGHT")
					elif event.key == pg.K_m and startGame == True:
						mouseMode = not mouseMode
				elif event.type == pg.KEYUP:
					pressed = pg.key.get_pressed()
					if event.key == pg.K_LEFT and startGame == True and mouseMode == False:
						if not pressed[pg.K_RIGHT]:
							p.move("STOP")
					elif event.key == pg.K_RIGHT and startGame == True and mouseMode == False:
						if not pressed[pg.K_LEFT]:
							p.move("STOP")
				elif event.type == pg.MOUSEBUTTONDOWN:
					if mouseMode and startGame:
						p.effect.play()
						shooting.extend(p.shoot(-2*p.level, 50, self.missile, self.missile_effect))
			ms = self.clock.tick(self.fps)
			self.playtime += ms / 1000.0
			pg.display.set_caption("Enjoy the shooting!")
			if gameover:
				self.write_instructions("GAME OVER!|Program terminating in {} seconds!|Press SPACE to restart!".format(countdown))
				pg.time.delay(1000)
				countdown -= 1
				if countdown == -1:
					running = False
			elif startGame == False:
				self.write_instructions("Press SPACE to start game!|Use left and right to control the plane!|Press up to fire!")
			else:
				text = "Level: {}  Score: {} HP: {}".format(level, score, p.hp)
				pg.display.set_caption(text)
				#power!
				if oil == None:
					val = randint(0,50)
					if randint(0,50) == val:
						oil = Power(self.width, self.height-p.height)
				#adding enemy
				if len(enemies) <= 5*level:
					val = randint(0, 60//level)
					if randint(0,60//level) == val:
						alien = Player(level=level+2, enemy=True, img=self.alien, effect=self.alien_effect)
						x = randint(0, self.width-alien.width)
						reset = True
						while reset:
							count = 0
							for e in enemies:
								rect_1 = pg.Rect(x, 0, alien.width, alien.height)
								rect_2 = pg.Rect(e.x, e.y, e.width, e.height)
								if rect_1.colliderect(rect_2):
									x = randint(0, self.width-alien.width)
								else:
									count += 1
							if count == len(enemies):
								reset = False
						alien.set_pos(x, 0)
						alien.image = alien.image.convert()
						enemies.append(alien)
				#dynamic background
				self.background.fill((255,255,255))
				for i in range(500):
					x = randint(0, self.width)
					y = randint(0, self.height)
					self.background.set_at((x,y), (0,0,0))
				self.background = self.background.convert()
				#player
				if not mouseMode:	
					p.x += p.vel_x
					if p.x <= 0:
						p.x = 0
					elif p.x >= self.width-p.width:
						p.x = self.width-p.width
				else:
					pos = pg.mouse.get_pos()
					x = pos[0]
					if x <= 0:
						p.x = 0
					elif x >= self.width-p.width:
						p.x = self.width-p.width
					else:
						p.x = x
				self.screen.blit(p.image,(p.x,p.y))

				#display enemy
				temp = []
				for e in enemies:
					self.screen.blit(e.image, (e.x, e.y))
					rand_fire = randint(0, 200)
					fire = randint(0, 200)
					if rand_fire == fire:
						nuclear.extend(e.shoot(3*level, 10, self.nuclear, self.nuclear_effect))
						e.effect.play()
					#enemy player collision
					if e.y <= self.height - e.height / 2:
						rect_1 = pg.Rect(e.x, e.y, e.width, e.height)
						rect_2 = pg.Rect(p.x, p.y, p.width, p.height)
						if rect_1.colliderect(rect_2):
							e.hp = 0
							p.hp -= 50

						if e.hp > 0:
							temp.append(e)
					else:
						p.hp -= 0.5
					
					if p.hp <= 0:
						gameover = True
						self.background.fill((0,0,0))
						self.background = self.background.convert()
						startGame = False
						size = self.boom.get_size()
						self.screen.blit(self.boom, (p.x+p.width/2-size[0]/2, p.y+p.height/2-size[1]/2))
					e.displayHP(self.screen)
					e.y += e.vel_y
				del enemies[:]
				enemies = temp

				
				for m in shooting:
					if m.remove == True:
						continue
					rect_1 = pg.Rect(m.x, m.y, m.width, m.height)
					#missile power collision causes player hp increase
					if oil != None:
						rect_2 = pg.Rect(oil.x, oil.y, oil.width, oil.height)
						if rect_1.colliderect(rect_2):
							p.hp += oil.power
							score += oil.score
							if p.hp >= p.level * 50:
								p.hp = p.level * 50
							oil.effect.play()
							oil = None
							m.remove = True
							continue
					#missile nuclear collision
					for n in nuclear:
						if n.remove == True:
							continue
						rect_2 = pg.Rect(n.x, n.y, n.width, n.height)
						if rect_1.colliderect(rect_2):
							score += 1*level
							n.boom.play()
							m.remove = True
							n.remove = True
						#nuclear power collision causes explosion
						if oil != None:
							rect_3 = pg.Rect(oil.x, oil.y, oil.width, oil.height)
							if rect_2.colliderect(rect_3):
								n.boom.play()
								oil = None
								n.remove = True
						#nuclear player collision
						rect_3 = pg.Rect(p.x, p.y, p.width, p.height)
						if rect_2.colliderect(rect_3):
							n.boom.play()
							n.remove = True
							p.hp -= 50

							if p.hp <= 0:
								gameover = True
								self.background.fill((0,0,0))
								self.background = self.background.convert()
								startGame = False
								size = self.boom.get_size()
								self.screen.blit(self.boom, (p.x+p.width/2-size[0]/2, p.y+p.height/2-size[1]/2))
					temp = []
					for e in enemies:
						rect_2 = pg.Rect(e.x, e.y, e.width, e.height)
						#alien power collision
						if oil is not None:
							rect_3 = pg.Rect(oil.x, oil.y, oil.width, oil.height)
							if rect_2.colliderect(rect_3):
								e.hp += oil.power
								if e.hp >= e.level * 50:
									e.hp = e.level * 50
								oil.effect.play()
								oil = None
						#missile alien collision
						if rect_1.colliderect(rect_2):
							score += 4 * level
							m.boom.play()
							m.remove = True
							e.hp -= 50
						if e.hp > 0:
							temp.append(e)
						else:
							size = self.boom.get_size()
							self.screen.blit(self.boom, (e.x+e.width/2-size[0]/2, e.y+e.height/2-size[1]/2))
					del enemies[:]
					enemies = temp
					


				#display missiles
				temp = []
				for m in shooting:
					if m.remove:
						continue
					m.y += m.vel_y
					if m.y <= 0:
						m.remove = True
					else:
						self.screen.blit(m.image, (m.x, m.y))
						temp.append(m)
				del shooting[:]
				shooting = temp
				#display nuclear
				temp = []
				for n in nuclear:
					if n.remove:
						continue
					n.y += n.vel_y
					if n.y <= 0:
						n.remove = True
					else:
						self.screen.blit(n.image, (n.x, n.y))
						temp.append(n)
				del nuclear[:]
				nuclear = temp
				if oil != None:
					self.screen.blit(oil.image, (oil.x, oil.y))
				p.displayHP(self.screen)

			if score >= 600 and score < 3000 and p.level == 1:
				level = 2
				temp_x = p.x + p.width / 2
				p = Player(level = level)
				p.set_pos(temp_x-p.width/2, self.height-p.height-5)
				for e in enemies:
					size = self.boom.get_size()
					self.screen.blit(self.boom, (e.x+e.width/2-size[0]/2, e.y+e.height/2-size[1]/2))
				enemies.clear()
				shooting.clear()
				nuclear.clear()
				self.levelup.play()
				
			elif score >= 3000 and p.level == 2:
				level = 3
				temp_x = p.x
				temp_x = p.x + p.width / 2
				p = Player(level = level)
				p.set_pos(temp_x-p.width/2, self.height-p.height-5)
				for e in enemies:
					size = self.boom.get_size()
					self.screen.blit(self.boom, (e.x+e.width/2-size[0]/2, e.y+e.height/2-size[1]/2))
				enemies.clear()
				shooting.clear()
				nuclear.clear()
				self.levelup.play()

			pg.display.flip()
			self.screen.blit(self.background, (0, 0))

		pg.quit()

	def write_instructions(self, text):
		texts = text.split("|")
		y = 0
		for t in texts:
			fw, fh = self.font.size(t)
			surface = self.font.render(t, True, (0,255,0))
			if y == 0:
				y = (self.height - fh) // 2
			else:
				y += fh
			self.screen.blit(surface,((self.width-fw) // 2, y))


if __name__ == "__main__":
	app = App()
	app.run()