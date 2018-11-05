import time

# Hide pygame message
import sys, os

with open(os.devnull, 'w') as f:
	old_stdout = sys.stdout
	sys.stdout = f

	import pygame

	sys.stdout = old_stdout

from GameEngine.Display import GameWindow
from GameEngine.Object import GameObject
from .Constant import *

class GameLogic:
	def __init__(self, gameEngine):
		# Called at the beginning of the game
		# Override with init function for the game
		# gameEngine must remain the only parameter for this function though
		self.gameEngine = gameEngine

		# An array of pygame events such as KEYDOWN, KEYUP etc.
		self.events = []

	def tick(self):
		# Called each tick of the game
		# Override with gamelogic
		pass

	def draw(self):
		# Called each frame of the game
		# Override with everything you want to draw
		pass

	def quit(self):
		# Will be called upon exit event
		# Return True to confirm exit, False to force GameEngine to keep running
		return True


class GameEngine:
	'''
		Info: One GameEngine class to handle them all
	'''
	def __init__(self, gameLogicClass, ticksPerSecond=100, framesPerSecond=30, debug=False):
		'''
			Types: GameEngine.GameLogic, number, number, boolean ->
		'''

		# GameEngine settings
		self.debug = debug
		self.running = False 					# Indicates whether mainloop (shall be) running

		self.gameObjects = {} 					# All the GameObjects indexed
		self.gameLogicClass = gameLogicClass 	# The GameLogic class implementing the game's logic

		self.setTicksPerSecond(ticksPerSecond)
		self.setFramesPerSecond(framesPerSecond)

		# Initialise pygame stuff
		pygame.init()
		pygame.font.init()

	# Modify GameEngine settings

	def setTicksPerSecond(self, ticksPerSecond):
		'''
			Types: number ->
		'''

		self.ticksPerSecond = ticksPerSecond
		self.secondsPerTick = 1/ticksPerSecond

		self.delta = self.secondsPerTick

	def getTicksPerSecond(self):
		return self.ticksPerSecond

	def getSecondsPerTick(self):
		return self.secondsPerTick

	def setFramesPerSecond(self, framesPerSecond):
		self.framesPerSecond = framesPerSecond
		self.secondsPerFrame = 1/framesPerSecond

		self.actualFramesPerSecond = 0.0

	def getFramesPerSecond(self):
		return self.framesPerSecond

	def getSecondsPerFrame(self):
		return self.secondsPerFrame

	def getActualFPS(self):
		return self.actualFramesPerSecond

	def getDelta(self):
		return self.delta

	# GameObjects

	def addGameObject(self, gameObject, index=False):
		# Check index, if no index calculate a new, unique one
		if index == False:
			index = len(self.gameObjects)

			while index in self.gameObjects: index += 1

		# Add GameObject
		self.gameObjects[index] = gameObject

		return index

	def getGameObject(self, index):
		try:
			gameObject = self.gameObjects[index]
		except KeyError:
			return False
		return gameObject

	def delGameObject(self, index):
		try:
			del self.gameObjects[index]
		except KeyError:
			return False
		return True

	# Running GameEngine

	def run(self):
		self.running = True

		# Setup GameLogic
		self.gameLogic = self.gameLogicClass(self)

		try:
			self.mainloop()
		except (KeyboardInterrupt, SystemExit):
			pass

		self.cleanup()

	def cleanup(self):
		pass

	def mainloop(self):
		lastTickTime = -self.secondsPerTick
		lastFrameTime = -self.secondsPerFrame

		lastFPSTime = time.perf_counter()
		fpsFrameCount = 0

		keyPressedEvents = []

		skip = False
		while self.running:
			# Tick
			if time.perf_counter() >= lastTickTime + self.secondsPerTick:
				# Update tick timer
				lastTickTime = time.perf_counter()

				# Evaluate and update events
				if not self.__updateEvents():
					continue

				# Evaluate gamelogic
				self.gameLogic.tick()

			# Draw
			if time.perf_counter() >= lastFrameTime + self.secondsPerFrame:
				# Update fps timer
				lastFrameTime = time.perf_counter()
				
				# Update actualFramesPerSecond
				if time.perf_counter() - lastFPSTime > 1.0:
					self.actualFramesPerSecond = fpsFrameCount/(time.perf_counter() - lastFPSTime)
					lastFPSTime = time.perf_counter()
					fpsFrameCount = 0

				# Draw
				self.gameLogic.draw()

				# Update fps count
				fpsFrameCount += 1

	def __updateEvents(self):
		# Evaluate and update events
		# Returns False to continue in mainloop

		# Initialise keyPressedEvents array
		try:
			self.keyPressedEvents
		except AttributeError:
			self.keyPressedEvents = []

		# Reset event array
		self.gameLogic.events = []

		# Loop over pygame events
		for event in pygame.event.get():
			# Quit Event -> ask gamelogic to quit
			if event.type == QUIT and self.gameLogic.quit():
				self.running = False
				# Don't evaluate GameLogic, draw, etc. but quit directly
				return False
			else:
				# Add all other events to the GameLogic events array
				self.gameLogic.events.append(event)

				# Create KEYPRESSED events
				if event.type == KEYDOWN:
					# Add KEYPRESSED event to keyPressedEvents
					eventKP = pygame.event.Event(KEYPRESSED, {"key": event.key})

					if not eventKP in self.keyPressedEvents:
						self.keyPressedEvents.append(eventKP)
				elif event.type == KEYUP:
					# Remove KEYPRESSED event to keyPressedEvents
					for e in self.keyPressedEvents:
						if e.key == event.key:
							self.keyPressedEvents.remove(e)
							break
		
		# Add KEYPRESSED events to the GameLogic events array	
		for event in self.keyPressedEvents:
			self.gameLogic.events.append(event)

		# Don't continue
		return True

	# Getter/setter

	def setCamera(self, camera):
		self.camera = camera

	def getCamera(self):
		return self.camera