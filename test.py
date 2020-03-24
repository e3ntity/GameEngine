#!/usr/bin/python3

import numpy

import GameEngine

from GameEngine.Object import Object3D as Object3D
from GameEngine.Text import Text as Text

class GameLogicOverride(GameEngine.GameLogic):
	def __init__(self, gameEngine):
		super().__init__(gameEngine)

		self.window = GameEngine.GameWindow(1600, 800)

		# Initialise cameras

		self.cameras = []

		screen0 = GameEngine.GameScreen(self.window, 0, 0, 800, 800)
		screen1 = GameEngine.GameScreen(self.window, 800, 0, 800, 800)

		self.cameras.append(GameEngine.GameCamera(screen0, (0, 0, -20)))
		self.cameras.append(GameEngine.GameCamera(screen1, (0, 0, -20), 120))

		for i, cam in enumerate(self.cameras):
			cam.setName("Cam{:}".format(i))

		self.activeCamera = self.cameras[0]

		# Initialise GameObjects

		self.cube = Object3D.Cube((0, 0, 0), (10, 10, 10))

		self.change = 100

	def tick(self):
		# Detect collision

		self.handleKeyInputs()

	def handleKeyInputs(self):
		shift = False
		for event in self.events:
			if event.type == GameEngine.KEYPRESSED:
				if event.key == GameEngine.K_LSHIFT:
					shift = True

		for event in self.events:
			if event.type == GameEngine.KEYPRESSED:
				if shift:
					if event.key == GameEngine.K_a:
						self.activeCamera.addX(-self.change * self.gameEngine.getDelta())
					elif event.key == GameEngine.K_d:
						self.activeCamera.addX(self.change * self.gameEngine.getDelta())
					elif event.key == GameEngine.K_w:
						self.activeCamera.addY(-self.change * self.gameEngine.getDelta())
					elif event.key == GameEngine.K_s:
						self.activeCamera.addY(self.change * self.gameEngine.getDelta())
					elif event.key == GameEngine.K_f:
						self.activeCamera.addZ(-self.change * self.gameEngine.getDelta())
					elif event.key == GameEngine.K_r:
						self.activeCamera.addZ(self.change * self.gameEngine.getDelta())
				else:
					if event.key == GameEngine.K_a:
						self.cube.addDim((-self.change * self.gameEngine.getDelta(), 0, 0))
					elif event.key == GameEngine.K_d:
						self.cube.addDim((self.change * self.gameEngine.getDelta(), 0, 0))
					elif event.key == GameEngine.K_w:
						self.cube.addDim((0, self.change * -self.gameEngine.getDelta(), 0))
					elif event.key == GameEngine.K_s:
						self.cube.addDim((0, self.change * self.gameEngine.getDelta(), 0))
					elif event.key == GameEngine.K_f:
						self.cube.addDim((0, 0, -self.change * self.gameEngine.getDelta()))
					elif event.key == GameEngine.K_r:
						self.cube.addDim((0, 0, self.change * self.gameEngine.getDelta()))

					elif event.key == GameEngine.K_UP:
						self.cube.addPos((0, -self.change * self.gameEngine.getDelta(), 0))
					elif event.key == GameEngine.K_DOWN:
						self.cube.addPos((0, self.change * self.gameEngine.getDelta(), 0))
					elif event.key == GameEngine.K_LEFT:
						self.cube.addPos((-self.change * self.gameEngine.getDelta(), 0, 0))
					elif event.key == GameEngine.K_RIGHT:
						self.cube.addPos((self.change * self.gameEngine.getDelta(), 0, 0))
			elif event.type == GameEngine.KEYDOWN:
				if shift: pass
				else:
					if event.key == GameEngine.K_p:
						self.activeCamera.debug = not self.activeCamera.debug

			elif event.type == GameEngine.MOUSEBUTTONDOWN:
				for camera in self.cameras:
					screen = camera.getScreen()
					if (event.pos[0] > screen.getX()
					and event.pos[0] < screen.getX() + screen.getWidth()
					and event.pos[1] > screen.getY()
					and event.pos[1] < screen.getY() + screen.getHeight()):
						self.activeCamera = camera
						break


	def draw(self):
		self.window.clear()

		for camera in self.cameras:
			camera.clear()

		counts = [0, 0]

		for i, camera in enumerate(self.cameras):
			counts[i] += camera.drawMesh(self.cube, width=0 if i in [0] else 1, hideInvisible=True, antialias=True)

		#print("Triangles: Cam0 -> {}, Cam1 -> {}".format(counts[0], counts[1]))

		for camera in self.cameras:
			camera.update()

		# Draw FPS
		color = (255, 255, 255)
		setFPS = self.gameEngine.getFramesPerSecond()
		if setFPS - setFPS * 0.1 > self.gameEngine.getActualFPS():
			color = (255, 0, 0)
		fps = Text.text("{}".format(int(numpy.round(self.gameEngine.getActualFPS()))), "Arial", 48, color=color)

		self.window.blit(fps, (self.window.getWidth() - fps.get_width(), 0))
		
		self.window.update()

	def quit(self):
		print("Bye")

		return True

def main():
	game = GameEngine.GameEngine(GameLogicOverride, framesPerSecond=30)

	game.run()

main()