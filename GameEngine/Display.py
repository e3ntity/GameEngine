# Hide pygame message
import sys, os

with open(os.devnull, 'w') as f:
	old_stdout = sys.stdout
	sys.stdout = f
	
	import pygame

	sys.stdout = old_stdout

class GameWindow:
	'''
		Info: The main window object
	'''
	def __init__(self, width, height):
		'''
			Types: number, number ->
		'''

		# Initialise the display
		if not pygame.display.get_init():
			pygame.display.init()

		# Set Dimension
		self.dim = self.width, self.height = width, height

		# Initialise window
		self.flags = 0
		self.window = pygame.display.set_mode(self.dim)

	def destroy(self):
		if pygame.display.get_init():
			pygame.display.quit()

	# Drawing, blit'ting etc.

	def update(self):
		# Show changes
		pygame.display.flip()

	def clear(self):
		self.window.fill((0, 0, 0))

	def blit(self, surface, position):
		self.window.blit(surface, position)

	# Basic getter/setter

	def getWindow(self):
		return self.window

	def setTitle(self, title):
		pygame.display.set_caption(self.title)

	def getTitle(self):
		return pygame.display.get_caption[0]

	def getDim(self):
		return self.dim

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height


class GameScreen:
	'''
		Info: A single screen that can be drawn anywhere on the main window
	'''
	def __init__(self, window, x, y, width, height):
		'''
			Types: GameEngine.GameWindow, number, number, number, number ->
		'''
		
		self.pos = (x, y)
		self.dim = (width, height)

		self.window = window
		self.screen = pygame.Surface(self.dim, flags=pygame.HWSURFACE)

	def clear(self):
		self.screen.fill((0, 0, 0))

	def update(self):
		'''
			Display screen to window
		'''

		self.window.blit(self.screen, self.pos)

	def blit(self, surface, pos):
		'''
			Types: pygame.surface, (number, number) -> boolean
		'''

		out = [False, False]

		if pos[0] + surface.get_width() < self.pos[0] or pos[0] > self.pos[0] + self.dim[0]:
			out[0] = True
		if pos[1] + surface.get_height() < self.pos[1] or pos[1] > self.pos[1] + self.dim[1]:
			out[1] = True

		if out[0] and out[1]:
			return False

		self.screen.blit(surface, (pos[0], pos[1]))

		return True

	# Basic getter/setter

	def getSurface(self):
		return self.screen

	def setPos(self, pos):
		self.pos = pos

	def getPos(self):
		return self.pos

	def setX(self, x):
		self.x = x

	def getX(self):
		return self.pos[0]

	def setY(self, y):
		self.y = y

	def getY(self):
		return self.pos[1]

	def setDim(self, dim):
		self.dim = dim

	def getDim(self):
		return self.dim

	def setWidth(self, widht):
		self.dim[0] = width

	def getWidth(self):
		return self.dim[0]

	def setHeight(self, height):
		self.dim[1] = height

	def getHeight(self):
		return self.dim[1]