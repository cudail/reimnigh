#!/usr/bin/env python

# © 2020 Caoimhe Ní Chaoimh
# CC BY-NC-SA 4.0

import argparse
from argparse import RawTextHelpFormatter
import sys
import textwrap
import re

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument('briathar', type=str)
args = parser.parse_args()
briathar = args.briathar

gutaí = "aouieáóúíé"

def comhair_siollaí(focal:str)->int:
	return len(re.findall(f"[{gutaí}]+[^{gutaí}]+", focal))

def uraigh(litir:str)->str:
	if is_guta(litir):
		return 'n-'
	return {'b':'m', 'c':'g', 'd':'n', 'f':'bh', 'g':'n', 'p':'b', 't':'d'}.get(litir)

def is_inséimhithe(litir:str)->bool:
	return litir in ['b','c','d','f','g','m','p','s','t']

def is_guta (litir:str)->bool:
	return litir.casefold() in gutaí

def is_caol(focal:str)->bool:
	return guta_deireanach(focal) in "eéií"

def guta_deireanach(focal:str)->str:
	gutaí = [litir for litir in focal if is_guta(litir) ]
	return gutaí[-1]

def leath_nó_caolaigh(deireadh:str, caol:bool)->str:
	if caol:
		return re.sub(r"\[\w+\]|[\(\)]", "", deireadh)
	else:
		return re.sub(r"\(\w+\)|[\[\]]", "", deireadh)

class Leagan():
	def __init__(self, *,
	             mír:str='', urú:bool=False, séimhiú:bool=False,
	             forainm:bool=False, gearr:bool=True, deireadh:str=""):
		self.mír=mír
		self.urú=urú
		self.séimhiú=séimhiú
		self.gearr=gearr
		self.deireadh=deireadh
		self.forainm=forainm
	def réimnigh(self, briathar, forainm=""):

		if comhair_siollaí(briathar) > 1:
			fréamh = re.sub(r"^(.+[^a])a?i(?:([lrns])|(gh))$", r"\1\2", briathar)
		else:
			fréamh = briathar

		céad_litir = briathar[0]
		litreacha_eile = self.gearr and fréamh[1:] or briathar[1:]

		m = self.mír and f"{self.mír} " or ''
		u = self.urú and uraigh(céad_litir) or ''
		s = self.séimhiú and is_inséimhithe(céad_litir) and 'h' or ''
		if self.mír == 'do':
			m = (is_guta(céad_litir) or (céad_litir=='f' and s=='h')) and "d'" or ""

		d = leath_nó_caolaigh(self.deireadh, is_caol(fréamh))
		f = self.forainm and f" {forainm}" or ""

		print(f"  {m}{u}{céad_litir}{s}{litreacha_eile}{d}{f}")

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
		self.a_gchaite=Aimsir("an aimsir ghnáthchaite")
		self.a_láith=Aimsir("an aimsir láithreach")
		self.a_fháist=Aimsir("an aimsir fháistineach")
		self.m_fosh=Aimsir("an modh foshuiteach")
		self.m_ord=Aimsir("an modh ordaitheach")
		self.m_coinn=Aimsir("an modh coinníollach")
		self.aimsirí = [self.a_chaite, self.a_gchaite, self.a_láith, self.a_fháist, self.m_fosh, self.m_ord, self.m_coinn]
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

céad_réimniú.a_chaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, forainm=True)
céad_réimniú.a_chaite.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, forainm=True)
céad_réimniú.a_chaite.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, forainm=True)
céad_réimniú.a_chaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh="(e)amar")
céad_réimniú.a_chaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, forainm=True)
céad_réimniú.a_chaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, forainm=True)
céad_réimniú.a_chaite.briathar_saor =      Leagan(deireadh="(e)adh")

céad_réimniú.a_gchaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh="[a]inn")
céad_réimniú.a_gchaite.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, deireadh="t(e)á")
céad_réimniú.a_gchaite.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh="(e)adh", forainm=True)
céad_réimniú.a_gchaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh="[a]imis")
céad_réimniú.a_gchaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, deireadh="(e)adh", forainm=True)
céad_réimniú.a_gchaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh="[a]idís")
céad_réimniú.a_gchaite.briathar_saor =      Leagan(mír='do', séimhiú=True, deireadh="t[a]í")

céad_réimniú.a_láith.céad_phearsa.uatha = Leagan(deireadh="[a]im")
céad_réimniú.a_láith.dara_pearsa.uatha =  Leagan(deireadh="(e)ann", forainm=True)
céad_réimniú.a_láith.tríú_phearsa.uatha = Leagan(deireadh="(e)ann", forainm=True)
céad_réimniú.a_láith.céad_phearsa.iorla = Leagan(deireadh="[a]imid")
céad_réimniú.a_láith.dara_pearsa.iorla =  Leagan(deireadh="(e)ann", forainm=True)
céad_réimniú.a_láith.tríú_phearsa.iorla = Leagan(deireadh="(e)ann", forainm=True)
céad_réimniú.a_láith.briathar_saor =      Leagan(deireadh="t(e)ar")

céad_réimniú.a_fháist.céad_phearsa.uatha = Leagan(deireadh="f[a]idh", forainm=True)
céad_réimniú.a_fháist.dara_pearsa.uatha =  Leagan(deireadh="f[a]idh", forainm=True)
céad_réimniú.a_fháist.tríú_phearsa.uatha = Leagan(deireadh="f[a]idh", forainm=True)
céad_réimniú.a_fháist.céad_phearsa.iorla = Leagan(deireadh="f[a]imid")
céad_réimniú.a_fháist.dara_pearsa.iorla =  Leagan(deireadh="f[a]idh", forainm=True)
céad_réimniú.a_fháist.tríú_phearsa.iorla = Leagan(deireadh="f[a]idh", forainm=True)
céad_réimniú.a_fháist.briathar_saor =      Leagan(deireadh="f(e)ar")

céad_réimniú.m_fosh.céad_phearsa.uatha = Leagan(mír='go', urú=True, deireadh="[a](e)", forainm=True)
céad_réimniú.m_fosh.dara_pearsa.uatha =  Leagan(mír='go', urú=True, deireadh="[a](e)", forainm=True)
céad_réimniú.m_fosh.tríú_phearsa.uatha = Leagan(mír='go', urú=True, deireadh="[a](e)", forainm=True)
céad_réimniú.m_fosh.céad_phearsa.iorla = Leagan(mír='go', urú=True, deireadh="[a]imid")
céad_réimniú.m_fosh.dara_pearsa.iorla =  Leagan(mír='go', urú=True, deireadh="[a](e)", forainm=True)
céad_réimniú.m_fosh.tríú_phearsa.iorla = Leagan(mír='go', urú=True, deireadh="[a](e)", forainm=True)
céad_réimniú.m_fosh.briathar_saor =      Leagan(mír='go', urú=True, deireadh="t(e)ar")

céad_réimniú.m_ord.céad_phearsa.uatha = Leagan(deireadh="[a]im")
céad_réimniú.m_ord.dara_pearsa.uatha =  Leagan()
céad_réimniú.m_ord.tríú_phearsa.uatha = Leagan(deireadh="(e)adh", forainm=True)
céad_réimniú.m_ord.céad_phearsa.iorla = Leagan(deireadh="[a]imis")
céad_réimniú.m_ord.dara_pearsa.iorla =  Leagan(deireadh="[a]igí")
céad_réimniú.m_ord.tríú_phearsa.iorla = Leagan(deireadh="[a]idís")
céad_réimniú.m_ord.briathar_saor =      Leagan(deireadh="t(e)ar")

céad_réimniú.m_coinn.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh="f[a]inn")
céad_réimniú.m_coinn.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, deireadh="f(e)á")
céad_réimniú.m_coinn.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh="f(e)adh", forainm=True)
céad_réimniú.m_coinn.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh="f[a]imis")
céad_réimniú.m_coinn.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, deireadh="f(e)adh", forainm=True)
céad_réimniú.m_coinn.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh="f[a]idís")
céad_réimniú.m_coinn.briathar_saor =      Leagan(mír='do', séimhiú=True, deireadh="f[a]í")

dara_réimniú.a_chaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, gearr=False, forainm=True)
dara_réimniú.a_chaite.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, gearr=False, forainm=True)
dara_réimniú.a_chaite.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, gearr=False, forainm=True)
dara_réimniú.a_chaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh="[a]íomar")
dara_réimniú.a_chaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, gearr=False, forainm=True)
dara_réimniú.a_chaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, gearr=False, forainm=True)
dara_réimniú.a_chaite.briathar_saor =      Leagan(deireadh="[a]íodh")

dara_réimniú.a_gchaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh="[a]ínn")
dara_réimniú.a_gchaite.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, deireadh="[a]íteá")
dara_réimniú.a_gchaite.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh="[a]íodh", forainm=True)
dara_réimniú.a_gchaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh="[a]ímis")
dara_réimniú.a_gchaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, deireadh="[a]íodh", forainm=True)
dara_réimniú.a_gchaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh="[a]ídís")
dara_réimniú.a_gchaite.briathar_saor =      Leagan(mír='do', séimhiú=True, deireadh="[a]ítí")

dara_réimniú.a_láith.céad_phearsa.uatha = Leagan(deireadh="[a]ím")
dara_réimniú.a_láith.dara_pearsa.uatha =  Leagan(deireadh="[a]íonn", forainm=True)
dara_réimniú.a_láith.tríú_phearsa.uatha = Leagan(deireadh="[a]íonn", forainm=True)
dara_réimniú.a_láith.céad_phearsa.iorla = Leagan(deireadh="[a]ímid")
dara_réimniú.a_láith.dara_pearsa.iorla =  Leagan(deireadh="[a]íonn", forainm=True)
dara_réimniú.a_láith.tríú_phearsa.iorla = Leagan(deireadh="[a]íonn", forainm=True)
dara_réimniú.a_láith.briathar_saor =      Leagan(deireadh="[a]ítear")

dara_réimniú.a_fháist.céad_phearsa.uatha = Leagan(deireadh="[ó](eo)idh", forainm=True)
dara_réimniú.a_fháist.dara_pearsa.uatha =  Leagan(deireadh="[ó](eo)idh", forainm=True)
dara_réimniú.a_fháist.tríú_phearsa.uatha = Leagan(deireadh="[ó](eo)idh", forainm=True)
dara_réimniú.a_fháist.céad_phearsa.iorla = Leagan(deireadh="[ó](eo)imid")
dara_réimniú.a_fháist.dara_pearsa.iorla =  Leagan(deireadh="[ó](eo)idh", forainm=True)
dara_réimniú.a_fháist.tríú_phearsa.iorla = Leagan(deireadh="[ó](eo)idh", forainm=True)
dara_réimniú.a_fháist.briathar_saor =      Leagan(deireadh="[ó](eo)far")

dara_réimniú.m_fosh.céad_phearsa.uatha = Leagan(mír='go', urú=True, deireadh="[a]í", forainm=True)
dara_réimniú.m_fosh.dara_pearsa.uatha =  Leagan(mír='go', urú=True, deireadh="[a]í", forainm=True)
dara_réimniú.m_fosh.tríú_phearsa.uatha = Leagan(mír='go', urú=True, deireadh="[a]í", forainm=True)
dara_réimniú.m_fosh.céad_phearsa.iorla = Leagan(mír='go', urú=True, deireadh="[a]ímid")
dara_réimniú.m_fosh.dara_pearsa.iorla =  Leagan(mír='go', urú=True, deireadh="[a]í", forainm=True)
dara_réimniú.m_fosh.tríú_phearsa.iorla = Leagan(mír='go', urú=True, deireadh="[a]í", forainm=True)
dara_réimniú.m_fosh.briathar_saor =      Leagan(mír='go', urú=True, deireadh="[a]ítear")

dara_réimniú.m_ord.céad_phearsa.uatha = Leagan(deireadh="[a]ím")
dara_réimniú.m_ord.dara_pearsa.uatha =  Leagan(gearr=False)
dara_réimniú.m_ord.tríú_phearsa.uatha = Leagan(deireadh="[a]íodh", forainm=True)
dara_réimniú.m_ord.céad_phearsa.iorla = Leagan(deireadh="[a]ímis")
dara_réimniú.m_ord.dara_pearsa.iorla =  Leagan(deireadh="[a]ígí")
dara_réimniú.m_ord.tríú_phearsa.iorla = Leagan(deireadh="[a]ídís")
dara_réimniú.m_ord.briathar_saor =      Leagan(deireadh="[a]ítear")

dara_réimniú.m_coinn.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh="[ó](eo)inn")
dara_réimniú.m_coinn.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, deireadh="[ó](eo)fá")
dara_réimniú.m_coinn.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh="[ó](eo)dh", forainm=True)
dara_réimniú.m_coinn.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh="[ó](eo)imis")
dara_réimniú.m_coinn.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, deireadh="[ó](eo)dh", forainm=True)
dara_réimniú.m_coinn.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh="[ó](eo)idís")
dara_réimniú.m_coinn.briathar_saor =      Leagan(mír='do', séimhiú=True, deireadh="[ó](eo)faí")

print(briathar)
print()

if comhair_siollaí(briathar) > 1:
	dara_réimniú.réimnigh(briathar)
else:
	céad_réimniú.réimnigh(briathar)
