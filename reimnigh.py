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


def uraigh(litir:str)->str:
	if is_guta(litir):
		return 'n-'
	return {'b':'m', 'c':'g', 'd':'n', 'f':'bh', 'g':'n', 'p':'b', 't':'d'}.get(litir)

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
	             mír:str='', urú:bool=False, séimhiú:bool=False,
	             forainm:bool=False, gearr:bool=True, leathan:str="", caol:str=""):
		self.mír=mír
		self.urú=urú
		self.séimhiú=séimhiú
		self.gearr=gearr
		self.leathan=leathan
		self.caol=caol
		self.forainm=forainm
	def réimnigh(self, briathar, forainm=""):
		if briathar[-4:] == 'aigh':
			fréamh = briathar[:-4]
		elif briathar[-3:] == 'igh':
			fréamh = briathar[:-3]
		else:
			fréamh = briathar

		céad_litir = briathar[0]
		litreacha_eile = self.gearr and fréamh[1:] or briathar[1:]

		m = self.mír and f"{self.mír} " or ''
		u = self.urú and uraigh(céad_litir) or ''
		s = self.séimhiú and is_inséimhithe(céad_litir) and 'h' or ''
		if self.mír == 'do':
			m = (is_guta(céad_litir) or (céad_litir=='f' and s=='h')) and "d'" or ""

		d = is_caol(fréamh) and self.caol or self.leathan
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
céad_réimniú.a_chaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, leathan='amar', caol='eamar')
céad_réimniú.a_chaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, forainm=True)
céad_réimniú.a_chaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, forainm=True)
céad_réimniú.a_chaite.briathar_saor =      Leagan(leathan='adh', caol='eadh')

céad_réimniú.a_gchaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, leathan='ainn', caol='inn')
céad_réimniú.a_gchaite.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, leathan='tá', caol='teá')
céad_réimniú.a_gchaite.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, leathan='adh', caol='eadh', forainm=True)
céad_réimniú.a_gchaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, leathan='aimis', caol='imis')
céad_réimniú.a_gchaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, leathan='adh', caol='eadh', forainm=True)
céad_réimniú.a_gchaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, leathan='aidís', caol='idís')
céad_réimniú.a_gchaite.briathar_saor =      Leagan(mír='do', séimhiú=True, leathan='taí', caol='tí')

céad_réimniú.a_láith.céad_phearsa.uatha = Leagan(leathan='aim', caol='im')
céad_réimniú.a_láith.dara_pearsa.uatha =  Leagan(leathan='ann', caol='eann', forainm=True)
céad_réimniú.a_láith.tríú_phearsa.uatha = Leagan(leathan='ann', caol='eann', forainm=True)
céad_réimniú.a_láith.céad_phearsa.iorla = Leagan(leathan='aimid', caol='imid')
céad_réimniú.a_láith.dara_pearsa.iorla =  Leagan(leathan='ann', caol='eann', forainm=True)
céad_réimniú.a_láith.tríú_phearsa.iorla = Leagan(leathan='ann', caol='eann', forainm=True)
céad_réimniú.a_láith.briathar_saor =      Leagan(leathan='tar', caol='tear')

céad_réimniú.a_fháist.céad_phearsa.uatha = Leagan(leathan='faidh', caol='fidh', forainm=True)
céad_réimniú.a_fháist.dara_pearsa.uatha =  Leagan(leathan='faidh', caol='fidh', forainm=True)
céad_réimniú.a_fháist.tríú_phearsa.uatha = Leagan(leathan='faidh', caol='fidh', forainm=True)
céad_réimniú.a_fháist.céad_phearsa.iorla = Leagan(leathan='faimid', caol='fimid')
céad_réimniú.a_fháist.dara_pearsa.iorla =  Leagan(leathan='faidh', caol='fidh', forainm=True)
céad_réimniú.a_fháist.tríú_phearsa.iorla = Leagan(leathan='faidh', caol='fidh', forainm=True)
céad_réimniú.a_fháist.briathar_saor =      Leagan(leathan='far', caol='fear')

céad_réimniú.m_fosh.céad_phearsa.uatha = Leagan(mír="go", urú=True, leathan="a", caol="e", forainm=True)
céad_réimniú.m_fosh.dara_pearsa.uatha =  Leagan(mír="go", urú=True, leathan="a", caol="e", forainm=True)
céad_réimniú.m_fosh.tríú_phearsa.uatha = Leagan(mír="go", urú=True, leathan="a", caol="e", forainm=True)
céad_réimniú.m_fosh.céad_phearsa.iorla = Leagan(mír="go", urú=True, leathan="aimid", caol="imid")
céad_réimniú.m_fosh.dara_pearsa.iorla =  Leagan(mír="go", urú=True, leathan="a", caol="e", forainm=True)
céad_réimniú.m_fosh.tríú_phearsa.iorla = Leagan(mír="go", urú=True, leathan="a", caol="e", forainm=True)
céad_réimniú.m_fosh.briathar_saor =      Leagan(mír="go", urú=True, leathan="tar", caol="tear")

céad_réimniú.m_ord.céad_phearsa.uatha = Leagan(leathan="aim", caol="im")
céad_réimniú.m_ord.dara_pearsa.uatha =  Leagan()
céad_réimniú.m_ord.tríú_phearsa.uatha = Leagan(leathan="adh", caol="eadh", forainm=True)
céad_réimniú.m_ord.céad_phearsa.iorla = Leagan(leathan="aimis", caol="imis")
céad_réimniú.m_ord.dara_pearsa.iorla =  Leagan(leathan="aigí", caol="igí")
céad_réimniú.m_ord.tríú_phearsa.iorla = Leagan(leathan="aidís", caol="idís")
céad_réimniú.m_ord.briathar_saor =      Leagan(leathan="tar", caol="tear")

céad_réimniú.m_coinn.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, leathan="fainn", caol="finn")
céad_réimniú.m_coinn.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, leathan="fá", caol="feá")
céad_réimniú.m_coinn.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, leathan="fadh", caol="feadh", forainm=True)
céad_réimniú.m_coinn.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, leathan="faimis", caol="fimis")
céad_réimniú.m_coinn.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, leathan="fadh", caol="feadh", forainm=True)
céad_réimniú.m_coinn.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, leathan="faidís", caol="fidís")
céad_réimniú.m_coinn.briathar_saor =      Leagan(mír='do', séimhiú=True, leathan="faí", caol="fí")

dara_réimniú.a_chaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, gearr=False, forainm=True)
dara_réimniú.a_chaite.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, gearr=False, forainm=True)
dara_réimniú.a_chaite.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, gearr=False, forainm=True)
dara_réimniú.a_chaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, leathan='aíomar', caol='íomar')
dara_réimniú.a_chaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, gearr=False, forainm=True)
dara_réimniú.a_chaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, gearr=False, forainm=True)
dara_réimniú.a_chaite.briathar_saor =      Leagan(leathan='aíodh', caol='íodh')

dara_réimniú.a_gchaite.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, leathan='aínn', caol='ínn')
dara_réimniú.a_gchaite.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, leathan='aíteá', caol='íteá')
dara_réimniú.a_gchaite.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, leathan='aíodh', caol='íodh', forainm=True)
dara_réimniú.a_gchaite.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, leathan='aímis', caol='ímis')
dara_réimniú.a_gchaite.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, leathan='aíodh', caol='íodh', forainm=True)
dara_réimniú.a_gchaite.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, leathan='aídís', caol='ídís')
dara_réimniú.a_gchaite.briathar_saor =      Leagan(mír='do', séimhiú=True, leathan='aítí', caol='ítí')

dara_réimniú.a_láith.céad_phearsa.uatha = Leagan(leathan='aím', caol='ím')
dara_réimniú.a_láith.dara_pearsa.uatha =  Leagan(leathan='aíonn', caol='íonn', forainm=True)
dara_réimniú.a_láith.tríú_phearsa.uatha = Leagan(leathan='aíonn', caol='íonn', forainm=True)
dara_réimniú.a_láith.céad_phearsa.iorla = Leagan(leathan='aímid', caol='ímid')
dara_réimniú.a_láith.dara_pearsa.iorla =  Leagan(leathan='aíonn', caol='íonn', forainm=True)
dara_réimniú.a_láith.tríú_phearsa.iorla = Leagan(leathan='aíonn', caol='íonn', forainm=True)
dara_réimniú.a_láith.briathar_saor =      Leagan(leathan='aítear', caol='ítear')

dara_réimniú.a_fháist.céad_phearsa.uatha = Leagan(leathan='óidh', caol='eoidh', forainm=True)
dara_réimniú.a_fháist.dara_pearsa.uatha =  Leagan(leathan='óidh', caol='eoidh', forainm=True)
dara_réimniú.a_fháist.tríú_phearsa.uatha = Leagan(leathan='óidh', caol='eoidh', forainm=True)
dara_réimniú.a_fháist.céad_phearsa.iorla = Leagan(leathan='óimid', caol='eoimid')
dara_réimniú.a_fháist.dara_pearsa.iorla =  Leagan(leathan='óidh', caol='eoidh', forainm=True)
dara_réimniú.a_fháist.tríú_phearsa.iorla = Leagan(leathan='óidh', caol='eoidh', forainm=True)
dara_réimniú.a_fháist.briathar_saor =      Leagan(leathan='ófar', caol='eofar')

dara_réimniú.m_fosh.céad_phearsa.uatha = Leagan(mír="go", urú=True, leathan="aí", caol="í", forainm=True)
dara_réimniú.m_fosh.dara_pearsa.uatha =  Leagan(mír="go", urú=True, leathan="aí", caol="í", forainm=True)
dara_réimniú.m_fosh.tríú_phearsa.uatha = Leagan(mír="go", urú=True, leathan="aí", caol="í", forainm=True)
dara_réimniú.m_fosh.céad_phearsa.iorla = Leagan(mír="go", urú=True, leathan="aímid", caol="ímid")
dara_réimniú.m_fosh.dara_pearsa.iorla =  Leagan(mír="go", urú=True, leathan="aí", caol="í", forainm=True)
dara_réimniú.m_fosh.tríú_phearsa.iorla = Leagan(mír="go", urú=True, leathan="aí", caol="í", forainm=True)
dara_réimniú.m_fosh.briathar_saor =      Leagan(mír="go", urú=True, leathan="aítear", caol="ítear")

dara_réimniú.m_ord.céad_phearsa.uatha = Leagan(leathan="aím", caol="ím")
dara_réimniú.m_ord.dara_pearsa.uatha =  Leagan(gearr=False)
dara_réimniú.m_ord.tríú_phearsa.uatha = Leagan(leathan="aíodh", caol="íodh", forainm=True)
dara_réimniú.m_ord.céad_phearsa.iorla = Leagan(leathan="aímis", caol="ímis")
dara_réimniú.m_ord.dara_pearsa.iorla =  Leagan(leathan="aígí", caol="ígí")
dara_réimniú.m_ord.tríú_phearsa.iorla = Leagan(leathan="aídís", caol="ídís")
dara_réimniú.m_ord.briathar_saor =      Leagan(leathan="aítear", caol="ítear")

dara_réimniú.m_coinn.céad_phearsa.uatha = Leagan(mír='do', séimhiú=True, leathan="óinn", caol="eoinn")
dara_réimniú.m_coinn.dara_pearsa.uatha =  Leagan(mír='do', séimhiú=True, leathan="ófá", caol="eofá")
dara_réimniú.m_coinn.tríú_phearsa.uatha = Leagan(mír='do', séimhiú=True, leathan="ódh", caol="eodh", forainm=True)
dara_réimniú.m_coinn.céad_phearsa.iorla = Leagan(mír='do', séimhiú=True, leathan="óimis", caol="eoimis")
dara_réimniú.m_coinn.dara_pearsa.iorla =  Leagan(mír='do', séimhiú=True, leathan="ódh", caol="eodh", forainm=True)
dara_réimniú.m_coinn.tríú_phearsa.iorla = Leagan(mír='do', séimhiú=True, leathan="óidís", caol="eoidís")
dara_réimniú.m_coinn.briathar_saor =      Leagan(mír='do', séimhiú=True, leathan="ófaí", caol="eofaí")

print(briathar)
print()

if briathar[-3:] == 'igh':
	dara_réimniú.réimnigh(briathar)
else:
	céad_réimniú.réimnigh(briathar)
