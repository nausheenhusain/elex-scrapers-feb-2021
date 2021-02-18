## elex scrapers, feb 2021

# JSON Schema

Please follow the schemas outlined below when storing race, reporting_unit, and candidate objects in an elections spreadsheet's "data" column.

# Race object schema

```
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Race",
    "description": "A single race.",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "The name of a race."
        },
        "description": {
            "type": "string",
            "description": "The description of a race."
        },
        "election_date": {
            "type": "string",
            "description": "The election date of a race."
        },
        "market": {
            "type": "string",
            "description": "The product affiliate code of the market."
        },
        "uncontested": {
            "type": "boolean",
            "description": "The flag for if a race is uncontested."
        },
        "amendment": {
            "type": "boolean",
            "description": "The flag for if a race is an amendment."
        },
        "state_postal": {
            "type": "string",
            "description": "The two character state postal code."
        },
        "recount": {
            "type": "boolean",
            "description": "The flag for if a race is under a recount."
        }
    },
    "required": ["name", "election_date", "market"]
}
```

# Reporting Unit object schema

```
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Reporting Unit",
    "description": "A single reporting unit belonging to a race.",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "The name of a reporting unit."
        },
        "level": {
            "type": "string",
            "description": "Set to 'subunit' if the reporting unit is a child of a parent reporting unit."
        },
        "district_type": {
            "type": "string",
            "description": "Details about a reporting unit's district."
        },
        "state_postal": {
            "type": "string",
            "description": "The two character state postal code."
        },
        "geo_id": {
            "type": "string",
            "description": "The reporting unit's geographical identifier, or fips code."
        },
        "electoral_vote_total": {
            "type": "integer",
            "description": "The number of electoral votes belonging to a reporting unit."
        },
        "precincts_reporting": {
            "type": "integer",
            "description": "The number of precincts reporting."
        },
        "total_precincts": {
            "type": "integer",
            "description": "The total number of precincts belonging to a reporting unit."
        },
        "data_source_update_time": {
            "type": "string",
            "format": "date-time",
            "description": "The date and time data associated with a reporting unit was updated."
        }
    },
    "required": ["state_postal", "data_source_update_time"]
}
```

# Candidate object schema

```
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Candidate",
    "description": "A single candidate belonging to a reporting unit.",
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string",
            "description": "The candidate's first name."
        },
        "last_name": {
            "type": "string",
            "description": "The candidate's last name."
        },
        "middle_name": {
            "type": "string",
            "description": "The candidate's middle name."
        },
        "party": {
            "type": "string",
            "description": "The candidate's party affiliation."
        },
        "incumbent": {
            "type": "boolean",
            "description": "The flag for a candidate's incumbency status."
        },
        "ballot_order": {
            "type": "integer",
            "description": "The order the candidate should appear in the chart."
        },
        "vote_count": {
            "type": "integer",
            "description": "The number of votes cast for the candidate."
        },
        "delegate_count": {
            "type": "integer",
            "description": "The number of delegates the candidate has won."
        },
        "electoral_vote_count": {
            "type": "integer",
            "description": "The number of electoral votes the candidate has won."
        },
        "winner": {
            "type": "boolean",
            "description": "The flag for if a candidate has won the race."
        },
        "runoff": {
            "type": "boolean",
            "description": "The flag for if the candidate will be in a runoff election."
        }
    },
    "required": []
}
```
