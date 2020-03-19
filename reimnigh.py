#!/usr/bin/env python

# © 2020 Caoimhe Ní Chaoimh
# CC BY-NC-SA 4.0

import argparse
from argparse import RawTextHelpFormatter
import sys
import textwrap

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument('briathar', type=str)
args = parser.parse_args()
briathar = args.briathar




def inséimhithe(litir:str)->bool:
	return litir in ['b','c','d','f','g','m','p','s','t']

def guta_deireanach(focal:str)->str:
	gutaí = [litir for litir in focal if litir in ['a','o','u','i','e']]
	return gutaí[-1]

def caol(focal:str)->bool:
	return guta_deireanach(focal) in ['i','e']

class Leagan():
	def __init__(self, *,
	             séimhiú:bool=False, urú:bool=False,
	             forainm:bool=False, leathan:str="", caol:str=""):
		self.séimhiú=séimhiú
		self.urú=urú
		self.forainm=forainm
		self.leathan=leathan
		self.caol=caol
	def réimnigh(self, fréamh, forainm=""):
		céad_litir=fréamh[0]
		litreacha_eile=fréamh[1:]
		s = self.séimhiú and inséimhithe(céad_litir) and 'h' or ''
		d = caol(fréamh) and self.caol or self.leathan
		f = self.forainm and f" {forainm}" or ""
		print(f"{céad_litir}{s}{litreacha_eile}{d}{f}")

class Pearsa():
	def __init__(self):
		self.uatha = None
		self.iorla = None

class Aimsir():
	def __init__(self):
		self.céad_phearsa = Pearsa()
		self.dara_pearsa = Pearsa()
		self.tríú_phearsa = Pearsa()
		self.briathar_saor = None

class Réimniú():
	def __init__(self):
		self.a_chaite=Aimsir()
		self.aimsirí = [self.a_chaite]
	def réimnigh(self, fréamh:str):
		for aimsir in self.aimsirí:
			aimsir.céad_phearsa.uatha.réimnigh(fréamh, "mé")
			aimsir.dara_pearsa.uatha.réimnigh(fréamh, "tú")
			aimsir.tríú_phearsa.uatha.réimnigh(fréamh, "sí")
			aimsir.tríú_phearsa.uatha.réimnigh(fréamh, "sé")
			aimsir.céad_phearsa.iorla.réimnigh(fréamh, "sinn")
			aimsir.dara_pearsa.iorla.réimnigh(fréamh, "sibh")
			aimsir.tríú_phearsa.iorla.réimnigh(fréamh, "siad")
			aimsir.briathar_saor.réimnigh(fréamh)

céad_réimniú = Réimniú()

céad_réimniú.a_chaite.céad_phearsa.uatha = Leagan(séimhiú=True, forainm=True)
céad_réimniú.a_chaite.dara_pearsa.uatha =  Leagan(séimhiú=True, forainm=True)
céad_réimniú.a_chaite.tríú_phearsa.uatha = Leagan(séimhiú=True, forainm=True)
céad_réimniú.a_chaite.céad_phearsa.iorla = Leagan(séimhiú=True, leathan='amar', caol='eamar')
céad_réimniú.a_chaite.dara_pearsa.iorla =  Leagan(séimhiú=True, forainm=True)
céad_réimniú.a_chaite.tríú_phearsa.iorla = Leagan(séimhiú=True, forainm=True)
céad_réimniú.a_chaite.briathar_saor =      Leagan(leathan='adh', caol='eadh')



céad_réimniú.réimnigh(briathar)
