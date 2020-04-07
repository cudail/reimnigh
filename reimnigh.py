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
parser.add_argument('-g', help='taispeántar an aimsir ghnáchchaite', action='store_true')
parser.add_argument('-l', help='taispeántar an aimsir láithreach', action='store_true')
parser.add_argument('-f', help='taispeántar an aimsir fháistineach', action='store_true')
parser.add_argument('-F', help='taispeántar an modh foshuiteach', action='store_true')
parser.add_argument('-o', help='taispeántar an modh ordaitheach', action='store_true')
parser.add_argument('-O', help='taispeántar an modh coinníollach', action='store_true')

parser.add_argument('-1', help='taispeántar an céad phearsa', action='store_true')
parser.add_argument('-2', help='taispeántar an dara pearsa', action='store_true')
parser.add_argument('-3', help='taispeántar an tríú pearsa', action='store_true')
parser.add_argument('-0', help='taispeántar an briathar saor', action='store_true')
parser.add_argument('-u', help='taispeántar an uatha', action='store_true')
parser.add_argument('-i', help='taispeántar an iolra', action='store_true')

parser.add_argument('-d', help='taispeántar an foirm dhearfach', action='store_true')
parser.add_argument('-D', help='taispeántar an foirm dhiúltach', action='store_true')
parser.add_argument('-C', help='taispeántar an foirm cheisteach', action='store_true')

parser.add_argument('-m', help='úsáidtear an chanúint na Mumhan', action='store_true')

parser.add_argument('-a', help='aibhsítear athruithe', action='store_true')

args = parser.parse_args()
briathar = args.briathar
a_chaite = args.c
a_gchaite = args.g
a_láith = args.l
a_fháist = args.f
m_fosh = args.F
m_ord = args.o
m_coinn = args.O
f_dhearfach = args.d
f_dhiúltach = args.D
f_cheisteach = args.C
c_mumhan = args.m
aibhsigh = args.a

briathar_saor = getattr(args, '0')
céad_phearsa = getattr(args, '1')
dara_pearsa = getattr(args, '2')
tríú_pearsa = getattr(args, '3')
uathar = args.u
iolra = args.i

gach_aimsirí = not (a_chaite or a_gchaite or a_láith or a_fháist or m_fosh or m_ord or m_coinn)
gach_pearsana = not (céad_phearsa or dara_pearsa or tríú_pearsa) and not briathar_saor
uathar_agus_uathar = not (uathar or iolra)
if briathar_saor and not uathar_agus_uathar and not (céad_phearsa or dara_pearsa or tríú_pearsa):
	gach_pearsana = True
gach_foirm = not (f_dhearfach or f_dhiúltach or f_cheisteach)

aibhsithe = '\033[01m'
neamhaibhsithe = '\033[21m'
folínithe = '\033[04m'
neamhfolínithe = '\033[24m'

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
	def __init__(self, *, mír:str=None, h_réimír:bool=None, urú:bool=None, séimhiú:bool=None,
	             forainmnigh:bool=None, foirm:Foirm=None, deireadh_tháite:str=None):
		self.mír=mír
		self.h_réimír=h_réimír
		self.urú=urú
		self.séimhiú=séimhiú
		self.foirm=foirm
		self.deireadh_tháite=deireadh_tháite
		self.forainmnigh=forainmnigh
		self.mumhan = None
	def réimnigh(self, briathar, deireadh_scartha, leaganacha=None, forainm=""):
		aschur = []
		leagan = (c_mumhan and self.mumhan) and self.mumhan or self
		for bunleagan in leaganacha:
			foirm = leagan.foirm or bunleagan and bunleagan.forainmnigh or Foirm.táite

			if leagan.mír == '' and bunleagan and (bunleagan.mír[0] == 'n' or bunleagan.mír[0] == 'a'):
				mír = bunleagan.mír
			else:
				mír = leagan.mír == None and ( bunleagan == None or None or bunleagan.mír ) or leagan.mír
			h_réimír = leagan.h_réimír == None and ( bunleagan == None or None or bunleagan.h_réimír ) or leagan.h_réimír
			urú = leagan.urú == None and ( bunleagan == None or None or bunleagan.urú ) or leagan.urú
			séimhiú = leagan.séimhiú == None and ( bunleagan == None or None or bunleagan.séimhiú ) or leagan.séimhiú
			forainmnigh = leagan.forainmnigh == None and ( bunleagan == None or None or bunleagan.forainmnigh ) or leagan.forainmnigh

			if comhair_siollaí(briathar) == 1 or briathar[-3:] == 'áin':
				fréamh = re.sub(r"^((?:.+[^a])|.)a?igh$", r"\1", briathar)
			else:
				fréamh = re.sub(r"^(.+[^a])a?i(?:([lrns])|(gh))$", r"\1\2", briathar)

			céad_litir = briathar[0]
			litreacha_eile = (foirm==Foirm.infinideach) and briathar[1:] or fréamh[1:]

			if is_guta(céad_litir):
				u = h_réimír and 'h' or ''
			else:
				u = urú and uraigh(céad_litir) or ''

			s = séimhiú and is_inséimhithe(céad_litir) and 'h' or ''

			m = mír and f"{mír} " or ''
			if mír == 'do':
				m = (is_guta(céad_litir) or (céad_litir=='f' and s=='h')) and "d'" or c_mumhan and "do " or ""
			elif mír == 'go' and is_guta(céad_litir):
				m = 'go n-'

			caol = is_caol(fréamh)
			if caol == None: caol = is_caol(briathar)
			if foirm == Foirm.táite:
				d = leath_nó_caolaigh(leagan.deireadh_tháite, caol)
			elif foirm == Foirm.scartha:
				d = leath_nó_caolaigh(deireadh_scartha, caol)
			else:
				d = ""

			if d and litreacha_eile and cuir_fada(litreacha_eile[-1]).casefold() == cuir_fada(d[0]).casefold():
				d = d[1:]
			if litreacha_eile and litreacha_eile[-1] == 'ó' and d[0] == 'a':
				d = d[1:]
			if comhair_siollaí(briathar) == 1 and d and (d[0]=='t' or d[0]=='f') and fréamh[-1] == 'é':
				d = f"i{d}"

			bf = forainmnigh
			if bf == None:
				bf = {Foirm.scartha:True, Foirm.táite:False, Foirm.infinideach:True}.get(foirm)
			f = bf and f" {forainm}" or ""
			
			a = aibhsigh and aibhsithe or ''
			n = aibhsigh and neamhaibhsithe or ''
			
			aschur.append(f"{m}{a}{u}{n}{céad_litir}{a}{s}{n}{litreacha_eile}{a}{d}{n}{f}")
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
		self.tríú_pearsa = Pearsa()
		self.deireadh_scartha = ""
		self.deireadh_scartha_mumhan = None
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
			foirmeacha = []
			if aimsir.dearfach and gach_foirm or f_dhearfach:
				foirmeacha.append(aimsir.dearfach)
			if aimsir.diúltach and gach_foirm or f_dhiúltach:
							foirmeacha.append(aimsir.diúltach)
			if aimsir.ceisteach and gach_foirm or f_cheisteach:
							foirmeacha.append(aimsir.ceisteach)

			pearsana = []
			aschur_aimsire = {'ainm':aimsir.ainm, 'pearsana':pearsana}
			deireadh = (c_mumhan and aimsir.deireadh_scartha_mumhan) and aimsir.deireadh_scartha_mumhan or aimsir.deireadh_scartha
			if (gach_pearsana or céad_phearsa) and (uathar_agus_uathar or uathar):
				pearsana.append(aimsir.céad_phearsa.uatha.réimnigh(fréamh, deireadh, foirmeacha, "mé"))
			if (gach_pearsana or dara_pearsa) and (uathar_agus_uathar or uathar):
				pearsana.append(aimsir.dara_pearsa.uatha.réimnigh(fréamh, deireadh, foirmeacha, "tú"))
			if (gach_pearsana or tríú_pearsa) and (uathar_agus_uathar or uathar):
				pearsana.append(aimsir.tríú_pearsa.uatha.réimnigh(fréamh, deireadh, foirmeacha, "sí"))
			if (gach_pearsana or tríú_pearsa) and (uathar_agus_uathar or uathar):
				pearsana.append(aimsir.tríú_pearsa.uatha.réimnigh(fréamh, deireadh, foirmeacha, "sé"))
			if (gach_pearsana or céad_phearsa) and (uathar_agus_uathar or iolra):
				pearsana.append(aimsir.céad_phearsa.iorla.réimnigh(fréamh, deireadh, foirmeacha, "sinn"))
			if (gach_pearsana or dara_pearsa) and (uathar_agus_uathar or iolra):
				pearsana.append(aimsir.dara_pearsa.iorla.réimnigh(fréamh, deireadh, foirmeacha, "sibh"))
			if (gach_pearsana or tríú_pearsa) and (uathar_agus_uathar or iolra):
				pearsana.append(aimsir.tríú_pearsa.iorla.réimnigh(fréamh, deireadh, foirmeacha, "siad"))
			if (gach_pearsana or briathar_saor):
				pearsana.append(aimsir.briathar_saor.réimnigh(fréamh, deireadh, foirmeacha))
			aschur.append(aschur_aimsire)
		return aschur	


céad_réimniú = Réimniú()

céad_réimniú.a_chaite.dearfach  = Leagan(mír='do',   séimhiú=True)
céad_réimniú.a_chaite.diúltach  = Leagan(mír='níor', séimhiú=True)
céad_réimniú.a_chaite.ceisteach = Leagan(mír='ar',   séimhiú=True)
céad_réimniú.a_chaite.céad_phearsa.uatha = Leagan(foirm=Foirm.infinideach)
céad_réimniú.a_chaite.dara_pearsa.uatha  = Leagan(foirm=Foirm.infinideach)
céad_réimniú.a_chaite.tríú_pearsa.uatha  = Leagan(foirm=Foirm.infinideach)
céad_réimniú.a_chaite.céad_phearsa.iorla = Leagan(deireadh_tháite="(e)amar")
céad_réimniú.a_chaite.dara_pearsa.iorla  = Leagan(foirm=Foirm.infinideach)
céad_réimniú.a_chaite.tríú_pearsa.iorla  = Leagan(foirm=Foirm.infinideach)
céad_réimniú.a_chaite.briathar_saor      = Leagan(mír='', séimhiú=False, deireadh_tháite="(e)adh")

céad_réimniú.a_chaite.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="(e)as")
céad_réimniú.a_chaite.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="[a]is")
céad_réimniú.a_chaite.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="(e)amair")
céad_réimniú.a_chaite.dara_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="(e)abhair")
céad_réimniú.a_chaite.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="(e)adar")


céad_réimniú.a_gchaite.deireadh_scartha = "(e)adh"
céad_réimniú.a_gchaite.dearfach  = Leagan(mír='do', séimhiú=True)
céad_réimniú.a_gchaite.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]inn")
céad_réimniú.a_gchaite.dara_pearsa.uatha  = Leagan(deireadh_tháite="t(e)á")
céad_réimniú.a_gchaite.tríú_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_gchaite.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]imis")
céad_réimniú.a_gchaite.dara_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_gchaite.tríú_pearsa.iorla  = Leagan(deireadh_tháite="[a]idís")
céad_réimniú.a_gchaite.briathar_saor      = Leagan(deireadh_tháite="t[a]í")

céad_réimniú.a_gchaite.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="th(e)á")
céad_réimniú.a_gchaite.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[a]imís")


céad_réimniú.a_láith.deireadh_scartha = "(e)ann"
céad_réimniú.a_láith.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]im")
céad_réimniú.a_láith.dara_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_láith.tríú_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_láith.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]imid")
céad_réimniú.a_láith.dara_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_láith.tríú_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_láith.briathar_saor      = Leagan(deireadh_tháite="t(e)ar")

céad_réimniú.a_láith.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="[a]ir")
céad_réimniú.a_láith.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[a]imíd")
céad_réimniú.a_láith.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="[a]id", forainmnigh=True)


céad_réimniú.a_fháist.deireadh_scartha = "f[a]idh"
céad_réimniú.a_fháist.céad_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.dara_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.tríú_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.céad_phearsa.iorla = Leagan(deireadh_tháite="f[a]imid")
céad_réimniú.a_fháist.dara_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.tríú_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.a_fháist.briathar_saor      = Leagan(deireadh_tháite="f(e)ar")

céad_réimniú.a_fháist.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="f(e)ad")
céad_réimniú.a_fháist.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="f[a]ir")
céad_réimniú.a_fháist.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="f[a]imíd")
céad_réimniú.a_fháist.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="f[a]id", forainmnigh=True)


céad_réimniú.m_fosh.deireadh_scartha = "[a](e)"
céad_réimniú.m_fosh.dearfach = Leagan(mír='go', urú=True)
céad_réimniú.m_fosh.diúltach = Leagan(mír='nár', séimhiú=True)
céad_réimniú.m_fosh.ceisteach = None
céad_réimniú.m_fosh.céad_phearsa.uatha = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_fosh.dara_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_fosh.tríú_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_fosh.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]imid")
céad_réimniú.m_fosh.dara_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_fosh.tríú_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_fosh.briathar_saor      = Leagan(deireadh_tháite="t(e)ar")

céad_réimniú.m_fosh.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="(e)ad")
céad_réimniú.m_fosh.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="[a]ir")


céad_réimniú.m_ord.deireadh_scartha = "(e)adh"
céad_réimniú.m_ord.diúltach = Leagan(mír='ná', h_réimír=True)
céad_réimniú.m_ord.ceisteach = None
céad_réimniú.m_ord.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]im")
céad_réimniú.m_ord.dara_pearsa.uatha  = Leagan(foirm=Foirm.infinideach, forainmnigh=False)
céad_réimniú.m_ord.tríú_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_ord.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]imis")
céad_réimniú.m_ord.dara_pearsa.iorla  = Leagan(deireadh_tháite="[a]igí")
céad_réimniú.m_ord.tríú_pearsa.iorla  = Leagan(deireadh_tháite="[a]idís")
céad_réimniú.m_ord.briathar_saor      = Leagan(deireadh_tháite="t(e)ar")

céad_réimniú.m_ord.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[a]imís")
céad_réimniú.m_ord.dara_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="[a]idh")


céad_réimniú.m_coinn.deireadh_scartha = "f(e)adh"
céad_réimniú.m_coinn.dearfach = Leagan(mír='do', séimhiú=True)
céad_réimniú.m_coinn.céad_phearsa.uatha = Leagan(deireadh_tháite="f[a]inn")
céad_réimniú.m_coinn.dara_pearsa.uatha  = Leagan(deireadh_tháite="f(e)á")
céad_réimniú.m_coinn.tríú_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_coinn.céad_phearsa.iorla = Leagan(deireadh_tháite="f[a]imis")
céad_réimniú.m_coinn.dara_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
céad_réimniú.m_coinn.tríú_pearsa.iorla  = Leagan(deireadh_tháite="f[a]idís")
céad_réimniú.m_coinn.briathar_saor      = Leagan(deireadh_tháite="f[a]í")

céad_réimniú.m_coinn.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="f[a]imís")



dara_réimniú = copy.deepcopy(céad_réimniú)

dara_réimniú.a_chaite.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]íomar")
dara_réimniú.a_chaite.briathar_saor      = Leagan(mír='', séimhiú=False, deireadh_tháite="[a]íodh")

dara_réimniú.a_chaite.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="[a]íos")
dara_réimniú.a_chaite.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="[a]ís")
dara_réimniú.a_chaite.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[a]íomair")
dara_réimniú.a_chaite.dara_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="[a]íobhair")
dara_réimniú.a_chaite.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="[a]íodar")


dara_réimniú.a_gchaite.deireadh_scartha = "[a]íodh"
dara_réimniú.a_gchaite.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]ínn")
dara_réimniú.a_gchaite.dara_pearsa.uatha  = Leagan(deireadh_tháite="[a]íteá")
dara_réimniú.a_gchaite.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]ímis")
dara_réimniú.a_gchaite.tríú_pearsa.iorla  = Leagan(deireadh_tháite="[a]ídís")
dara_réimniú.a_gchaite.briathar_saor      = Leagan(deireadh_tháite="[a]ítí")

dara_réimniú.a_gchaite.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="[a]íthá")
dara_réimniú.a_gchaite.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[a]ímís")


dara_réimniú.a_láith.deireadh_scartha = "[a]íonn"
dara_réimniú.a_láith.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]ím")
dara_réimniú.a_láith.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]ímid")
dara_réimniú.a_láith.briathar_saor      = Leagan(deireadh_tháite="[a]ítear")
dara_réimniú.a_láith.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]ímid")

dara_réimniú.a_láith.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[a]ímíd")
dara_réimniú.a_láith.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="[a]íd", forainmnigh=True)
dara_réimniú.a_láith.briathar_saor.mumhan      = Leagan(deireadh_tháite="[a]íthear")


dara_réimniú.a_fháist.deireadh_scartha = "[ó](eo)idh"
dara_réimniú.a_fháist.céad_phearsa.iorla = Leagan(deireadh_tháite="[ó](eo)imid")
dara_réimniú.a_fháist.briathar_saor      = Leagan(deireadh_tháite="[ó](eo)far")

dara_réimniú.a_fháist.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="[ó](eo)d")
dara_réimniú.a_fháist.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="[ó](eo)ir")
dara_réimniú.a_fháist.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[ó](eo)imíd")
dara_réimniú.a_fháist.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[ó](eo)id", forainmnigh=True)


dara_réimniú.m_fosh.deireadh_scartha = "[a]í"
dara_réimniú.m_fosh.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]ímid")
dara_réimniú.m_fosh.briathar_saor      = Leagan(deireadh_tháite="[a]ítear")

dara_réimniú.m_fosh.deireadh_scartha_mumhan = "[a]ídh"
dara_réimniú.m_fosh.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="[a]íod")
dara_réimniú.m_fosh.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="[a]ír")
dara_réimniú.m_fosh.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[a]ímíd")
dara_réimniú.m_fosh.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="[a]íd", forainmnigh=True)
dara_réimniú.m_fosh.briathar_saor.mumhan      = Leagan(deireadh_tháite="[a]íthear")


dara_réimniú.m_ord.deireadh_scartha = "[a]íodh"
dara_réimniú.m_ord.céad_phearsa.uatha = Leagan(deireadh_tháite="[a]ím")
dara_réimniú.m_ord.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]ímis")
dara_réimniú.m_ord.dara_pearsa.iorla  = Leagan(deireadh_tháite="[a]ígí")
dara_réimniú.m_ord.tríú_pearsa.iorla  = Leagan(deireadh_tháite="[a]ídís")
dara_réimniú.m_ord.briathar_saor      = Leagan(deireadh_tháite="[a]ítear")

dara_réimniú.m_ord.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[a]ímís")
dara_réimniú.m_ord.dara_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="[a]ídh")
dara_réimniú.m_ord.briathar_saor.mumhan      = Leagan(deireadh_tháite="[a]íthear")


dara_réimniú.m_coinn.deireadh_scartha = "[ó](eo)dh"
dara_réimniú.m_coinn.céad_phearsa.uatha = Leagan(deireadh_tháite="[ó](eo)inn")
dara_réimniú.m_coinn.dara_pearsa.uatha  = Leagan(deireadh_tháite="[ó](eo)fá")
dara_réimniú.m_coinn.céad_phearsa.iorla = Leagan(deireadh_tháite="[ó](eo)imis")
dara_réimniú.m_coinn.tríú_pearsa.iorla  = Leagan(deireadh_tháite="[ó](eo)idís")
dara_réimniú.m_coinn.briathar_saor      = Leagan(deireadh_tháite="[ó](eo)faí")

dara_réimniú.m_coinn.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[ó](eo)imís")



céad_réimniú_igh = copy.deepcopy(céad_réimniú)

céad_réimniú_igh.a_chaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="íomar")
céad_réimniú_igh.a_chaite.briathar_saor = Leagan(mír='do', séimhiú=True, deireadh_tháite="íodh")

céad_réimniú_igh.a_chaite.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="íos")
céad_réimniú_igh.a_chaite.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="ís")
céad_réimniú_igh.a_chaite.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="íomair")
céad_réimniú_igh.a_chaite.dara_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="íobhair")
céad_réimniú_igh.a_chaite.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="íodar")


céad_réimniú_igh.a_gchaite.deireadh_scartha = "íodh"
céad_réimniú_igh.a_gchaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, deireadh_tháite="ínn")
céad_réimniú_igh.a_gchaite.dara_pearsa.uatha  = Leagan(mír='do', séimhiú=True, deireadh_tháite="iteá")
céad_réimniú_igh.a_gchaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, deireadh_tháite="ímis")
céad_réimniú_igh.a_gchaite.tríú_pearsa.iorla  = Leagan(mír='do', séimhiú=True, deireadh_tháite="íodh")
céad_réimniú_igh.a_gchaite.briathar_saor      = Leagan(mír='do', séimhiú=True, deireadh_tháite="ití")

céad_réimniú_igh.a_gchaite.dara_pearsa.uatha.mumhan  = Leagan(mír='do', séimhiú=True, deireadh_tháite="íthá")
céad_réimniú_igh.a_gchaite.céad_phearsa.iorla.mumhan = Leagan(mír='do', séimhiú=True, deireadh_tháite="ímís")
céad_réimniú_igh.a_gchaite.tríú_pearsa.iorla.mumhan  = Leagan(mír='do', séimhiú=True, deireadh_tháite="ídís")
céad_réimniú_igh.a_gchaite.briathar_saor.mumhan      = Leagan(mír='do', séimhiú=True, deireadh_tháite="ítí")


céad_réimniú_igh.a_láith.deireadh_scartha = "íonn"
céad_réimniú_igh.a_láith.céad_phearsa.uatha = Leagan(deireadh_tháite="ím")
céad_réimniú_igh.a_láith.céad_phearsa.iorla = Leagan(deireadh_tháite="ímid")
céad_réimniú_igh.a_láith.briathar_saor      = Leagan(deireadh_tháite="itear")

céad_réimniú_igh.a_láith.dara_pearsa.uatha.mumhan  = Leagan(foirm=Foirm.scartha)
céad_réimniú_igh.a_láith.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="ímíd")
céad_réimniú_igh.a_láith.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="íd", forainmnigh=True)


céad_réimniú_igh.a_fháist.deireadh_scartha = "ífidh"
céad_réimniú_igh.a_fháist.céad_phearsa.iorla = Leagan(deireadh_tháite="ífimid")
céad_réimniú_igh.a_fháist.briathar_saor      = Leagan(deireadh_tháite="ífear")

céad_réimniú_igh.a_fháist.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="ífead")
céad_réimniú_igh.a_fháist.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="ífir")
céad_réimniú_igh.a_fháist.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="ífimíd")
céad_réimniú_igh.a_fháist.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="ífid", forainmnigh=True)
céad_réimniú_igh.a_fháist.briathar_saor.mumhan      = Leagan(deireadh_tháite="ífar")



céad_réimniú_igh.m_fosh.deireadh_scartha = "í"
céad_réimniú_igh.m_fosh.céad_phearsa.iorla = Leagan(deireadh_tháite="ímid")
céad_réimniú_igh.m_fosh.briathar_saor      = Leagan(deireadh_tháite="itear")

céad_réimniú_igh.m_fosh.deireadh_scartha_mumhan = "ídh"
céad_réimniú_igh.m_fosh.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="íod")
céad_réimniú_igh.m_fosh.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="ír")
céad_réimniú_igh.m_fosh.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="ímíd")
céad_réimniú_igh.m_fosh.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="íd", forainmnigh=True)
céad_réimniú_igh.m_fosh.briathar_saor.mumhan      = Leagan(deireadh_tháite="ítear")


céad_réimniú_igh.m_ord.deireadh_scartha = "íodh"
céad_réimniú_igh.m_ord.céad_phearsa.uatha = Leagan(deireadh_tháite="ím")
céad_réimniú_igh.m_ord.céad_phearsa.iorla = Leagan(deireadh_tháite="ímis")
céad_réimniú_igh.m_ord.dara_pearsa.iorla  = Leagan(deireadh_tháite="ígí")
céad_réimniú_igh.m_ord.tríú_pearsa.iorla  = Leagan(deireadh_tháite="ídís")
céad_réimniú_igh.m_ord.briathar_saor      = Leagan(deireadh_tháite="itear")

céad_réimniú_igh.m_ord.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="ímís")
céad_réimniú_igh.m_ord.dara_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="ídh")
céad_réimniú_igh.m_ord.briathar_saor.mumhan      = Leagan(deireadh_tháite="ítear")


céad_réimniú_igh.m_coinn.deireadh_scartha = "ífeadh"
céad_réimniú_igh.m_coinn.céad_phearsa.uatha = Leagan(deireadh_tháite="ífinn")
céad_réimniú_igh.m_coinn.dara_pearsa.uatha  = Leagan(deireadh_tháite="ífeá")
céad_réimniú_igh.m_coinn.céad_phearsa.iorla = Leagan(deireadh_tháite="ífimis")
céad_réimniú_igh.m_coinn.tríú_pearsa.iorla  = Leagan(deireadh_tháite="ífidís")
céad_réimniú_igh.m_coinn.briathar_saor      = Leagan(deireadh_tháite="ífí")

céad_réimniú_igh.m_coinn.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="ífá")
céad_réimniú_igh.m_coinn.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="ífimís")



def cén_réimniú(briathar:str)->Réimniú:
	if comhair_siollaí(briathar) > 1:
		if briathar[-3:] == 'igh' or briathar[-2:] in ['ir', 'il', 'in']:
			if briathar[-3:] not in ['áil', 'áin', 'óil']:
				return dara_réimniú
	if briathar[-3:] == 'igh' and briathar[-4:] not in ['éigh', 'óigh']:
		return céad_réimniú_igh
	return céad_réimniú

def priontáil_toradh(toradh:List):
	leithid_colún={}
	for aimsir in toradh:
		for ró in aimsir['pearsana']:
			for i, cill in enumerate(ró):
				if leithid_colún.get(i) == None or len(cill) > leithid_colún.get(i):
					leithid_colún[i] = len(cill)
	for aimsir in toradh:
		if len(toradh) > 1:
			f = aibhsigh and folínithe or ''
			n = aibhsigh and neamhfolínithe or ''
			print(f"  {f}{aimsir['ainm']}{n}")
		for ró in aimsir['pearsana']:
			líne=""
			for i, cill in enumerate(ró):
				líne += cill + " " * (leithid_colún[i] - len(cill) + 4)
			print(líne)
		if aimsir != toradh[-1]:
			print()

priontáil_toradh(cén_réimniú(briathar).réimnigh(briathar))
