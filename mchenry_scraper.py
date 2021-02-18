##
## McHenry scraper, election 2021
## This is written in Python3.
##

from datetime import datetime, timezone
import json
import probablepeople as pp
import requests
from scrapers.utils.scraper_helper import get_name, initialize_race_obj
from urllib.request import urlopen

def parse_name(fullname):
	first, middle, last = "","",""
	return get_name(fullname,first,middle,last)

def get_results_url():

	## gets current version of results URL
	GET_VERSION = 'https://results.enr.clarityelections.com//IL/McHenry/105201/current_ver.txt'
	version = requests.get(GET_VERSION).json()
	curr_ver = str(version)
	build_results_url = str('https://results.enr.clarityelections.com//IL/McHenry/105201/'+curr_ver+'/json/en/summary.json')
	print(build_results_url)
	
	return build_results_url

def get_precincts_url():
	
	## gets current version of precincts URL
	GET_VERSION = 'https://results.enr.clarityelections.com//IL/McHenry/105201/current_ver.txt'
	version = requests.get(GET_VERSION).json()
	curr_ver = str(version)
	build_precincts_url = str('https://results.enr.clarityelections.com//IL/McHenry/105201/'+curr_ver+'/json/en/electionsettings.json')
	print(build_precincts_url)
	
	return build_precincts_url

def scrape_mchenry():

	COUNTY_NAME = "McHenry"
	# URLs
	MCHENRY_RACE_URL = get_results_url()
	PRECINCTS_URL = get_precincts_url()
	
	data = requests.get(MCHENRY_RACE_URL).json()
	precincts_data = requests.get(PRECINCTS_URL).json()
	
	# gets precinct info
	precincts_reporting = precincts_data['settings']['numberofprecinctsreporting']
	precincts_total = precincts_data['settings']['totalprecinctsreporting']
	
	mchenry_county_results = []

	for datum in data:

		if datum['CAT'] == 'County' and datum['SUBCAT'] == 'Questions':
			options = datum['CH']
			votes = datum['V']
			race_name = datum['C']

			race_obj = initialize_race_obj(datum['C'],precincts_reporting,precincts_total,COUNTY_NAME)

			for option_index, (option, vote) in enumerate(zip(options, votes)):
				
				race_obj["reporting_units"][0]['candidates'].append({
					"first_name": "",
					"middle_name": "",
					"last_name": option.title(),
					"vote_count": int(vote),
					"ballot_order": int(option_index + 1)
				})

			mchenry_county_results.append(race_obj)

		elif datum['CAT'] == "County" and datum['SUBCAT'] != "Questions":
			candidates = datum['CH']
			cand_votes = datum['V']
			cand_parties = datum['P']
		
			race_name = datum['C']

			race_obj = initialize_race_obj(datum['C'],precincts_reporting,precincts_total,COUNTY_NAME)

			for cand_index, (candidate, cand_vote, cand_party) in enumerate(zip(candidates, cand_votes, cand_parties)):
				full_name = pp.parse(candidate, 'person') # uses probablepeople to parse names into a list
				first_name, middle_name, last_name = parse_name(full_name)

				race_obj["reporting_units"][0]['candidates'].append({
					"first_name": first_name,
					"middle_name": middle_name,
					"last_name": last_name,
					"vote_count": int(cand_vote),
					"party": cand_party,
					"ballot_order": int(cand_index + 1)
				})

			mchenry_county_results.append(race_obj)

	with open('scrapers/mchenry_data.json', 'w', encoding='utf-8') as f:
		json.dump(mchenry_county_results, f, ensure_ascii=False, indent=4)

	return mchenry_county_results

# this should be commented out when running the app
# leave it in if you're just testing the scraper
# scrape_mchenry()