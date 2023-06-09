class Material:
	def __init__(self, name=None, Ka=[1.,1.,1.], Kd=[1.,1.,1.], Ks=[1.,1.,1.], Ns=10.0, texture=None):
		'''
		:param name: The name of the Material
		:param Ka: specifies ambient colour
		:param Kd: specifies diffuse colour
		:param Ks: specifies specular colour
		:param Ns: defines the focus of specular highlights in the material
		:param texture: Name of the texture the texture would be map_Kd usually in the .mtl file
		:param alpha: The alpha of the object this makes it slightly see-through or invisible
		'''
		self.name = name
		self.Ka = Ka
		self.Kd = Kd
		self.Ks = Ks
		self.Ns = Ns
		self.texture = texture
		self.alpha = 1.0

class MaterialLibrary:
	def __init__(self):
		# Stores the materials and names in a library
		self.materials = []
		self.names = {}

	def add_material(self, material):
		# Looks at the material name then looks at the length of the materials and appends a new material
		self.names[material.name] = len(self.materials)
		self.materials.append(material)