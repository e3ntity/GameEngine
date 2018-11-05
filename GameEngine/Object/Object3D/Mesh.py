import numpy

from GameEngine.Object.Object import GameObject

class Vec3D:
	def __init__(self, pos, y=None, z=None):
		'''
			Types: -> Vec3D::set
			Precondition: -> Vec3D::set
		'''

		self.set(pos, y, z)

	def set(self, pos, y=None, z=None):
		'''
			Types: 3-tuple/number, number, number
			Precondition: if pos is a number, y and z must also be set
		'''

		if y != None or z != None:
			if y == None or z == None:
				raise Exception("Vec3D::__init__ takes either a 3-tuple position as the first argument or 3 numbers")
			self.pos = (pos, y, z)
		else:
			self.pos = pos

	def add(self, pos):
		'''
			Types: (number, number, number) ->
		'''

		npos = []

		for i in range(3):
			npos.append(self.pos[i] + pos[i])

		self.pos = (npos[0], npos[1], npos[2])

	def get(self):
		'''
			Types: -> (number, number, number)
		'''
		
		return self.pos

	def getX(self):
		return self.pos[0]

	def getY(self):
		return self.pos[1]

	def getZ(self):
		return self.pos[2]

	def getLength(self):
		return numpy.sqrt(self.pos[0] ** 2 + self.pos[1] ** 2 + self.pos[2] ** 2)

	def normalize(self):
		'''
			Types: -> Vec3D
		'''

		length = self.getLength()

		return Vec3D((self.pos[0]/length, self.pos[1]/length, self.pos[2]/length))

	def to2D(self):
		'''
			Types: -> (number, number)
		'''

		x = self.pos[0] - self.pos[2]/2
		y = self.pos[1] - self.pos[2]/2

		return x, y

	@staticmethod
	def crossProduct(vecA, vecB):
		'''
			Types: Vec3D, Vec3D -> Vec3D
		'''

		x = vecA.getY() * vecB.getZ() - vecA.getZ() * vecB.getY()
		y = vecA.getZ() * vecB.getX() - vecA.getX() * vecB.getZ()
		z = vecA.getX() * vecB.getY() - vecA.getY() * vecB.getX()

		return Vec3D((x, y, z))

	@staticmethod
	def dotProduct(vecA, vecB):
		'''
			Types: Vec3D, Vec3D -> number
		'''

		return vecA.getX() * vecB.getX() + vecA.getY() * vecB.getY() + vecA.getZ() * vecB.getZ()

	@staticmethod
	def add(vecA, vecB):
		'''
			Types: vec3D, vec3D -> vec3D
		'''

		x = vecA.getX() + vecB.getX()
		y = vecA.getY() + vecB.getY()
		z = vecA.getZ() + vecB.getZ()

		return Vec3D((x, y, z))

	@staticmethod
	def sub(vecA, vecB):
		'''
			Types: vec3D, vec3D -> vec3D
		'''

		x = vecA.getX() - vecB.getX()
		y = vecA.getY() - vecB.getY()
		z = vecA.getZ() - vecB.getZ()

		return Vec3D((x, y, z))

	@staticmethod
	def mul(vec, scalar):
		'''
			Types: vec3D, number -> vec3D
		'''

		x = vec.getX() * scalar
		y = vec.getY() * scalar
		z = vec.getZ() * scalar

		return Vec3D((x, y, z))

	@staticmethod
	def div(vec, scalar):
		'''
			Types: vec3D, number -> vec3D
		'''

		x = vec.getX() / scalar
		y = vec.getY() / scalar
		z = vec.getZ() / scalar

		return Vec3D((x, y, z))

class Triangle:
	def __init__(self, pos):
		'''
			Types: (Vec3D, Vec3D, Vec3D) ->
		'''

		self.pos = pos

	def getVectors(self):
		'''
			Types: -> (Vec3D, Vec3D, Vec3D)
		'''

		return self.pos

	def getNormalVector(self):
		'''
			Types: -> Vec3D
		'''
 
		vecA = Vec3D.sub(self.pos[0], self.pos[1])
		vecB = Vec3D.sub(self.pos[2], self.pos[1])

		nVec = Vec3D.crossProduct(vecA, vecB)

		return Vec3D.div(nVec, nVec.getLength())


	def getLines(self):
		lines = []

		for i in range(3):
			start_pos = self.pos[i]
			end_pos = self.pos[(i + 1) % 3]

			lines.append((start_pos, end_pos))

		return lines

class Mesh:
	def __init__(self, triangles={}):
		'''
			Types: {} ->
		'''

		self.triangles = triangles

	def getLines(self):
		lines = []
		for _, triangle in self.triangles.items():
			lines += triangle.getLines()

		return lines

	def getTriangles(self):
		return self.triangles

	def addTriangle(self, triangle, index=False):
		# Check index, if no index calculate a new, unique one
		if index == False:
			index = len(self.triangles)

			while index in self.triangles: index += 1

		# Add Triangle
		self.triangles[index] = triangle

		return index

	def getTriangle(self, index):
		try:
			triangle = self.triangles[index]
		except KeyError:
			return False
		return triangle

	def setTriangle(self, triangle, index):
		try:
			self.triangles[index] = triangle
		except KeyError:
			return False
		return True

	def delTriangle(self, index):
		try:
			del self.triangles[index]
		except KeyError:
			return False
		return True

class Cube(Mesh):
	def __init__(self, pos, dim):
		'''
			Types: (number, number, number), (number, number, number)
		'''

		super().__init__()

		# Position and Dimension
		self.pos = pos
		self.dim = dim

		# Initialise mesh with 0-vectors
		for i in range(12):
			self.addTriangle(Vec3D(0, 0, 0), i)

		# Update mesh vectors
		self.__updateMesh()

	def __updateMesh(self):
		p = []

		for i, pos in enumerate(self.pos):
			p.append(pos - self.dim[i]/2)

		x = p[0]
		y = p[1]
		z = p[2]
		w = self.dim[0]
		h = self.dim[1]
		d = self.dim[2]

		p0 = Vec3D(x, y, z)
		p1 = Vec3D(x + w, y, z)
		p2 = Vec3D(x + w, y + h, z)
		p3 = Vec3D(x, y + h, z)

		p4 = Vec3D(x, y, z + d)
		p5 = Vec3D(x + w, y, z + d)
		p6 = Vec3D(x + w, y + h, z + d)
		p7 = Vec3D(x, y + h, z + d)

		self.setTriangle(Triangle((p3, p0, p1)), 0)
		self.setTriangle(Triangle((p3, p1, p2)), 1)

		# Right
		self.setTriangle(Triangle((p2, p1, p5)), 2)
		self.setTriangle(Triangle((p2, p5, p6)), 3)

		# Back
		self.setTriangle(Triangle((p6, p5, p4)), 4)
		self.setTriangle(Triangle((p6, p4, p7)), 5)

		# Left
		self.setTriangle(Triangle((p7, p4, p0)), 6)
		self.setTriangle(Triangle((p7, p0, p3)), 7)

		# Top
		self.setTriangle(Triangle((p0, p4, p5)), 8)
		self.setTriangle(Triangle((p0, p5, p1)), 9)

		# Bottom
		self.setTriangle(Triangle((p7, p3, p2)), 10)
		self.setTriangle(Triangle((p7, p2, p6)), 11)

	def setPos(self, pos):
		self.pos = pos

		self.__updateMesh()

	def getPos(self):
		return self.pos

	def addPos(self, pos):
		npos = []

		for i in range(3):
			npos.append(self.pos[i] + pos[i])

		self.pos = (npos[0], npos[1], npos[2])

		self.__updateMesh()

	def setDim(self, dim):
		self.dim = dim

		self.__updateMesh()

	def getDim(self):
		return self.dim

	def addDim(self, dim):
		ndim = []

		for i in range(3):
			ndim.append(self.dim[i] + dim[i])

		self.dim = (ndim[0], ndim[1], ndim[2])
		
		self.__updateMesh()