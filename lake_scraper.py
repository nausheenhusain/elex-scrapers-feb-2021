##
## Lake scraper, election 2021
## This is written in Python3.
##

from datetime import datetime, timezone
import json
import probablepeople as pp
from urllib.request import urlopen
import requests
from scrapers.utils.scraper_helper import get_name, initialize_race_obj

# RESULTS_URL = 'https://results.enr.clarityelections.com/IL/Lake/108200/web.274956/#/summary'

def parse_name(fullname):
	first, middle, last = "","",""
	return get_name(fullname,first,middle,last)

def get_results_url():

	## gets current version of results URL
	GET_VERSION = 'https://results.enr.clarityelections.com//IL/Lake/108200/current_ver.txt'
	version = requests.get(GET_VERSION).json()
	curr_ver = str(version)
	build_results_url = str('https://results.enr.clarityelections.com//IL/Lake/108200/'+curr_ver+'/json/en/summary.json')
	
	return build_results_url

def get_precincts_url():
	
	## gets current version of precincts URL
	GET_VERSION = 'https://results.enr.clarityelections.com//IL/Lake/108200/current_ver.txt'
	version = requests.get(GET_VERSION).json()
	curr_ver = str(version)
	build_precincts_url = str('https://results.enr.clarityelections.com//IL/Lake/108200/'+curr_ver+'/json/en/electionsettings.json')
	
	return build_precincts_url


def scrape_lake():

	COUNTY_NAME = "Lake County"
	# sets URLs
	LAKE_RACE_URL = get_results_url()
	PRECINCTS_URL = get_precincts_url()
	
	# gets data 
	data = requests.get(LAKE_RACE_URL).json()
	precincts_data = requests.get(PRECINCTS_URL).json()
	
	# gets precinct info
	precincts_reporting = precincts_data['settings']['numberofprecinctsreporting']
	precincts_total = precincts_data['settings']['totalprecinctsreporting']
	
	# creates empty list for results info
	lake_county_results = []

	for datum in data:
		race_name = datum['C']
		candidates = datum['CH']
		cand_votes = datum['V']
		cand_parties = datum['P']

		race_obj = initialize_race_obj(datum['C'],precincts_reporting,precincts_total,COUNTY_NAME)

		for cand_index, (candidate, cand_vote, cand_party) in enumerate(zip(candidates, cand_votes, cand_parties)):
			full_name = pp.parse(candidate, 'person') # uses probablepeople to parse names into a list
			first_name, middle_name, last_name = parse_name(full_name)

			# appends to candidates list
			race_obj["reporting_units"][0]['candidates'].append({
				"first_name": first_name,
				"middle_name": middle_name,
				"last_name": last_name,
				"vote_count": int(cand_vote),
				"ballot_order": int(cand_index + 1)
			})
			# print(race_obj)

		lake_county_results.append(race_obj)
		
		# print(lake_county_results)

	with open('scrapers/lake_data.json', 'w', encoding='utf-8') as f:
		json.dump(lake_county_results, f, ensure_ascii=False, indent=4)

	return lake_county_results

# this should be commented out when running the app
# leave it in if you're just testing the scraper
# scrape_lake()