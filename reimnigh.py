#!/usr/bin/env python

# © 2020 Caoimhe Ní Chaoimh
# CC BY-NC-SA 4.0

from copy import deepcopy
from enum import Enum, auto
from re import sub, findall
from typing import List

# vowels
gutaí = "aouieáóúíé"


# count the number of syllables in a word by counting clusters of vowels
def comhair_siollaí(focal: str) -> int:
	return len(findall(f"[{gutaí}]+[^{gutaí}]+", focal))


# eclipsis
def uraigh(litir: str) -> str:
	return {'b': 'm', 'c': 'g', 'd': 'n', 'f': 'bh', 'g': 'n', 'p': 'b', 't': 'd'}.get(litir)


# strip fada from vowels
def cuir_fada(litir: str) -> str:
	return {'á': 'a', 'ó': 'o', 'ú': 'u', 'í': 'i', 'é': 'e'}.get(litir) or litir


# is this letter leniteable?
def is_inséimhithe(litir: str) -> bool:
	return litir in ['b', 'c', 'd', 'f', 'g', 'm', 'p', 's', 't']


# is this a vowel?
def is_guta(litir: str) -> bool:
	return litir.casefold() in gutaí


# does this string end in a slender vowel?
def is_caol(focal: str) -> bool:
	guta = guta_deireanach(focal)
	if guta:
		return guta in "eéií"


# what is the last vowel in this string?
def guta_deireanach(focal: str) -> str:
	gutaí_amháin = [litir for litir in focal if is_guta(litir)]
	if gutaí_amháin:
		return gutaí_amháin[-1]


# get slender or broad form of given ending
# slender form -> remove letters encased in []
# broad formn -> remove letters encased in ()
def leath_nó_caolaigh(deireadh: str, caol: bool) -> str:
	if caol:
		return sub(r"\[\w+\]|[()]", "", deireadh)
	else:
		return sub(r"\(\w+\)|[\[\]]", "", deireadh)


# highlight string if ANSI highlights are enabled
def aibhsigh(teaghrán: str) -> str:
	return f"[01m{teaghrán}[21m"


# underline string if ANSI highlights are enabled
def folínigh(teaghrán: str) -> str:
	return f"[04m{teaghrán}[24m"


# remove ASCI escape sequences
def neamhaibhsigh(teaghrán: str) -> str:
	return sub(r"\[\d\dm", "", teaghrán)


# analytic, synthetic or infinitive form
class Foirm(Enum):
	scartha = auto()
	táite = auto()
	infinideach = auto()


# options for tenses
class FoghaAimsire(Enum):
	def __init__(self, ainm):
		self.ainm = ainm

	chaite = "an aimsir chaite"
	ghnáthchaite = "an aimsir ghnáthchaite"
	láithreach = "an aimsir láithreach"
	fháistineach = "an aimsir fháistineach"
	foshuiteach = "an modh foshuiteach"
	ordaitheach = "an modh ordaitheach"
	coinníollach = "an modh coinníollach"


# options for persons
class FoghaPearsan(Enum):
	def __init__(self, forainm):
		self.forainm = forainm  # pronoun

	céad_uatha = "mé"
	dara_uatha = "tú"
	tríú_uatha = "sí/sé"
	céad_iorla = "sinn"
	dara_iorla = "sibh"
	tríú_iorla = "siad"
	briathar_saor = None


# options for affirmative, negative and interrogative moods
class FoghaFoirme(Enum):
	dhearfach = auto()
	dhiúltach = auto()
	cheisteach = auto()


# Defines a specific form of a verb with various rules
# e.g. the first person singular affirmative form for a first conjugation verb 
#      is a synthetic form with an ending "aim" or "im"
#      -> foirm=Foirm.táite, deireadh_tháite="[a]im" 
class Leagan:
	def __init__(self, *, mír:str=None, urú:bool=None, séimhiú:bool=None,
	             forainmnigh:bool=None, foirm:Foirm=None, deireadh_tháite:str=None):
		self.mír = mír
		self.urú = urú
		self.séimhiú = séimhiú
		self.foirm = foirm
		self.deireadh_tháite = deireadh_tháite
		self.forainmnigh = forainmnigh
		self.mumhan = None

	# conjugate
	def réimnigh(self, briathar, deireadh_scartha, leaganacha, forainm, mumhan, aibhsiú):
		aschur = []  # output stored in list
		leagan = (mumhan and self.mumhan) and self.mumhan or self  # check if we're using the Munster form

		for bunleagan in leaganacha:
			# Build rules from hierarchy. If this object has a rule specified itself, use that
			# otherwise check if the base form for this tense has it defined
			foirm = leagan.foirm or bunleagan and bunleagan.forainmnigh or Foirm.táite  # synthetic form if not specified otherwise
			mír = leagan.mír is None and (bunleagan is None or None or bunleagan.mír) or leagan.mír
			urú = leagan.urú is None and (bunleagan is None or None or bunleagan.urú) or leagan.urú
			séimhiú = leagan.séimhiú is None and (bunleagan is None or None or bunleagan.séimhiú) or leagan.séimhiú
			forainmnigh = leagan.forainmnigh is None and (bunleagan is None or None or bunleagan.forainmnigh) or leagan.forainmnigh

			# from stems for verbs ending in -igh, il, ir, in and is
			if len(briathar) > 2 and briathar[-3:] in ['igh', 'ígh']:
				fréamh = sub(r"^((?:.+[^a])|.)a?[ií]gh$", r"\1", briathar)
			elif comhair_siollaí(briathar) > 1:
				fréamh = sub(r"^(.+[^a])[a]?i(?:([lrns])|(gh))$", r"\1\2", briathar)
			else:
				fréamh = briathar

			céad_litir = briathar[0]  # first letter
			litreacha_eile = (foirm == Foirm.infinideach) and briathar[1:] or fréamh[1:]  # rest of the word

			# do we have lenition?
			s = séimhiú and is_inséimhithe(céad_litir) and 'h' or ''

			# prefix
			réimnír = urú and uraigh(céad_litir) or ''

			if mír is None:
				mír = ''
			# particles can cause mutations
			# 'go' causes vowels to take an n- prefix
			elif mír == 'go' and is_guta(céad_litir):
				réimnír = 'n-'
			# 'ná' causes vowels to take a h- prefix
			elif mír == 'ná' and is_guta(céad_litir):
				réimnír = 'h'
			# 'do' is supressed unless the verb starts with a vowel or we're using the Munster dialect
			elif mír == 'do':
				if is_guta(céad_litir) or (céad_litir == 'f' and s == 'h'):
					réimnír = "d'"
					# hack to supress d' prefix for past tense autonomous form
					if forainm is None and leagan.deireadh_tháite.endswith("dh"):
						réimnír = ''
					mír = ''
				else:
					mír = mumhan and 'do' or ''

			# is our stem slender or broad?
			caol = is_caol(fréamh)

			# -áil becomes -ál unless we have an analytic form ending that starts with 't'
			# in which case it stays as -áil and takes a slender ending
			if briathar[-3:] == 'áil' and litreacha_eile[-2:] == 'ál' and foirm == Foirm.táite and leagan.deireadh_tháite[0] == 't':
				caol = True
				litreacha_eile = litreacha_eile[:-2] + 'áil'
			elif (briathar[-4:] in ['óigh', 'úigh', 'áigh'] or briathar[-5:] in ['eoigh', 'uaigh']) and foirm == Foirm.táite and leagan.deireadh_tháite[0] == 't':
				caol = True
				litreacha_eile = litreacha_eile + 'i'

			if caol is None: caol = is_caol(briathar)

			# form the ending
			if foirm == Foirm.táite:
				deireadh = leath_nó_caolaigh(leagan.deireadh_tháite, caol)  # form the analytic ending
			elif foirm == Foirm.scartha:
				deireadh = leath_nó_caolaigh(deireadh_scartha, caol)  # form the synthetic ending
			else:
				deireadh = ''

			# remove double vowels if the stem ends with the same letter the ending starts with
			if deireadh and fréamh and cuir_fada(fréamh[-1]).casefold() == cuir_fada(deireadh[0]).casefold():
				deireadh = deireadh[1:]
			# if stem ends in ó or ú and ending ends in a, remove the a
			elif deireadh and litreacha_eile and litreacha_eile[-1] in ['ó', 'ú', 'o'] and deireadh[0] == 'a':
				deireadh = deireadh[1:]
			elif deireadh and comhair_siollaí(briathar) == 1 and (deireadh[0] == 't' or deireadh[0] == 'f') and fréamh[-1] == 'é':
				deireadh = f"i{deireadh}"
			# analytic 3rd person plural Munster forms that would normally end in an lenited d end in an unlenited d instead 
			if mumhan and foirm == Foirm.scartha and forainm == 'siad' and deireadh[-3:] == 'idh':
				deireadh = deireadh[:-1]

			# if we didn't specify if pronouns should be shown or not
			# then show them unless we're using a synthetic form
			if forainmnigh is False or forainmnigh is None and foirm == Foirm.táite:
				forainm = ''

			if aibhsiú:
				focal = f"{aibhsigh(réimnír)}{céad_litir}{aibhsigh(s)}{litreacha_eile}{aibhsigh(deireadh)}"
				aschur.append(f"{mír and mír + ' ' or ''}{focal}{forainm and ' ' + aibhsigh(forainm) or ''}")
			else:
				focal = f"{réimnír}{céad_litir}{s}{litreacha_eile}{deireadh}"
				aschur.append(f"{mír and mír + ' ' or ''}{focal}{forainm and ' ' + forainm or ''}")
		return aschur


# Person
class Pearsa:
	def __init__(self):
		self.uatha = None
		self.iorla = None


# Tense
class Aimsir:
	def __init__(self, ainm: str):
		self.ainm = ainm
		self.céad_phearsa = Pearsa()
		self.dara_pearsa = Pearsa()
		self.tríú_pearsa = Pearsa()
		self.deireadh_scartha = ""
		self.deireadh_scartha_mumhan = None
		self.briathar_saor = None
		self.dearfach = Leagan()
		self.diúltach = Leagan(mír='ní', séimhiú=True)
		self.ceisteach = Leagan(mír='an', urú=True)


# Conjugation
class Réimniú:
	def __init__(self):
		self.a_chaite = Aimsir("an aimsir chaite")
		self.a_gchaite = Aimsir("an aimsir ghnáthchaite")
		self.a_láith = Aimsir("an aimsir láithreach")
		self.a_fháist = Aimsir("an aimsir fháistineach")
		self.m_fosh = Aimsir("an modh foshuiteach")
		self.m_ord = Aimsir("an modh ordaitheach")
		self.m_coinn = Aimsir("an modh coinníollach")
		self.aimsirí = {FoghaAimsire.chaite: self.a_chaite,
		                FoghaAimsire.ghnáthchaite: self.a_gchaite,
		                FoghaAimsire.láithreach: self.a_láith,
		                FoghaAimsire.fháistineach: self.a_fháist,
		                FoghaAimsire.foshuiteach: self.m_fosh,
		                FoghaAimsire.ordaitheach: self.m_ord,
		                FoghaAimsire.coinníollach: self.m_coinn}

	# conjugate
	def réimnigh(self, fréamh: str, foghannaAimsirí: list, foghannaPearsana: list, foghannaFoirmeacha: list, mumhan: bool, aibhsigh: bool):
		aschur = []
		for a in foghannaAimsirí:
			aimsir = self.aimsirí.get(a)
			foirmeacha = []

			for f in foghannaFoirmeacha:
				if f == FoghaFoirme.dhearfach and aimsir.dearfach:
					foirmeacha.append(aimsir.dearfach)
				if f == FoghaFoirme.dhiúltach and aimsir.diúltach:
					foirmeacha.append(aimsir.diúltach)
				if f == FoghaFoirme.cheisteach and aimsir.ceisteach:
					foirmeacha.append(aimsir.ceisteach)

			deireadh = (mumhan and aimsir.deireadh_scartha_mumhan) and aimsir.deireadh_scartha_mumhan or aimsir.deireadh_scartha
			pearsana = []
			aschur_aimsire = {'ainm': aimsir.ainm, 'pearsana': pearsana}
			for p in foghannaPearsana:
				if p == FoghaPearsan.céad_uatha:
					pearsana.append(aimsir.céad_phearsa.uatha.réimnigh(fréamh, deireadh, foirmeacha, p.forainm, mumhan, aibhsigh))
				if p == FoghaPearsan.dara_uatha:
					pearsana.append(aimsir.dara_pearsa.uatha.réimnigh(fréamh, deireadh, foirmeacha, p.forainm, mumhan, aibhsigh))
				if p == FoghaPearsan.tríú_uatha:
					pearsana.append(aimsir.tríú_pearsa.uatha.réimnigh(fréamh, deireadh, foirmeacha, p.forainm, mumhan, aibhsigh))
				if p == FoghaPearsan.céad_iorla:
					pearsana.append(aimsir.céad_phearsa.iorla.réimnigh(fréamh, deireadh, foirmeacha, p.forainm, mumhan, aibhsigh))
				if p == FoghaPearsan.dara_iorla:
					pearsana.append(aimsir.dara_pearsa.iorla.réimnigh(fréamh, deireadh, foirmeacha, p.forainm, mumhan, aibhsigh))
				if p == FoghaPearsan.tríú_iorla:
					pearsana.append(aimsir.tríú_pearsa.iorla.réimnigh(fréamh, deireadh, foirmeacha, p.forainm, mumhan, aibhsigh))
				if p == FoghaPearsan.briathar_saor:
					pearsana.append(aimsir.briathar_saor.réimnigh(fréamh, deireadh, foirmeacha, p.forainm, mumhan, aibhsigh))
			aschur.append(aschur_aimsire)
		return aschur


# define conjugation rules
def déan_rialacha():
	# first conjugation
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
	céad_réimniú.a_chaite.briathar_saor      = Leagan(séimhiú=False, deireadh_tháite="(e)adh")

	céad_réimniú.a_chaite.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="(e)as")
	céad_réimniú.a_chaite.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="[a]is")
	céad_réimniú.a_chaite.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="(e)amair")
	céad_réimniú.a_chaite.dara_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="(e)abhair")
	céad_réimniú.a_chaite.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="(e)adar")
	céad_réimniú.a_chaite.briathar_saor.mumhan      = Leagan(séimhiú=False, deireadh_tháite="(e)adh")


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
	céad_réimniú.a_gchaite.briathar_saor.mumhan      = Leagan(séimhiú=False, deireadh_tháite="tí")


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


	céad_réimniú.m_fosh.deireadh_scartha = "[a](e)"
	céad_réimniú.m_fosh.dearfach  = Leagan(mír='go', urú=True)
	céad_réimniú.m_fosh.diúltach  = Leagan(mír='nár', séimhiú=True)
	céad_réimniú.m_fosh.ceisteach = None
	céad_réimniú.m_fosh.céad_phearsa.uatha = Leagan(foirm=Foirm.scartha)
	céad_réimniú.m_fosh.dara_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
	céad_réimniú.m_fosh.tríú_pearsa.uatha  = Leagan(foirm=Foirm.scartha)
	céad_réimniú.m_fosh.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]imid")
	céad_réimniú.m_fosh.dara_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
	céad_réimniú.m_fosh.tríú_pearsa.iorla  = Leagan(foirm=Foirm.scartha)
	céad_réimniú.m_fosh.briathar_saor      = Leagan(deireadh_tháite="t(e)ar")

	céad_réimniú.m_fosh.deireadh_scartha_mumhan = "(e)aidh"
	céad_réimniú.m_fosh.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="(e)ad")
	céad_réimniú.m_fosh.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="[a]ir")


	céad_réimniú.m_ord.deireadh_scartha = "(e)adh"
	céad_réimniú.m_ord.diúltach  = Leagan(mír='ná')
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
	céad_réimniú.m_coinn.briathar_saor.mumhan      = Leagan(séimhiú=False, deireadh_tháite="fí")


	# second conjugation
	dara_réimniú = deepcopy(céad_réimniú)

	dara_réimniú.a_chaite.céad_phearsa.iorla = Leagan(deireadh_tháite="[a]íomar")
	dara_réimniú.a_chaite.briathar_saor      = Leagan(séimhiú=False, deireadh_tháite="[a]íodh")

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

	dara_réimniú.a_láith.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="[a]ír")
	dara_réimniú.a_láith.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[a]ímíd")
	dara_réimniú.a_láith.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="[a]íd", forainmnigh=True)
	dara_réimniú.a_láith.briathar_saor.mumhan      = Leagan(deireadh_tháite="[a]íthear")

	dara_réimniú.a_fháist.deireadh_scartha = "[ó](eo)idh"
	dara_réimniú.a_fháist.céad_phearsa.iorla = Leagan(deireadh_tháite="[ó](eo)imid")
	dara_réimniú.a_fháist.briathar_saor      = Leagan(deireadh_tháite="[ó](eo)far")

	dara_réimniú.a_fháist.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="[ó](eo)d")
	dara_réimniú.a_fháist.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="[ó](eo)ir")
	dara_réimniú.a_fháist.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="[ó](eo)imíd")

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


	# first conjugation, special case for verbs ending in -igh
	céad_réimniú_igh = deepcopy(céad_réimniú)

	céad_réimniú_igh.a_chaite.céad_phearsa.iorla = Leagan(deireadh_tháite="íomar")
	céad_réimniú_igh.a_chaite.briathar_saor      = Leagan(deireadh_tháite="íodh")

	céad_réimniú_igh.a_chaite.céad_phearsa.uatha.mumhan = Leagan(deireadh_tháite="íos")
	céad_réimniú_igh.a_chaite.dara_pearsa.uatha.mumhan  = Leagan(deireadh_tháite="ís")
	céad_réimniú_igh.a_chaite.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="íomair")
	céad_réimniú_igh.a_chaite.dara_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="íobhair")
	céad_réimniú_igh.a_chaite.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="íodar")


	céad_réimniú_igh.a_gchaite.deireadh_scartha = "íodh"
	céad_réimniú_igh.a_gchaite.céad_phearsa.uatha = Leagan(deireadh_tháite="ínn")
	céad_réimniú_igh.a_gchaite.dara_pearsa.uatha  = Leagan(deireadh_tháite="iteá")
	céad_réimniú_igh.a_gchaite.céad_phearsa.iorla = Leagan(deireadh_tháite="ímis")
	céad_réimniú_igh.a_gchaite.tríú_pearsa.iorla  = Leagan(deireadh_tháite="ídís")
	céad_réimniú_igh.a_gchaite.briathar_saor      = Leagan(deireadh_tháite="ití")

	céad_réimniú_igh.a_gchaite.dara_pearsa.uatha.mumhan =  Leagan(deireadh_tháite="íthá")
	céad_réimniú_igh.a_gchaite.céad_phearsa.iorla.mumhan = Leagan(deireadh_tháite="ímís")
	céad_réimniú_igh.a_gchaite.tríú_pearsa.iorla.mumhan  = Leagan(deireadh_tháite="ídís")
	céad_réimniú_igh.a_gchaite.briathar_saor.mumhan      = Leagan(deireadh_tháite="ítí")


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

	return {1: céad_réimniú, 1.5: céad_réimniú_igh, 2: dara_réimniú}


# detect which conjugation a verb is part of
def cén_réimniú(briathar: str) -> Réimniú:
	if comhair_siollaí(briathar) > 1:
		if briathar[-3:] == 'igh' or briathar[-2:] in ['ir', 'il', 'in', 'is']:
			if briathar[-3:] not in ['áil', 'áin', 'óil', 'úir']:
				return déan_rialacha().get(2)
	if briathar[-3:] in ['igh', 'ígh'] and briathar[-4:] not in ['éigh', 'óigh', 'úigh', 'áigh'] and briathar[-5:] not in ['eoigh', 'uaigh']:
		return déan_rialacha().get(1.5)
	return déan_rialacha().get(1)


# print results
def priontáil_toradh(toradh: List, aibhsiú: bool = False):
	leithid_colún = {}
	for aimsir in toradh:
		for ró in aimsir['pearsana']:
			for i, cill in enumerate(ró):
				fad = len(neamhaibhsigh(cill))
				if leithid_colún.get(i) is None or fad > leithid_colún.get(i):
					leithid_colún[i] = fad
	for aimsir in toradh:
		# if more than one tense was specified, print the name of each tense
		if len(toradh) > 1:
			if aibhsiú:
				print(f"  {folínigh(aimsir['ainm'])}")
			else:
				print(f"  {aimsir['ainm']}")
		for ró in aimsir['pearsana']:
			líne = ""
			for i, cill in enumerate(ró):
				líne += cill + " " * (leithid_colún[i] - len(neamhaibhsigh(cill)) + 4)
			print(líne)
		# print an empty line between each tense
		if aimsir != toradh[-1]:
			print()


def réimnigh(briathar: str, aimsirí: list = FoghaAimsire, pearsana: list = FoghaPearsan, foirmeacha: list = FoghaFoirme, mumhan: bool = False, aibhsigh: bool = False):
	return cén_réimniú(briathar).réimnigh(briathar, aimsirí, pearsana, foirmeacha, mumhan, aibhsigh)


if __name__ == '__main__':
	from argparse import ArgumentParser

	parser = ArgumentParser()
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

	aimsirí = []
	foirmeacha = []
	pearsana = []

	# what tenses are we conjugating?
	if args.c:
		aimsirí.append(FoghaAimsire.chaite)
	if args.g:
		aimsirí.append(FoghaAimsire.ghnáthchaite)
	if args.l:
		aimsirí.append(FoghaAimsire.láithreach)
	if args.f:
		aimsirí.append(FoghaAimsire.fháistineach)
	if args.F:
		aimsirí.append(FoghaAimsire.foshuiteach)
	if args.o:
		aimsirí.append(FoghaAimsire.ordaitheach)
	if args.O:
		aimsirí.append(FoghaAimsire.coinníollach)
	# if no tense is specified show all
	if not aimsirí:
		aimsirí = FoghaAimsire

	# what forms are we showing?
	if args.d:
		foirmeacha.append(FoghaFoirme.dhearfach)
	if args.D:
		foirmeacha.append(FoghaFoirme.dhiúltach)
	if args.C:
		foirmeacha.append(FoghaFoirme.cheisteach)
	# if none of affirmative, negative or interrogative forms are specified, show all of them
	if not foirmeacha:
		foirmeacha = [FoghaFoirme.dhearfach, FoghaFoirme.dhiúltach, FoghaFoirme.cheisteach]

	# what persons are we using?
	briathar_saor = getattr(args, '0')
	céad_phearsa = getattr(args, '1')
	dara_pearsa = getattr(args, '2')
	tríú_pearsa = getattr(args, '3')
	uathar = args.u
	iolra = args.i
	# if no persons are specified show all
	gach_pearsana = not (céad_phearsa or dara_pearsa or tríú_pearsa) and not briathar_saor
	# if singular or plural are not specified show both
	uathar_agus_uathar = not (uathar or iolra)
	# if autonomous and either singular or plural is specified, but not 1st, 2nd or 3rd person
	# then enable 1st, 2nd and 3rd person forms as well as the autonomous forms
	if briathar_saor and not uathar_agus_uathar and not (céad_phearsa or dara_pearsa or tríú_pearsa):
		gach_pearsana = True
	if (gach_pearsana or céad_phearsa) and (uathar_agus_uathar or uathar):
		pearsana.append(FoghaPearsan.céad_uatha)
	if (gach_pearsana or dara_pearsa) and (uathar_agus_uathar or uathar):
		pearsana.append(FoghaPearsan.dara_uatha)
	if (gach_pearsana or tríú_pearsa) and (uathar_agus_uathar or uathar):
		pearsana.append(FoghaPearsan.tríú_uatha)
	if (gach_pearsana or céad_phearsa) and (uathar_agus_uathar or iolra):
		pearsana.append(FoghaPearsan.céad_iorla)
	if (gach_pearsana or dara_pearsa) and (uathar_agus_uathar or iolra):
		pearsana.append(FoghaPearsan.dara_iorla)
	if (gach_pearsana or tríú_pearsa) and (uathar_agus_uathar or iolra):
		pearsana.append(FoghaPearsan.tríú_iorla)
	if gach_pearsana or briathar_saor:
		pearsana.append(FoghaPearsan.briathar_saor)

	priontáil_toradh(réimnigh(args.briathar, aimsirí, pearsana, foirmeacha, args.m, args.a), args.a)
