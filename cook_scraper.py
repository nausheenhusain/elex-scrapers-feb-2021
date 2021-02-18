##
## Cook scraper, election 2021
## This is written in Python3.

# 0 race id (4 chars)
# 4 candidate id (3 chars)
# 7 precinct total (4 chars)
# 11 votes (7 chars)
# 18 completed precincts (4 chars)

## Made-up example:
## 0068001006100020400000
## 	0068 001   0061        0,0, 0, 2, 0, 4,0              0,0,0,0
##  0123 456   78910     11,12,13,14,15,16,17           18,19,20,21
##  race can   total            votes                  reported prec


import csv
from datetime import datetime, timezone
from ftplib import FTP_TLS
import json
import probablepeople as pp
import re
from urllib.request import urlopen
from scrapers.utils.scraper_helper import get_name, initialize_race_obj

def parse_name(fullname):
	first, middle, last = "","",""
	return get_name(fullname,first,middle,last)

def get_txtfile():
# gets relevant file from FTP server

	ftps = FTP_TLS("ftps.cookcountyclerk.com")
	ftps.login(user='reporters',passwd='R3p047')
	ftps.prot_p()
	ftps.getwelcome()
	ftps.dir()
	print('getting new txt file')
	with open('scrapers/updated_cook.txt', 'wb') as new_results: # this should create a new file called updated_cook.txt
		ftps.retrbinary('RETR ' + 'SummaryExport.txt', new_results.write) # confirm the name of the file that will have updated results
	print('exiting server')
	ftps.quit()

def scrape_cook():
	
	## This scraper loops through the results txt data (SummaryExport.txt) and matches only with data from cook-IDs.csv. 
	## It only adds in the race_obj if the race name doesn't exist in `added`,
	## which starts as an empty list. Within that for loop exists another for+if loop that loops through the
	## `cook_county_results` list and adds the current race's candidate info.

	get_txtfile()

	COUNTY_NAME = "Cook County"
	cook_county_results = []
	added = []

	with open('scrapers/cook-IDs.csv', newline='') as f:
		reader = csv.reader(f)
		cook_info = list(reader)
	with open('scrapers/updated_cook.txt','r') as r: # should be name of newly-written file
		results_data = r.readlines()

	# This matches results races to dict races by the first seven characters of the record.
	for results_row in results_data:
		current_ID_match = results_row[0:7] #RESULTS
		for info_line in cook_info:
			full_ID_match = info_line[0][0:7] #CONTEXT
			
			if current_ID_match == full_ID_match:
				
				full_ID = info_line[0]
				race_name = info_line[1].title()
				candidate = info_line[2]
				full_name = pp.parse(candidate, 'person') # uses probablepeople to parse names into a list
				
				first_name, middle_name, last_name = parse_name(full_name)
				
				precincts_total = int(results_row[7:11])
				vote_count = int(results_row[11:18])
				precincts_reporting = int(results_row[18:22])
				cand_party = full_ID[22:25]
				ballot_order = int(info_line[0][4:7])

				if race_name not in added:
					# creates object in format of race object for use in TribPub's Google Sheet
					race_obj = initialize_race_obj(race_name,precincts_reporting,precincts_total,COUNTY_NAME)
					cook_county_results.append(race_obj)
					added.append(race_name)
				else:
					pass

				for item in cook_county_results:
					if item['name'] == race_name.title():
						first_name, middle_name, last_name = parse_name(full_name)
						
						item['reporting_units'][0]['candidates'].append({
						"first_name": first_name,
						"middle_name": middle_name,
						"last_name": last_name,
						"vote_count": int(vote_count),
						"ballot_order": int(ballot_order)
					})
					else:
						pass
			else:
				pass
	
	# print(cook_county_results)

	with open('scrapers/cook_data.json', 'w', encoding='utf-8') as f:
		json.dump(cook_county_results, f, ensure_ascii=False, indent=4)

	return cook_county_results

# this should be commented out when running the app
# leave it in if you're just testing the scraper
# scrape_cook()