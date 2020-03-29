#!/usr/bin/env python

# © 2020 Caoimhe Ní Chaoimh
# CC BY-NC-SA 4.0

import argparse
import copy
import re
import sys
import textwrap
from argparse import RawTextHelpFormatter
from enum import Enum, auto
from typing import List

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument('briathar', type=str)

parser.add_argument('-c', help='taispeántar an aimsir chaite', action='store_true')
parser.add_argument('-C', help='taispeántar an aimsir ghnáchchaite', action='store_true')
parser.add_argument('-l', help='taispeántar an aimsir láithreach', action='store_true')
parser.add_argument('-f', help='taispeántar an aimsir fháistineach', action='store_true')
parser.add_argument('-F', help='taispeántar an modh foshuiteach', action='store_true')
parser.add_argument('-o', help='taispeántar an modh ordaitheach', action='store_true')
parser.add_argument('-O', help='taispeántar an modh coinníollach', action='store_true')

args = parser.parse_args()
briathar = args.briathar
a_chaite = args.c
a_gchaite = args.C
a_láith = args.l
a_fháist = args.f
m_fosh = args.F
m_ord = args.o
m_coinn = args.O

gach_aimsirí = not (a_chaite or a_gchaite or a_láith or a_fháist or m_fosh or m_ord or m_coinn)

gutaí = "aouieáóúíé"

def comhair_siollaí(focal:str)->int:
	return len(re.findall(f"[{gutaí}]+[^{gutaí}]+", focal))

def uraigh(litir:str)->str:
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
	def __init__(self, *, mír:str=None, urú:bool=None, séimhiú:bool=None,
	             forainmnigh:bool=None, foirm:Foirm=None, deireadh_tháite:str=None):
		self.mír=mír
		self.urú=urú
		self.séimhiú=séimhiú
		self.foirm=foirm
		self.deireadh_tháite=deireadh_tháite
		self.forainmnigh=forainmnigh
	def réimnigh(self, briathar, deireadh_scartha, leaganacha=None, forainm=""):
		aschur = []
		for bunleagan in leaganacha:
			foirm = self.foirm or bunleagan and bunleagan.forainmnigh or Foirm.táite

			if self.mír == '' and bunleagan and (bunleagan.mír[0] == 'n' or bunleagan.mír[0] == 'a'):
				mír = bunleagan.mír
			else:
				mír = self.mír == None and ( bunleagan == None or None or bunleagan.mír ) or self.mír
			urú = self.urú == None and ( bunleagan == None or None or bunleagan.urú ) or self.urú
			séimhiú = self.séimhiú == None and ( bunleagan == None or None or bunleagan.séimhiú ) or self.séimhiú
			forainmnigh = self.forainmnigh == None and ( bunleagan == None or None or bunleagan.forainmnigh ) or self.forainmnigh

			uimhir_réimnithe = comhair_siollaí(briathar) == 1 and 1 or 2

			if uimhir_réimnithe == 2:
				fréamh = re.sub(r"^(.+[^a])a?i(?:([lrns])|(gh))$", r"\1\2", briathar)
			else:
				fréamh = re.sub(r"^((?:.+[^a])|.)a?igh$", r"\1", briathar)

			céad_litir = briathar[0]
			litreacha_eile = (foirm==Foirm.infinideach) and briathar[1:] or fréamh[1:]

			u = urú and uraigh(céad_litir) or ''
			s = séimhiú and is_inséimhithe(céad_litir) and 'h' or ''
			m = mír and f"{mír} " or ''
			if mír == 'do':
				m = (is_guta(céad_litir) or (céad_litir=='f' and s=='h')) and "d'" or ""
			elif mír == 'go' and is_guta(céad_litir):
				m = 'go n-'

			caol = is_caol(fréamh)
			if caol == None: caol = is_caol(briathar)
			if foirm == Foirm.táite:
				d = leath_nó_caolaigh(self.deireadh_tháite, caol)
			elif foirm == Foirm.scartha:
				d = leath_nó_caolaigh(deireadh_scartha, caol)
			else:
				d = ""

			if d and litreacha_eile and cuir_fada(litreacha_eile[-1]).casefold() == cuir_fada(d[0]).casefold():
				d = d[1:]
			if uimhir_réimnithe == 1 and d and (d[0]=='t' or d[0]=='f') and fréamh[-1] == 'é':
				d = f"i{d}"

			bf = forainmnigh
			if bf == None:
				bf = {Foirm.scartha:True, Foirm.táite:False, Foirm.infinideach:True}.get(foirm)
			f = bf and f" {forainm}" or ""
			aschur.append(f"{m}{u}{céad_litir}{s}{litreacha_eile}{d}{f}")
		return aschur

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
		self.dearfach  = Leagan()
		self.diúltach  = Leagan(mír='ní', séimhiú=True)
		self.ceisteach = Leagan(mír='an', urú=True)

class Réimniú():
	def __init__(self):
		self.a_chaite=Aimsir("an aimsir chaite")
		self.a_gchaite=Aimsir("an aimsir ghnáthchaite")
		self.a_láith=Aimsir("an aimsir láithreach")
		self.a_fháist=Aimsir("an aimsir fháistineach")
		self.m_fosh=Aimsir("an modh foshuiteach")
		self.m_ord=Aimsir("an modh ordaitheach")
		self.m_coinn=Aimsir("an modh coinníollach")
		self.aimsirí = []
		if gach_aimsirí or a_chaite:  self.aimsirí.append(self.a_chaite)
		if gach_aimsirí or a_gchaite: self.aimsirí.append(self.a_gchaite)
		if gach_aimsirí or a_láith:   self.aimsirí.append(self.a_láith)
		if gach_aimsirí or a_fháist:  self.aimsirí.append(self.a_fháist)
		if gach_aimsirí or m_fosh:    self.aimsirí.append(self.m_fosh)
		if gach_aimsirí or m_ord:     self.aimsirí.append(self.m_ord)
		if gach_aimsirí or m_coinn:   self.aimsirí.append(self.m_coinn)
	def réimnigh(self, fréamh:str):
		aschur = []
		for aimsir in self.aimsirí:
			foirmeacha = [aimsir.dearfach,  aimsir.diúltach]
			if aimsir.ceisteach != None: foirmeacha.append(aimsir.ceisteach)
			aschur_aimsire = {'ainm':aimsir.ainm, 'pearsana':[]}
			aschur_aimsire['pearsana'].append(aimsir.céad_phearsa.uatha.réimnigh(fréamh, aimsir.deireadh_scartha, foirmeacha, "mé"))
			aschur_aimsire['pearsana'].append(aimsir.dara_pearsa.uatha.réimnigh(fréamh, aimsir.deireadh_scartha, foirmeacha, "tú"))
			aschur_aimsire['pearsana'].append(aimsir.tríú_phearsa.uatha.réimnigh(fréamh, aimsir.deireadh_scartha, foirmeacha, "sí"))
			aschur_aimsire['pearsana'].append(aimsir.tríú_phearsa.uatha.réimnigh(fréamh, aimsir.deireadh_scartha, foirmeacha, "sé"))
			aschur_aimsire['pearsana'].append(aimsir.céad_phearsa.iorla.réimnigh(fréamh, aimsir.deireadh_scartha, foirmeacha, "sinn"))
			aschur_aimsire['pearsana'].append(aimsir.dara_pearsa.iorla.réimnigh(fréamh, aimsir.deireadh_scartha, foirmeacha, "sibh"))
			aschur_aimsire['pearsana'].append(aimsir.tríú_phearsa.iorla.réimnigh(fréamh, aimsir.deireadh_scartha, foirmeacha, "siad"))
			aschur_aimsire['pearsana'].append(aimsir.briathar_saor.réimnigh(fréamh, aimsir.deireadh_scartha, foirmeacha))
			aschur.append(aschur_aimsire)
		return aschur	


céad_réimniú = Réimniú()
dara_réimniú = Réimniú()

céad_réimniú.a_chaite.dearfach  = Leagan(mír='do',   séimhiú=True)
céad_réimniú.a_chaite.diúltach  = Leagan(mír='níor', séimhiú=True)
céad_réimniú.a_chaite.ceisteach = Leagan(mír='ar',   séimhiú=True)
céad_réimniú.a_chaite.céad_phearsa.uatha = Leagan(foirm=Foirm.infinideach)
céad_réimniú.a_chaite.dara_pearsa.uatha  = Leagan(foirm=Foirm.infinideach)
céad_réimniú.a_chaite.tríú_phearsa.uatha = Leagan(foirm=Foirm.infinideach)
céad_réimniú.a_chaite.céad_phearsa.iorla = Leagan(deireadh_tháite="(e)amar")
céad_réimniú.a_chaite.dara_pearsa.iorla  = Leagan(foirm=Foirm.infinideach)
céad_réimniú.a_chaite.tríú_phearsa.iorla = Leagan(foirm=Foirm.infinideach)
céad_réimniú.a_chaite.briathar_saor      = Leagan(mír='', séimhiú=False, deireadh_tháite="(e)adh")

céad_réimniú.a_gchaite.deireadh_scartha = "(e)adh"
céad_réimniú.a_gchaite.dearfach  = Leagan(mír='do', séimhiú=True)
céad_réimniú.a_gchaite.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]inn")
céad_réimniú.a_gchaite.dara_pearsa.uatha  = Leagan(deireadh_tháite="t(e)á")
céad_réimniú.a_gchaite.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_gchaite.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]imis")
céad_réimniú.a_gchaite.dara_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_gchaite.tríú_phearsa.iorla = Leagan(deireadh_tháite="[a]idís")
céad_réimniú.a_gchaite.briathar_saor      = Leagan(deireadh_tháite="t[a]í")

céad_réimniú.a_láith.deireadh_scartha = "(e)ann"
céad_réimniú.a_láith.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]im")
céad_réimniú.a_láith.dara_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_láith.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_láith.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]imid")
céad_réimniú.a_láith.dara_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_láith.tríú_phearsa.iorla = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_láith.briathar_saor      = Leagan(deireadh_tháite="t(e)ar")

céad_réimniú.a_fháist.deireadh_scartha = "f[a]idh"
céad_réimniú.a_fháist.céad_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.dara_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.céad_phearsa.iorla = Leagan(deireadh_tháite="f[a]imid")
céad_réimniú.a_fháist.dara_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.tríú_phearsa.iorla = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.briathar_saor      = Leagan(deireadh_tháite="f(e)ar")

céad_réimniú.m_fosh.deireadh_scartha = "[a](e)"
céad_réimniú.m_fosh.dearfach = Leagan(mír='go', urú=True)
céad_réimniú.m_fosh.diúltach = Leagan(mír='nár', séimhiú=True)
céad_réimniú.m_fosh.ceisteach = None
céad_réimniú.m_fosh.céad_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_fosh.dara_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_fosh.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_fosh.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]imid")
céad_réimniú.m_fosh.dara_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_fosh.tríú_phearsa.iorla = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_fosh.briathar_saor      = Leagan(deireadh_tháite="t(e)ar")

céad_réimniú.m_ord.deireadh_scartha = "(e)adh"
céad_réimniú.m_ord.diúltach = Leagan(mír='ná', séimhiú=False)
céad_réimniú.m_ord.ceisteach = None
céad_réimniú.m_ord.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]im")
céad_réimniú.m_ord.dara_pearsa.uatha  = Leagan(foirm=Foirm.infinideach, forainmnigh=False)
céad_réimniú.m_ord.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_ord.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]imis")
céad_réimniú.m_ord.dara_pearsa.iorla  = Leagan(deireadh_tháite="[a]igí")
céad_réimniú.m_ord.tríú_phearsa.iorla = Leagan(deireadh_tháite="[a]idís")
céad_réimniú.m_ord.briathar_saor      = Leagan(deireadh_tháite="t(e)ar")

céad_réimniú.m_coinn.deireadh_scartha = "f(e)adh"
céad_réimniú.m_coinn.dearfach = Leagan(mír='do', séimhiú=True)
céad_réimniú.m_coinn.céad_phearsa.uatha = Leagan(deireadh_tháite="f[a]inn")
céad_réimniú.m_coinn.dara_pearsa.uatha  = Leagan(deireadh_tháite="f(e)á")
céad_réimniú.m_coinn.tríú_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_coinn.céad_phearsa.iorla = Leagan(deireadh_tháite="f[a]imis")
céad_réimniú.m_coinn.dara_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_coinn.tríú_phearsa.iorla = Leagan(deireadh_tháite="f[a]idís")
céad_réimniú.m_coinn.briathar_saor      = Leagan(deireadh_tháite="f[a]í")

dara_réimniú = copy.deepcopy(céad_réimniú)

dara_réimniú.a_chaite.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]íomar")
dara_réimniú.a_chaite.briathar_saor      = Leagan(mír='', séimhiú=False, deireadh_tháite="[a]íodh")

dara_réimniú.a_gchaite.deireadh_scartha = "[a]íodh"
dara_réimniú.a_gchaite.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]ínn")
dara_réimniú.a_gchaite.dara_pearsa.uatha  = Leagan(deireadh_tháite="[a]íteá")
dara_réimniú.a_gchaite.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]ímis")
dara_réimniú.a_gchaite.tríú_phearsa.iorla = Leagan(deireadh_tháite="[a]ídís")
dara_réimniú.a_gchaite.briathar_saor      = Leagan(deireadh_tháite="[a]ítí")

dara_réimniú.a_láith.deireadh_scartha = "[a]íonn"
dara_réimniú.a_láith.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]ím")
dara_réimniú.a_láith.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]ímid")
dara_réimniú.a_láith.briathar_saor      = Leagan(deireadh_tháite="[a]ítear")

dara_réimniú.a_fháist.deireadh_scartha = "[ó](eo)idh"
dara_réimniú.a_fháist.céad_phearsa.iorla = Leagan(deireadh_tháite="[ó](eo)imid")
dara_réimniú.a_fháist.briathar_saor      = Leagan(deireadh_tháite="[ó](eo)far")

dara_réimniú.m_fosh.deireadh_scartha = "[a]í"
dara_réimniú.m_fosh.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]ímid")
dara_réimniú.m_fosh.briathar_saor      = Leagan(deireadh_tháite="[a]ítear")

dara_réimniú.m_ord.deireadh_scartha = "[a]íodh"
dara_réimniú.m_ord.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]ím")
dara_réimniú.m_ord.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]ímis")
dara_réimniú.m_ord.dara_pearsa.iorla  = Leagan(deireadh_tháite="[a]ígí")
dara_réimniú.m_ord.tríú_phearsa.iorla = Leagan(deireadh_tháite="[a]ídís")
dara_réimniú.m_ord.briathar_saor      = Leagan(deireadh_tháite="[a]ítear")

dara_réimniú.m_coinn.deireadh_scartha = "[ó](eo)dh"
dara_réimniú.m_coinn.céad_phearsa.uatha = Leagan(deireadh_tháite="[ó](eo)inn")
dara_réimniú.m_coinn.dara_pearsa.uatha  = Leagan(deireadh_tháite="[ó](eo)fá")
dara_réimniú.m_coinn.céad_phearsa.iorla = Leagan(deireadh_tháite="[ó](eo)imis")
dara_réimniú.m_coinn.tríú_phearsa.iorla = Leagan(deireadh_tháite="[ó](eo)idís")
dara_réimniú.m_coinn.briathar_saor      = Leagan(deireadh_tháite="[ó](eo)faí")

céad_réimniú_igh = copy.deepcopy(céad_réimniú)

céad_réimniú_igh.a_chaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="íomar")
céad_réimniú_igh.a_chaite.briathar_saor = Leagan(mír='do', séimhiú=True, deireadh_tháite="íodh")

céad_réimniú_igh.a_gchaite.deireadh_scartha = "íodh"
céad_réimniú_igh.a_gchaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh_tháite="ínn")
céad_réimniú_igh.a_gchaite.dara_pearsa.uatha  = Leagan(mír='do', séimhiú=True, deireadh_tháite="iteá")
céad_réimniú_igh.a_gchaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="ímis")
céad_réimniú_igh.a_gchaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="íodh")
céad_réimniú_igh.a_gchaite.briathar_saor      = Leagan(mír='do', séimhiú=True, deireadh_tháite="ití")

céad_réimniú_igh.a_láith.deireadh_scartha = "íonn"
céad_réimniú_igh.a_láith.céad_phearsa.uatha = Leagan(deireadh_tháite="ím")
céad_réimniú_igh.a_láith.céad_phearsa.iorla = Leagan(deireadh_tháite="ímid")
céad_réimniú_igh.a_láith.briathar_saor      = Leagan(deireadh_tháite="itear")

céad_réimniú_igh.a_fháist.deireadh_scartha = "ífidh"
céad_réimniú_igh.a_fháist.céad_phearsa.iorla = Leagan(deireadh_tháite="ífimid")
céad_réimniú_igh.a_fháist.briathar_saor      = Leagan(deireadh_tháite="ífear")

céad_réimniú_igh.m_fosh.deireadh_scartha = "í"
céad_réimniú_igh.m_fosh.céad_phearsa.iorla = Leagan(mír='go', urú=True, deireadh_tháite="ímid")
céad_réimniú_igh.m_fosh.briathar_saor      = Leagan(mír='go', urú=True, deireadh_tháite="itear")

céad_réimniú_igh.m_ord.deireadh_scartha = "íodh"
céad_réimniú_igh.m_ord.céad_phearsa.uatha = Leagan(deireadh_tháite="ím")
céad_réimniú_igh.m_ord.céad_phearsa.iorla = Leagan(deireadh_tháite="ímis")
céad_réimniú_igh.m_ord.dara_pearsa.iorla  = Leagan(deireadh_tháite="ígí")
céad_réimniú_igh.m_ord.tríú_phearsa.iorla = Leagan(deireadh_tháite="ídís")
céad_réimniú_igh.m_ord.briathar_saor      = Leagan(deireadh_tháite="itear")

céad_réimniú_igh.m_coinn.deireadh_scartha = "ífeadh"
céad_réimniú_igh.m_coinn.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh_tháite="ífinn")
céad_réimniú_igh.m_coinn.dara_pearsa.uatha  = Leagan(mír='do', séimhiú=True, deireadh_tháite="ífeá")
céad_réimniú_igh.m_coinn.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="ífimis")
céad_réimniú_igh.m_coinn.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="ífidís")
céad_réimniú_igh.m_coinn.briathar_saor      = Leagan(mír='do', séimhiú=True, deireadh_tháite="ífí")


if comhair_siollaí(briathar) > 1:
	réimniú = dara_réimniú
elif briathar[-3:] == 'igh' and briathar[-4:] != 'éigh':
	réimniú = céad_réimniú_igh
else:
	réimniú = céad_réimniú

def priontáil_tábla(tábla:List):
	column_widths={}
	for ró in tábla:
		for i, cill in enumerate(ró):
			if column_widths.get(i) == None or len(cill) > column_widths.get(i):
				column_widths[i] = len(cill)
	for ró in tábla:
		aschur=""
		for i, cill in enumerate(ró):
			aschur += cill + " " * (column_widths[i] - len(cill) + 4)
		print(aschur)	


print(briathar)
print()

column_widths={}
réimnithe = réimniú.réimnigh(briathar)
for aimsir in réimnithe:
	for ró in aimsir['pearsana']:
		for i, cill in enumerate(ró):
			if column_widths.get(i) == None or len(cill) > column_widths.get(i):
				column_widths[i] = len(cill)

for aimsir in réimnithe:
	print("  " + aimsir['ainm'])
	for ró in aimsir['pearsana']:
		líne=""
		for i, cill in enumerate(ró):
			líne += cill + " " * (column_widths[i] - len(cill) + 4)
		print(líne)	
	print()
