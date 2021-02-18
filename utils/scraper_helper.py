##
## Helper module, election Feb 2021
## This is written in Python3.
##

from datetime import datetime, timezone

def get_name(full_name, first, middle, last):
	# print('hello from helper')
	if len(full_name) == 1:
		first = ""
		middle = ""
		last = full_name[0][0]
	elif len(full_name) == 2:
		first = full_name[0][0]
		middle = ""
		last = full_name[1][0]
	elif len(full_name) == 3:
		first = full_name[0][0]
		middle = full_name[1][0]
		last = full_name[2][0]
	elif len(full_name) == 4:
		first = full_name[0][0]
		middle = full_name[1][0]
		last = full_name[2][0]+" "+full_name[3][0]
	return first.title(), middle.title(), last.title()

# Format of race object for use in TribPub's Google Sheet
def initialize_race_obj(name,reporting,total, countyname):
	race_obj = {
		"name": name.title(),
		"description": "",
		"election_date": "2021-02-23",
		"market": "chinews",
		"uncontested": False,
		"amendment": bool(False),
		"state_postal": "IL",
		"recount": False,
		"reporting_units": [
			{
				"name": countyname,
				"level": "county",
				"district_type": "",
				"state_postal": "IL",
				"geo_id": "",
				"electoral_vote_total": 0,
				"precincts_reporting": int(reporting),
				"total_precincts": int(total),
				"data_source_update_time": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z'),
				"candidates": []
			}
		]
	}
	return race_obj	