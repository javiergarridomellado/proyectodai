from django.test import TestCase

# Create your tests here.


from restaurante.views import *
from restaurante.models import Bar
from django.test.client import RequestFactory
# Create your tests here.Anadido testeo rutas



class BarMethodTests(TestCase):

	def test_nombre_bar(self):
		bar = Bar(nombre='BarPaco' ,direccion='Recogidas', numerovisitas='500')
		bar.save()
		self.assertEqual(bar.nombre,'BarPaco')
		self.assertEqual(bar.direccion,'Recogidas')
		self.assertEqual(bar.numerovisitas,'500')
		print("Testeo correcto.")
