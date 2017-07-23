import VR
from Device import Device

class Lamp(Device):
	""" Klasse fuer Lampen als Smart-Devices

	Klasse Lamp erbt von Klasse Device und baut somit auf dem generischen Smart-Device auf.
	In der aktuellen Version bestehen Lampen aus einer einfachen Geometrie aus zwei Primitiven
	(Kugel und Zylinder), die im Konstruktor erstellt werden. Eine Lampe enthaelt eine Referenz
	auf ihr zugehoeriges Licht-Objekt in PolyVR. Wenn die Lampe ein- oder ausgeschaltet wird,
	wird das zugewiesebe Licht ebenfalls umgeschaltet, und die Geometrie der "Gluehbirne" wechselt
	ihr Material um farblich den Zustand der Lampe zu verdeutlichen.

	@attr isOn: Angabe, ob die Lampe eingeschaltet ist, oder nicht (Boolean)
	@attr light: Referenz auf die zugehoerige Lichtquelle in PolyVR (VR.Light)
	@attr transform: Transform-Objekt, das die Geometrie der Lampe unter sich vereint (VR.Transform)
	@attr cordGeom: Geometrie des Lampenkabels (VR.Geometry)
	@attr bulbGeom: Geometrie des Leuchtkoerpers der Lampe (VR.Geometry)
	@attr lightBeacon: Objekt fuer die raeumliche Positionierung der Lichtquelle in PolyVR (VR.LightBeacon)
	@attr cordMat: Material des Lampenkabels (VR.Material)
	@attr bulbOffMat: Material des ausgeschalteten Leuchtkoerpers der Lampe (VR.Material)
	@attr bulbOnMat; Material des eingeschalteten Leuchtkoerpers der Lampe (VR.Material)
	"""
	def __init__(self, item_id, room_name, parent, light):
		""" Instanziiere ein Objekt der Klasse Lamp.

		Der Konstruktor erstellt eine Lampe am festgelegten Zentrum des angegebenen Raums (anhand des Mittelpunkts des Bodens),
		welche in diesem Raum von der Decke haengt. Er definiert die Geometrie der Lampe aus zwei Primitiven und weist dieser 
		die passenden Materialien zu.

		@param item_id: Eindeutige Identifizierung der Lampe (String)
		@param room_name: Name des Raums, der diese Lampe in der VR-Umgebung enthaelt. (String)
		@param parent: Elternobjekt der Lampe im Szenengraph (VR.Object)
		@param light: zu dieser Lampe gehoerende Lichtquelle in PolyVR (VR.Light)
		"""
		self.isOn = False
		self.light = light

		self.transform = VR.Transform("Lamp_" + parent.getName())
		parent.addChild(self.transform)
		self.transform.setPose([0,2.4,0],[0,0,-1],[0,1,0])
		
		self.cordGeom = VR.Geometry("Cord" + parent.getName())
		self.transform.addChild(self.cordGeom)
		self.cordGeom.setPrimitive("Cylinder 0.3 0.01 8 0 0 1")
		self.cordGeom.setPose([0,0,0],[0,0,-1],[0,1,0])
		
		self.bulbGeom = VR.Geometry("LightBuld" + parent.getName())
		self.transform.addChild(self.bulbGeom)
		self.bulbGeom.setPrimitive("Sphere 0.1 2")
		self.bulbGeom.setPose([0,-0.25,0],[0,0,-1],[0,1,0])
		
		self.lightBeacon = VR.LightBeacon("LightBeacon_" + parent.getName())
		self.transform.addChild(self.lightBeacon)
		self.lightBeacon.setPose([0,-0.25,0],[0,0,-1],[0,1,0])
		light.setBeacon(self.lightBeacon)

		self.cordMat = VR.materials["Lamp Cord"]
		self.cordGeom.setMaterial(self.cordMat)

		self.bulbOffMat = VR.materials["Light Bulb off"]
		self.bulbGeom.setMaterial(self.bulbOffMat)

		self.bulbOnMat = VR.materials["Light Bulb on"]

		super(Lamp, self).__init__(item_id, "LIGHT", True, room_name, self.bulbGeom)

	def switchOn(self):
		""" Schalte die Lampe ein.

		aendert das Material der Lampe und schaltet die PolyVR-Lichtquelle ein.
		"""
		if self._ok:
			self.bulbGeom.setMaterial(self.bulbOnMat)
			self.light.setOn(True)
			self.isOn = True

	def switchOff(self):
		""" Schalte die Lampe aus.

		aendert das Material der Lampe und schaltet die PolyVR-Lichtquelle aus.
		"""
		self.bulbGeom.setMaterial(self.bulbOffMat)
		self.light.setOn(False)
		self.isOn = False

	def switch(self, on):
		""" Schalte die Lampe und ihre Lichtquelle um, je nach uebergebenem Parameter

		@param on: Gibt an, ob die Lampe ein- oder ausgeschaltet werden soll; an/aus (Boolean)
		"""
		if on and not self.isOn:
			self.switchOn()
		elif not on and self.isOn:
			self.switchOff()
	def toggle(self):
		""" oeffne, oder schliesse, die Tuer abhaengig von ihrem oeffnungszustand.
		"""
		if self.isOn:
			self.switchOff()
		else:
			self.switchOn()


	def set_broken(self):
		""" Schaffe einen Defekt bei der Lampe.

		Schaltet die Lampe aus, da die Defekt-Simulation das nicht uebernimmt, und ruft die
		entsprechende Methode in der Superklasse auf.
		"""
		super(Lamp, self).set_broken()
		self.switchOff()
		
	def set_repaired(self):
		""" Repariere einen Defekt bei der Lampe.
		
		Davon ausgehend, dass sich zur Lampenreparatur eine Person im zugehoerigen Raum
		befinden muss, und die Lampe auf deren Anwesenheit reagieren soll, schaltet die
		Lampe automatisch ein, wenn sie repariert ist.
		Ruft ebenfalls die entsprechende Methode in der Superklasse auf.
		"""
		super(Lamp, self).set_repaired()
		self.switchOn()
