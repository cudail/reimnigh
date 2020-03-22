#!/usr/bin/env python

# © 2020 Caoimhe Ní Chaoimh
# CC BY-NC-SA 4.0

import argparse
from argparse import RawTextHelpFormatter
import sys
import textwrap
import re
import copy
from enum import Enum, auto

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

def cuir_fada(litir:str)->str:
	return {'á':'a', 'ó':'o', 'ú':'u', 'í':'i', 'é':'e'}.get(litir) or litir

def is_inséimhithe(litir:str)->bool:
	return litir in ['b','c','d','f','g','m','p','s','t']

def is_guta (litir:str)->bool:
	return litir.casefold() in gutaí

def is_caol(focal:str)->bool:
	guta = guta_deireanach(focal)
	if guta: return guta_deireanach(focal) in "eéií"

def guta_deireanach(focal:str)->str:
	gutaí = [litir for litir in focal if is_guta(litir) ]
	if gutaí: return gutaí[-1]

def leath_nó_caolaigh(deireadh:str, caol:bool)->str:
	if caol:
		return re.sub(r"\[\w+\]|[\(\)]", "", deireadh)
	else:
		return re.sub(r"\(\w+\)|[\[\]]", "", deireadh)


class Foirm(Enum):
	scartha=auto()
	táite=auto()
	infinideach=auto()

class Leagan():
	def __init__(self, *,
	             mír:str='', urú:bool=False, séimhiú:bool=False,
	             forainm:bool=None, foirm:Foirm=Foirm.táite, deireadh_tháite:str=""):
		self.mír=mír
		self.urú=urú
		self.séimhiú=séimhiú
		self.foirm=foirm
		self.deireadh_tháite=deireadh_tháite
		self.forainm=forainm
	def réimnigh(self, briathar, deireadh_scartha, forainm=""):

		uimhir_réimnithe = comhair_siollaí(briathar) == 1 and 1 or 2

		if uimhir_réimnithe == 2:
			fréamh = re.sub(r"^(.+[^a])a?i(?:([lrns])|(gh))$", r"\1\2", briathar)
		else:
			fréamh = re.sub(r"^((?:.+[^a])|.)a?igh$", r"\1", briathar)

		céad_litir = briathar[0]
		litreacha_eile = (self.foirm==Foirm.infinideach) and briathar[1:] or fréamh[1:]

		m = self.mír and f"{self.mír} " or ''
		u = self.urú and uraigh(céad_litir) or ''
		s = self.séimhiú and is_inséimhithe(céad_litir) and 'h' or ''
		if self.mír == 'do':
			m = (is_guta(céad_litir) or (céad_litir=='f' and s=='h')) and "d'" or ""

		caol = is_caol(fréamh)
		if caol == None: caol = is_caol(briathar)
		if self.foirm == Foirm.táite:
			d = leath_nó_caolaigh(self.deireadh_tháite, caol)
		elif self.foirm == Foirm.scartha:
			d = leath_nó_caolaigh(deireadh_scartha, caol)
		else:
			d = ""

		if d and litreacha_eile and cuir_fada(litreacha_eile[-1]).casefold() == cuir_fada(d[0]).casefold():
			d = d[1:]
		if uimhir_réimnithe == 1 and d and (d[0]=='t' or d[0]=='f') and fréamh[-1] == 'é':
			d = f"i{d}"

		bf = self.forainm
		if bf == None:
			bf = {Foirm.scartha:True, Foirm.táite:False, Foirm.infinideach:True}.get(self.foirm)
		f = bf and f" {forainm}" or ""

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
		self.deireadh_scartha = ""
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
			aimsir.céad_phearsa.uatha.réimnigh(fréamh, aimsir.deireadh_scartha, "mé")
			aimsir.dara_pearsa.uatha.réimnigh(fréamh, aimsir.deireadh_scartha, "tú")
			aimsir.tríú_phearsa.uatha.réimnigh(fréamh, aimsir.deireadh_scartha, "sí")
			aimsir.tríú_phearsa.uatha.réimnigh(fréamh, aimsir.deireadh_scartha, "sé")
			aimsir.céad_phearsa.iorla.réimnigh(fréamh, aimsir.deireadh_scartha, "sinn")
			aimsir.dara_pearsa.iorla.réimnigh(fréamh, aimsir.deireadh_scartha, "sibh")
			aimsir.tríú_phearsa.iorla.réimnigh(fréamh, aimsir.deireadh_scartha, "siad")
			aimsir.briathar_saor.réimnigh(fréamh, aimsir.deireadh_scartha)
			print()

céad_réimniú = Réimniú()
dara_réimniú = Réimniú()

céad_réimniú.a_chaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, foirm=Foirm.infinideach)
céad_réimniú.a_chaite.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, foirm=Foirm.infinideach)
céad_réimniú.a_chaite.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, foirm=Foirm.infinideach)
céad_réimniú.a_chaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="(e)amar")
céad_réimniú.a_chaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, foirm=Foirm.infinideach)
céad_réimniú.a_chaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, foirm=Foirm.infinideach)
céad_réimniú.a_chaite.briathar_saor =      Leagan(deireadh_tháite="(e)adh")

céad_réimniú.a_gchaite.deireadh_scartha = "(e)adh"
céad_réimniú.a_gchaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh_tháite="[a]inn")
céad_réimniú.a_gchaite.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, deireadh_tháite="t(e)á")
céad_réimniú.a_gchaite.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, foirm=Foirm.scartha)
céad_réimniú.a_gchaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="[a]imis")
céad_réimniú.a_gchaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, foirm=Foirm.scartha)
céad_réimniú.a_gchaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="[a]idís")
céad_réimniú.a_gchaite.briathar_saor =      Leagan(mír='do', séimhiú=True, deireadh_tháite="t[a]í")

céad_réimniú.a_láith.deireadh_scartha = "(e)ann"
céad_réimniú.a_láith.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]im")
céad_réimniú.a_láith.dara_pearsa.uatha =  Leagan(foirm=Foirm.scartha)
céad_réimniú.a_láith.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_láith.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]imid")
céad_réimniú.a_láith.dara_pearsa.iorla =  Leagan(foirm=Foirm.scartha)
céad_réimniú.a_láith.tríú_phearsa.iorla = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_láith.briathar_saor =      Leagan(deireadh_tháite="t(e)ar")

céad_réimniú.a_fháist.deireadh_scartha = "f[a]idh"
céad_réimniú.a_fháist.céad_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.dara_pearsa.uatha =  Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.céad_phearsa.iorla = Leagan(deireadh_tháite="f[a]imid")
céad_réimniú.a_fháist.dara_pearsa.iorla =  Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.tríú_phearsa.iorla = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.briathar_saor =      Leagan(deireadh_tháite="f(e)ar")

céad_réimniú.m_fosh.deireadh_scartha = "[a](e)"
céad_réimniú.m_fosh.céad_phearsa.uatha = Leagan(mír='go', urú=True, foirm=Foirm.scartha)
céad_réimniú.m_fosh.dara_pearsa.uatha =  Leagan(mír='go', urú=True, foirm=Foirm.scartha)
céad_réimniú.m_fosh.tríú_phearsa.uatha = Leagan(mír='go', urú=True, foirm=Foirm.scartha)
céad_réimniú.m_fosh.céad_phearsa.iorla = Leagan(mír='go', urú=True, deireadh_tháite="[a]imid")
céad_réimniú.m_fosh.dara_pearsa.iorla =  Leagan(mír='go', urú=True, foirm=Foirm.scartha)
céad_réimniú.m_fosh.tríú_phearsa.iorla = Leagan(mír='go', urú=True, foirm=Foirm.scartha)
céad_réimniú.m_fosh.briathar_saor =      Leagan(mír='go', urú=True, deireadh_tháite="t(e)ar")

céad_réimniú.m_ord.deireadh_scartha = "(e)adh"
céad_réimniú.m_ord.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]im")
céad_réimniú.m_ord.dara_pearsa.uatha =  Leagan(foirm=Foirm.infinideach, forainm=False)
céad_réimniú.m_ord.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_ord.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]imis")
céad_réimniú.m_ord.dara_pearsa.iorla =  Leagan(deireadh_tháite="[a]igí")
céad_réimniú.m_ord.tríú_phearsa.iorla = Leagan(deireadh_tháite="[a]idís")
céad_réimniú.m_ord.briathar_saor =      Leagan(deireadh_tháite="t(e)ar")

céad_réimniú.m_coinn.deireadh_scartha = "f(e)adh"
céad_réimniú.m_coinn.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh_tháite="f[a]inn")
céad_réimniú.m_coinn.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, deireadh_tháite="f(e)á")
céad_réimniú.m_coinn.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, foirm=Foirm.scartha)
céad_réimniú.m_coinn.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="f[a]imis")
céad_réimniú.m_coinn.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, foirm=Foirm.scartha)
céad_réimniú.m_coinn.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="f[a]idís")
céad_réimniú.m_coinn.briathar_saor =      Leagan(mír='do', séimhiú=True, deireadh_tháite="f[a]í")

dara_réimniú.a_chaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, foirm=Foirm.infinideach)
dara_réimniú.a_chaite.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, foirm=Foirm.infinideach)
dara_réimniú.a_chaite.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, foirm=Foirm.infinideach)
dara_réimniú.a_chaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="[a]íomar")
dara_réimniú.a_chaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, foirm=Foirm.infinideach)
dara_réimniú.a_chaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, foirm=Foirm.infinideach)
dara_réimniú.a_chaite.briathar_saor =      Leagan(deireadh_tháite="[a]íodh")

dara_réimniú.a_gchaite.deireadh_scartha = "[a]íodh"
dara_réimniú.a_gchaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh_tháite="[a]ínn")
dara_réimniú.a_gchaite.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, deireadh_tháite="[a]íteá")
dara_réimniú.a_gchaite.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, foirm=Foirm.scartha)
dara_réimniú.a_gchaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="[a]ímis")
dara_réimniú.a_gchaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, foirm=Foirm.scartha)
dara_réimniú.a_gchaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="[a]ídís")
dara_réimniú.a_gchaite.briathar_saor =      Leagan(mír='do', séimhiú=True, deireadh_tháite="[a]ítí")

dara_réimniú.a_láith.deireadh_scartha = "[a]íonn"
dara_réimniú.a_láith.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]ím")
dara_réimniú.a_láith.dara_pearsa.uatha =  Leagan(foirm=Foirm.scartha)
dara_réimniú.a_láith.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
dara_réimniú.a_láith.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]ímid")
dara_réimniú.a_láith.dara_pearsa.iorla =  Leagan(foirm=Foirm.scartha)
dara_réimniú.a_láith.tríú_phearsa.iorla = Leagan(foirm=Foirm.scartha)
dara_réimniú.a_láith.briathar_saor =      Leagan(deireadh_tháite="[a]ítear")

dara_réimniú.a_fháist.deireadh_scartha = "[ó](eo)idh"
dara_réimniú.a_fháist.céad_phearsa.uatha = Leagan(foirm=Foirm.scartha)
dara_réimniú.a_fháist.dara_pearsa.uatha =  Leagan(foirm=Foirm.scartha)
dara_réimniú.a_fháist.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
dara_réimniú.a_fháist.céad_phearsa.iorla = Leagan(deireadh_tháite="[ó](eo)imid")
dara_réimniú.a_fháist.dara_pearsa.iorla =  Leagan(foirm=Foirm.scartha)
dara_réimniú.a_fháist.tríú_phearsa.iorla = Leagan(foirm=Foirm.scartha)
dara_réimniú.a_fháist.briathar_saor =      Leagan(deireadh_tháite="[ó](eo)far")

dara_réimniú.m_fosh.deireadh_scartha = "[a]í"
dara_réimniú.m_fosh.céad_phearsa.uatha = Leagan(mír='go', urú=True, foirm=Foirm.scartha)
dara_réimniú.m_fosh.dara_pearsa.uatha =  Leagan(mír='go', urú=True, foirm=Foirm.scartha)
dara_réimniú.m_fosh.tríú_phearsa.uatha = Leagan(mír='go', urú=True, foirm=Foirm.scartha)
dara_réimniú.m_fosh.céad_phearsa.iorla = Leagan(mír='go', urú=True, deireadh_tháite="[a]ímid")
dara_réimniú.m_fosh.dara_pearsa.iorla =  Leagan(mír='go', urú=True, foirm=Foirm.scartha)
dara_réimniú.m_fosh.tríú_phearsa.iorla = Leagan(mír='go', urú=True, foirm=Foirm.scartha)
dara_réimniú.m_fosh.briathar_saor =      Leagan(mír='go', urú=True, deireadh_tháite="[a]ítear")

dara_réimniú.m_ord.deireadh_scartha = "[a]íodh"
dara_réimniú.m_ord.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]ím")
dara_réimniú.m_ord.dara_pearsa.uatha =  Leagan(foirm=Foirm.infinideach, forainm=False)
dara_réimniú.m_ord.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
dara_réimniú.m_ord.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]ímis")
dara_réimniú.m_ord.dara_pearsa.iorla =  Leagan(deireadh_tháite="[a]ígí")
dara_réimniú.m_ord.tríú_phearsa.iorla = Leagan(deireadh_tháite="[a]ídís")
dara_réimniú.m_ord.briathar_saor =      Leagan(deireadh_tháite="[a]ítear")

dara_réimniú.m_coinn.deireadh_scartha = "[ó](eo)dh"
dara_réimniú.m_coinn.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh_tháite="[ó](eo)inn")
dara_réimniú.m_coinn.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, deireadh_tháite="[ó](eo)fá")
dara_réimniú.m_coinn.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, foirm=Foirm.scartha)
dara_réimniú.m_coinn.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="[ó](eo)imis")
dara_réimniú.m_coinn.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, foirm=Foirm.scartha)
dara_réimniú.m_coinn.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="[ó](eo)idís")
dara_réimniú.m_coinn.briathar_saor =      Leagan(mír='do', séimhiú=True, deireadh_tháite="[ó](eo)faí")

céad_réimniú_igh = copy.deepcopy(céad_réimniú)

céad_réimniú_igh.a_chaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="íomar")
céad_réimniú_igh.a_chaite.briathar_saor = Leagan(mír='do', séimhiú=True, deireadh_tháite="íodh")

céad_réimniú_igh.a_gchaite.deireadh_scartha = "íodh"
céad_réimniú_igh.a_gchaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh_tháite="ínn")
céad_réimniú_igh.a_gchaite.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, deireadh_tháite="iteá")
céad_réimniú_igh.a_gchaite.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, foirm=Foirm.scartha)
céad_réimniú_igh.a_gchaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="ímis")
céad_réimniú_igh.a_gchaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, foirm=Foirm.scartha)
céad_réimniú_igh.a_gchaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="íodh")
céad_réimniú_igh.a_gchaite.briathar_saor =      Leagan(mír='do', séimhiú=True, deireadh_tháite="ití")

céad_réimniú_igh.a_láith.deireadh_scartha = "íonn"
céad_réimniú_igh.a_láith.céad_phearsa.uatha = Leagan(deireadh_tháite="ím")
céad_réimniú_igh.a_láith.dara_pearsa.uatha =  Leagan(foirm=Foirm.scartha)
céad_réimniú_igh.a_láith.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú_igh.a_láith.céad_phearsa.iorla = Leagan(deireadh_tháite="ímid")
céad_réimniú_igh.a_láith.dara_pearsa.iorla =  Leagan(foirm=Foirm.scartha)
céad_réimniú_igh.a_láith.tríú_phearsa.iorla = Leagan(foirm=Foirm.scartha)
céad_réimniú_igh.a_láith.briathar_saor =      Leagan(deireadh_tháite="itear")

céad_réimniú_igh.a_fháist.deireadh_scartha = "ífidh"
céad_réimniú_igh.a_fháist.céad_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú_igh.a_fháist.dara_pearsa.uatha =  Leagan(foirm=Foirm.scartha)
céad_réimniú_igh.a_fháist.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú_igh.a_fháist.céad_phearsa.iorla = Leagan(deireadh_tháite="ífimid")
céad_réimniú_igh.a_fháist.dara_pearsa.iorla =  Leagan(foirm=Foirm.scartha)
céad_réimniú_igh.a_fháist.tríú_phearsa.iorla = Leagan(foirm=Foirm.scartha)
céad_réimniú_igh.a_fháist.briathar_saor =      Leagan(deireadh_tháite="ífear")

céad_réimniú_igh.m_fosh.deireadh_scartha = "í"
céad_réimniú_igh.m_fosh.céad_phearsa.uatha = Leagan(mír='go', urú=True, foirm=Foirm.scartha)
céad_réimniú_igh.m_fosh.dara_pearsa.uatha =  Leagan(mír='go', urú=True, foirm=Foirm.scartha)
céad_réimniú_igh.m_fosh.tríú_phearsa.uatha = Leagan(mír='go', urú=True, foirm=Foirm.scartha)
céad_réimniú_igh.m_fosh.céad_phearsa.iorla = Leagan(mír='go', urú=True, deireadh_tháite="ímid")
céad_réimniú_igh.m_fosh.dara_pearsa.iorla =  Leagan(mír='go', urú=True, foirm=Foirm.scartha)
céad_réimniú_igh.m_fosh.tríú_phearsa.iorla = Leagan(mír='go', urú=True, foirm=Foirm.scartha)
céad_réimniú_igh.m_fosh.briathar_saor =      Leagan(mír='go', urú=True, deireadh_tháite="itear")

céad_réimniú_igh.m_ord.deireadh_scartha = "íodh"
céad_réimniú_igh.m_ord.céad_phearsa.uatha = Leagan(deireadh_tháite="ím")
céad_réimniú_igh.m_ord.dara_pearsa.uatha =  Leagan(foirm=Foirm.infinideach, forainm=True)
céad_réimniú_igh.m_ord.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú_igh.m_ord.céad_phearsa.iorla = Leagan(deireadh_tháite="ímis")
céad_réimniú_igh.m_ord.dara_pearsa.iorla =  Leagan(deireadh_tháite="ígí")
céad_réimniú_igh.m_ord.tríú_phearsa.iorla = Leagan(deireadh_tháite="ídís")
céad_réimniú_igh.m_ord.briathar_saor =      Leagan(deireadh_tháite="itear")

céad_réimniú_igh.m_coinn.deireadh_scartha = "ífeadh"
céad_réimniú_igh.m_coinn.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh_tháite="ífinn")
céad_réimniú_igh.m_coinn.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, deireadh_tháite="ífeá")
céad_réimniú_igh.m_coinn.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, foirm=Foirm.scartha)
céad_réimniú_igh.m_coinn.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="ífimis")
céad_réimniú_igh.m_coinn.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, foirm=Foirm.scartha)
céad_réimniú_igh.m_coinn.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="ífidís")
céad_réimniú_igh.m_coinn.briathar_saor =      Leagan(mír='do', séimhiú=True, deireadh_tháite="ífí")


print(briathar)
print()

if comhair_siollaí(briathar) > 1:
	réimniú = dara_réimniú
elif briathar[-3:] == 'igh' and briathar[-4:] != 'éigh':
	réimniú = céad_réimniú_igh
else:
	réimniú = céad_réimniú

réimniú.réimnigh(briathar)
