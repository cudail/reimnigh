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


def is_inséimhithe(litir:str)->bool:
	return litir in ['b','c','d','f','g','m','p','s','t']

def is_guta (litir:str)->bool:
	return litir.casefold() in ['a','á','o','ó','u','ú','i','í','e','é']

def is_caol(focal:str)->bool:
	return guta_deireanach(focal) in ['i','e','í','é']

def guta_deireanach(focal:str)->str:
	gutaí = [litir for litir in focal if is_guta(litir) ]
	return gutaí[-1]


class Leagan():
	def __init__(self, *,
	             do:bool=False, séimhiú:bool=False, urú:bool=False,
	             forainm:bool=False, leathan:str="", caol:str=""):
		self.do=do
		self.séimhiú=séimhiú
		self.urú=urú
		self.forainm=forainm
		self.leathan=leathan
		self.caol=caol
	def réimnigh(self, fréamh, forainm=""):
		céad_litir=fréamh[0]
		litreacha_eile=fréamh[1:]

		s = self.séimhiú and is_inséimhithe(céad_litir) and 'h' or ''
		d = (self.do and (is_guta(céad_litir) or (céad_litir=='f' and s=='h'))) and "d'" or ''

		dr = is_caol(fréamh) and self.caol or self.leathan
		f = self.forainm and f" {forainm}" or ""

		if litreacha_eile[-3:] == 'igh' and dr:
			litreacha_eile = litreacha_eile[:-3]
		print(f"  {d}{céad_litir}{s}{litreacha_eile}{dr}{f}")

class Pearsa():
	def __init__(self):
		self.uatha = None
		self.iorla = None

class Aimsir():
	def __init__(self, ainm:str):
		self.ainm = ainm
		self.céad_phearsa = Pearsa()
		self.dara_pearsa = Pearsa()
		self.tríú_phearsa = Pearsa()
		self.briathar_saor = None

class Réimniú():
	def __init__(self):
		self.a_chaite=Aimsir("an aimsir chaite")
		self.a_láithreach=Aimsir("an aimsir láithreach")
		self.aimsirí = [self.a_chaite, self.a_láithreach]
	def réimnigh(self, fréamh:str):
		for aimsir in self.aimsirí:
			print(f"{aimsir.ainm}:")
			aimsir.céad_phearsa.uatha.réimnigh(fréamh, "mé")
			aimsir.dara_pearsa.uatha.réimnigh(fréamh, "tú")
			aimsir.tríú_phearsa.uatha.réimnigh(fréamh, "sí")
			aimsir.tríú_phearsa.uatha.réimnigh(fréamh, "sé")
			aimsir.céad_phearsa.iorla.réimnigh(fréamh, "sinn")
			aimsir.dara_pearsa.iorla.réimnigh(fréamh, "sibh")
			aimsir.tríú_phearsa.iorla.réimnigh(fréamh, "siad")
			aimsir.briathar_saor.réimnigh(fréamh)
			print()

céad_réimniú = Réimniú()
dara_réimniú = Réimniú()

céad_réimniú.a_chaite.céad_phearsa.uatha = Leagan(do=True, séimhiú=True, forainm=True)
céad_réimniú.a_chaite.dara_pearsa.uatha =  Leagan(do=True, séimhiú=True, forainm=True)
céad_réimniú.a_chaite.tríú_phearsa.uatha = Leagan(do=True, séimhiú=True, forainm=True)
céad_réimniú.a_chaite.céad_phearsa.iorla = Leagan(do=True, séimhiú=True, leathan='amar', caol='eamar')
céad_réimniú.a_chaite.dara_pearsa.iorla =  Leagan(do=True, séimhiú=True, forainm=True)
céad_réimniú.a_chaite.tríú_phearsa.iorla = Leagan(do=True, séimhiú=True, forainm=True)
céad_réimniú.a_chaite.briathar_saor =      Leagan(leathan='adh', caol='eadh')

dara_réimniú.a_chaite.céad_phearsa.uatha = Leagan(do=True, séimhiú=True, forainm=True)
dara_réimniú.a_chaite.dara_pearsa.uatha =  Leagan(do=True, séimhiú=True, forainm=True)
dara_réimniú.a_chaite.tríú_phearsa.uatha = Leagan(do=True, séimhiú=True, forainm=True)
dara_réimniú.a_chaite.céad_phearsa.iorla = Leagan(do=True, séimhiú=True, leathan='aíomar', caol='íomar')
dara_réimniú.a_chaite.dara_pearsa.iorla =  Leagan(do=True, séimhiú=True, forainm=True)
dara_réimniú.a_chaite.tríú_phearsa.iorla = Leagan(do=True, séimhiú=True, forainm=True)
dara_réimniú.a_chaite.briathar_saor =      Leagan(leathan='aíodh', caol='íodh')

céad_réimniú.a_láithreach.céad_phearsa.uatha = Leagan(leathan='aim', caol='im')
céad_réimniú.a_láithreach.dara_pearsa.uatha =  Leagan(leathan='ann', caol='eann', forainm=True)
céad_réimniú.a_láithreach.tríú_phearsa.uatha = Leagan(leathan='ann', caol='eann', forainm=True)
céad_réimniú.a_láithreach.céad_phearsa.iorla = Leagan(leathan='aimid', caol='imid')
céad_réimniú.a_láithreach.dara_pearsa.iorla =  Leagan(leathan='ann', caol='eann', forainm=True)
céad_réimniú.a_láithreach.tríú_phearsa.iorla = Leagan(leathan='ann', caol='eann', forainm=True)
céad_réimniú.a_láithreach.briathar_saor =      Leagan(leathan='tar', caol='tear')

dara_réimniú.a_láithreach.céad_phearsa.uatha = Leagan(leathan='aím', caol='ím')
dara_réimniú.a_láithreach.dara_pearsa.uatha =  Leagan(leathan='aíonn', caol='íonn', forainm=True)
dara_réimniú.a_láithreach.tríú_phearsa.uatha = Leagan(leathan='aíonn', caol='íonn', forainm=True)
dara_réimniú.a_láithreach.céad_phearsa.iorla = Leagan(leathan='aímid', caol='ímid')
dara_réimniú.a_láithreach.dara_pearsa.iorla =  Leagan(leathan='aíonn', caol='íonn', forainm=True)
dara_réimniú.a_láithreach.tríú_phearsa.iorla = Leagan(leathan='aíonn', caol='íonn', forainm=True)
dara_réimniú.a_láithreach.briathar_saor =      Leagan(leathan='aítear', caol='ítear')


print(briathar)
print()

if briathar[-3:] == 'igh':
	dara_réimniú.réimnigh(briathar)
else:
	céad_réimniú.réimnigh(briathar)
