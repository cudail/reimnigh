#!/usr/bin/env python

# © 2020 Caoimhe Ní Chaoimh
# CC BY-NC-SA 4.0

from glob import glob
import json
import subprocess
import unittest
import reimnigh

datadir = "test/BuNaMo/verb"  # submodule with grammar database
gramadoir_exe = "test/gramadoir"  # test utility for processing data from above datasource

# réimnigh and the gramadóir app output things in a slightly different format
# so these are a few mappings to translate between them
tensemap = {
	"an aimsir chaite": "Past",
	"an aimsir ghnáthchaite": "PastCont",
	"an aimsir láithreach": "PresCont",
	"an aimsir fháistineach": "Fut",
	"an modh coinníollach": "Cond",
	"an modh foshuiteach": "Subj",
	"an modh ordaitheach": "Imper",
}
personmap = ["Sg1", "Sg2", "Sg3Fem", "Pl1", "Pl2", "Pl3", "Auto"]
shapemap = ["Declar", "Declar", "Interrog"]
polmap = ["Pos", "Neg", "Pos"]

# Don't test against these
irregular_verbs = ["abair", "beir", "bí", "clois", "déan", "faight", "feic", "ith", "tabhair", "tar", "téigh"]


class ReimnightTests(unittest.TestCase):
	def test_conjugation(self):
		files = glob(f"{datadir}/*_verb.xml")
		for file in files:
			jsondata = subprocess.run([gramadoir_exe, file], stdout=subprocess.PIPE)
			dictionary = json.loads(jsondata.stdout.decode('utf-8'))
			verb = dictionary['verbName']
			if verb in irregular_verbs:
				continue  # ignore irregular verbs
			with self.subTest(verb=verb):
				output = reimnigh.réimnigh(verb)
				for tense in output:
					for p, person in enumerate(tense['pearsana']):
						for f, form in enumerate(person):
							entries = [e for e in dictionary['forms'] if
								e['tense'] == tensemap.get(tense['ainm']) and
								e['person'] == personmap[p] and
								e['shape'] == shapemap[f] and
								e['polarity'] == polmap[f]]
							if not entries:
								continue  # some verbs in BuNaMo dataset seem to be missing past tense autonomous forms?
							# réimnigh outputs first person singular as one line, so we need to fix it a little
							if form.endswith('sí/sé'):
								form = form[:-3]
							# There may be multiple entries for a given form, e.g. brisimid/briseann muid
							# This will only validate against the first one
							expected = entries[0]['value']
							self.assertEqual(expected, form, f"{verb}: expected form '{expected}', actual output: '{form}'")


if __name__ == '__main__':
	unittest.main()
