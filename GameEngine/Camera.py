# Hide pygame message
import sys, os

with open(os.devnull, 'w') as f:
	old_stdout = sys.stdout
	sys.stdout = f
	
	import pygame

	sys.stdout = old_stdout

import numpy

from .Display import GameScreen as GameScreen
from .Object.Object3D import Mesh as Mesh
from .Object.Object3D import Triangle as Triangle
from .Object.Object3D import Vec3D as Vec3D
from .Text import Text as Text

class GameCamera:
	def __init__(self, screen, pos=(0, 0, 0), fov=90.0, debug=False):
		'''
			Types: GameScreen, (number, number, number), float, boolean ->
		'''

		self.debug = debug
		self.screen = screen

		self.name = "" # Can be set later for debug etc.

		# GameCamera settings

		self.pos = pos
		self.setFOV(fov)

		self.aspectRatio = self.screen.getHeight()/self.screen.getWidth()

	def drawMesh(self, mesh, antialias=False, hideInvisible=True, color=(255, 255, 255), width=1):
		'''
			Types: Mesh, boolean, (number, number, number), number -> number
		'''

		count = 0
		for triangle in mesh.getTriangles().values():
			if self.drawTriangle(triangle, antialias=antialias, hideInvisible=hideInvisible, color=color, width=width):
				count += 1

		return count

	def drawTriangle(self, triangle, antialias=False, hideInvisible=True, color=(255, 255, 255), width=1):
		'''
			Types: Triangle, boolean, (number, number, number), number, (number, number, number) -> number
		'''

		if hideInvisible:
			normVec = triangle.getNormalVector()
			camVec = Vec3D(self.pos)
			diffVec = Vec3D.sub(triangle.getVectors()[1], camVec)

			if Vec3D.dotProduct(normVec, diffVec) > 0:
				return False

		if self.debug:
			self.lastTriangleHI = hideInvisible

		vectors = triangle.getVectors()
		pointlist = []

		for vec in vectors:
			pointlist.append(self.__projectPoint(vec))

		if antialias and width > 0:
			pygame.draw.aalines(self.screen.getSurface(), color, True, pointlist, False)
		else:
			pygame.draw.polygon(self.screen.getSurface(), color, pointlist, width)
			if self.debug:
				pygame.draw.polygon(self.screen.getSurface(), (255, 0, 0), pointlist, 1)

		return True

	def drawLine(self, start, end, color=(255, 255, 255), width=1):
		'''
			Types: Vec3D, Vec3D, (number, number, number), number -> boolean
		'''

		points = [start, end]

		# Check that line is in camera's view
		if not (self.__checkVisible(points[0]) or self.__checkVisible(points[1])):
			return False

		# Translate line to camera's view
		for i in range(2):
			points[i] = self.__projectPoint(points[i])

		pygame.draw.line(self.screen.getSurface(), color, points[0], points[1], width)

		return True

	# TODO
	def __checkVisible(self, vec):
		coords = vec.get()

		# Check z-axis
		if coords[2] < self.pos[2]:
			return False

		return True

	def __projectPoint(self, vec):
		'''
			Types: Vec3D -> (number, number)
		'''

		coords = [vec.get()[0], vec.get()[1], vec.get()[2]]

		for i in range(3):
			coords[i] = coords[i] - self.pos[i]

		ar = self.aspectRatio
		zn = float(self.pos[2])
		zf = 1000.0 # TODO
		fovRad = 1.0 / numpy.tan(self.fov * 0.5 / 180 * numpy.pi)

		projMatrix = numpy.matrix([	[ar*fovRad, 0, 0, 0],
									[0, fovRad, 0, 0],
									[0, 0, zf/(zf-zn), 1.0],
									[0, 0, (zf * zn)/(zf-zn), 0]
									])
		vecMatrix = numpy.matrix(coords + [1])

		r = numpy.dot(vecMatrix, projMatrix).tolist()[0]

		if r[3] == 0:
			r[3] = 1

		x = (r[0]/r[3] + 1) / 2 * float(self.screen.getWidth())
		y = (r[1]/r[3] + 1) / 2 * float(self.screen.getHeight())
		z = r[2]/r[3]

		return Vec3D((x, y, z)).to2D()


	def clear(self):
		self.screen.clear()

	def update(self):
		if self.debug:
			self.__printDebug()
		self.screen.update()

	# Basic getter/setter

	def setName(self, name):
		self.name = name

	def getName(self):
		return self.name

	def getScreen(self):
		return self.screen

	def setFOV(self, fov):
		self.fov = float(fov % 361)

	def getFOV(self):
		return self.fov

	def addFOV(self, df):
		self.setFOV(self.fov + df)

	def setPos(self, pos):
		self.pos = pos

	def getPos(self):
		return self.pos

	def addPos(self, pos):
		npos = []

		for i, opos in enumerate(self.pos):
			npos.append(opos + pos[i])

		self.pos = npos

	def setX(self, x):
		self.setPos((x, self.pos[1], self.pos[2]))

	def getX(self):
		return self.pos[0]

	def addX(self, dx):
		self.addPos((dx, 0, 0))

	def setY(self, y):
		self.setPos((self.pos[0], y, self.pos[1]))

	def getY(self):
		return self.pos[1]

	def addY(self, dy):
		self.addPos((0, dy, 0))

	def setZ(self, z):
		self.setPos((self.pos[0], self.pos[1], z))

	def getZ(self):
		return self.pos[2]

	def addZ(self, dz):
		self.addPos((0, 0, dz))

	def __printDebug(self):
		texts = [
			"Hide invisible surfaces: {}".format(self.lastTriangleHI),
			"FOV: {:10.2f}".format(self.fov),
			"X: {:.2f}  Y: {:.2f}  Z: {:.2f}".format(self.getX(), self.getY(), self.getZ())
		]

		if self.name:
			texts.append("Name: {}".format(self.name))

		surfaces = []
		for text in texts:
			surfaces.append(Text.text(text, "Arial", 32, antialias=True))

		y = self.screen.getHeight()
		for surface in surfaces:
			y -= surface.get_height()

			self.screen.blit(surface, (0, y))