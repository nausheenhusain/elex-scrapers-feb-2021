##
## Kane scraper, election Feb 2021
## This is written in Python3.
##

from bs4 import BeautifulSoup
from datetime import datetime, timezone
import json
import probablepeople as pp
import re
import requests
import urllib.request
import urllib.parse
from scrapers.utils.scraper_helper import get_name, initialize_race_obj

# RESULTS_URL = 'http://electionresults.countyofkane.org/Contests.aspx?Id=24'

def parse_name(fullname):
## get_name in utils

	first, middle, last = "","",""
	return get_name(fullname,first,middle,last)

def get_results_url():
## gets results URL

	KANE_RACE_URL = 'http://electionresults.countyofkane.org/Contests.aspx?Id=24'
	html = urllib.request.urlopen(KANE_RACE_URL).read()
	soup = BeautifulSoup(html, 'html.parser')
	
	return soup

def scrape_kane():

	COUNTY_NAME = "Kane County"
	kane_data = get_results_url()
	
	# creates empty list for results info
	kane_county_results = []

	race_data = kane_data.findAll("h2") # h2 gets each race name, findPrevious/Next/Children is based on this
	for race in race_data:
		candidates = []
		votes = []

		# finds precincts reporting and total precincts
		finding_precincts_info = race.findPrevious('td')
		precincts_info = finding_precincts_info.findPrevious('td')
		precincts = list(map(int, re.findall(r'\d+', str(precincts_info)))) # gets integers from precincts line, makes list
		precincts_reporting = precincts[0]
		precincts_total = precincts[1]
		# print(precincts_reporting, precincts_total)

		cands = race.findNext('table')
		names = cands.findChildren('td')
		for name in names:
			name = str(name)
			if name.startswith('<td>'):
				# splits may be necessary to pinpoint just name
				# appends each name to candidates list
				if '(Write-In)' in name:
					name = name.split('<b>', 2)
					name_split = name[0]
					cand_name_split = name_split.split('>', 2)
					cand_name = cand_name_split[1]
					candidates.append(cand_name)
					# print('appended', cand_name)
				elif '(Independent)' in name or '(Democratic)' in name or '(Republican)' in name:
					candidate_split = name.rsplit('(', 1)
					candidate = candidate_split[0]
					cand_name_split = candidate.split('>', 1)
					cand_name = cand_name_split[1]
					candidates.append(cand_name)
					# print(cand_name)
				else:
					name_split = name.split('>', 2)
					name_split = str(name_split[1])
					final_name = name_split.split('</', 2)
					cand_name = final_name[0]
					candidates.append(cand_name)
					# print('appended', cand_name)
			if '<b>' in name:
				name_split = name.split('</b>', 2)
				name_split = str(name_split[0])
				final_name = name_split.split('<b>', 2)
				if '%' not in final_name[1]:
					# separates vote percentages from vote counts
					# appends votes to votes list
					cand_votes = final_name[1]
					votes.append(cand_votes)
					# print('appended', cand_votes)
		
		race = str(race)
		race_split = race.split('<br/>', 2)
		race_split = race_split[0]
		final_race_name = race_split.split('>', 2)
		race_name = final_race_name[1]

		# creates object in format of race object for use in TribPub's Google Sheet
		race_obj = initialize_race_obj(race_name,precincts_reporting,precincts_total,COUNTY_NAME)

		for option_index, (candidate, vote) in enumerate(zip(candidates, votes)):
			full_name = pp.parse(candidate, 'person') # uses probablepeople to parse names into a list
			first_name, middle_name, last_name = parse_name(full_name)
			
			race_obj["reporting_units"][0]['candidates'].append({
				"first_name": first_name,
				"middle_name": middle_name,
				"last_name": last_name,
				"vote_count": int(vote),
				"ballot_order": int(option_index + 1)
			})

		kane_county_results.append(race_obj)

	with open('scrapers/kane_data.json', 'w', encoding='utf-8') as f:
		json.dump(kane_county_results, f, ensure_ascii=False, indent=4)

	return kane_county_results
	
# this should be commented out when running the app
# leave it in if you're just testing the scraper	
# scrape_kane()