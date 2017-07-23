import VR
from Device import Device

class Radiator(Device):
	""" Definiert eine Heizung als Subklasse von Device.

	Eine Heizung ist ein Geraet in der VR-Umgebung mit einer "physischen" Repraesentation, das
	kaputt gehen und reperiert werden kann. Die Heizung laedt zwei 3D-Modelle, von denen immer
	genau eines, abhaengig ihres Funktionszustands, sichtbar ist.  

	@attr transform: uebergeordnetes Transform-Objekt, fuer die zwei Geometrie-Objekte (VR.Transform)
	@attr geometry: Geometrie-Objekt des funktionierenden Heizkoerpers (VR.Geometry)
	@attr geometryBroken: Geometrie-Objekt des defekten Heizkoerpers (VR.Geometry)
	"""

	def __init__(self, item_id, room_name, position, direction, scale):
		""" Erstelle eine Objekt der Klasse Radiator.

		Erstellt eine Heizung, laedt die benoetigten 3D-Modelle und verbindet diese
		mit der PolyVR-Umgebung. Die Modelle fuer die Heizung muessen sich hierbei 
		im korrekten Unterordner befinden: /assets/[Raumname]/radiator(_broken).dae

		@param item_id: Eindeutiger Identifikator der Heizung (String)
		@param room_name: Name des Raums, welcher die Heizung enthaelt (String)
		@param position: Position der Heizung, relativ zum enthaltenden Raum ([float, float, float])
		@param direction: Ausrichtung der Heizung, relativ zum enthaltenden Raum ([float, float, float])
		@param scale: Skalierung der Heizung, (wahrscheinlich) relaitv zum enthaltenden Raum ([float, float, float])
		"""
		self.transform = VR.Transform("Radiator_" + room_name)
		self.transform.setPose(position, direction, [0,1,0])
		self.transform.setScale(scale)
		VR.find(room_name).addChild(self.transform)
		
		path = "./assets/" + room_name + "/"
		self.geometry = VR.loadGeometry(path + "radiator.dae", preset="COLLADA").getChild(0).getChild(0)
		self.transform.addChild(self.geometry)
		self.geometryBroken = VR.loadGeometry(path + "radiator_broken.dae", preset="COLLADA").getChild(0).getChild(0)
		self.transform.addChild(self.geometryBroken)
		self.geometryBroken.setVisible(False)
		
		# Obsolete Implementierung um bei Defekten das Material zu wechseln. Kann nach wie vor verwendet werden.
		'''self.operatingMat = self.geometry.getMaterial()
		self.brokenMat = VR.materials["Broken Radiator"]
		self.geometry.setMaterial(self.operatingMat)'''

		super(Radiator, self).__init__(item_id, "RADIATOR", True, room_name, self.geometry)

	def set_broken(self):
		""" Schaffe einen Defekt bei der Heizung.

		Aendert das Geometriemodell auf die defekte Variante und ruft die
		entsprechende Methode in der Superklasse auf.
		"""
		#self.geometry.setMaterial(self.brokenMat)
		self.geometry.setVisible(False)
		self.geometryBroken.setVisible(True)
		self.set_geometry(self.geometryBroken)
		super(Radiator, self).set_broken()

	def set_repaired(self):
		"""  Beseitige den Defekt bei der Heizung.

		Aendert das Geometriemodell auf die funktionale Variante und ruft die 
		entsprechende Methode in der Superklasse auf.
		"""
		#self.geometry.setMaterial(self.operatingMat)
		self.geometryBroken.setVisible(False)
		self.geometry.setVisible(True)
		self.set_geometry(self.geometry)
		super(Radiator, self).set_repaired()
