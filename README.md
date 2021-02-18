# TribPub election scraper template

This is a [Serverless](https://serverless.com/) template for creating scrapers that feed into Tribune Publishing's election results system. 

The project relies on the Serverless framework, which wraps scrapers in AWS Lambda functions and handles deployment and cron-like scheduling of the scripts.

This template is meant to provide flexibility to local markets to use the methods and libraries they need to retrieve data, while including helper functions to ensure scraped data adheres to the schema used universally.

Fetched data should be transformed to JSON that can be passed to the template's Google Sheet loader helper. See the [example data](example_data.json) for how data should look.


## Requirements
1. **Serverless**: The Node-based tool can be installed with: `npm install -g serverless`

2. **OAuth credentials for your Google Sheet**: Store credentials for the Google account that owns the sheet with results in `config/client_secrets.json`. Consult Ryan Asher for the credentials for your market's Google Sheet.
More on how it will be used here: https://gspread.readthedocs.io/en/latest/oauth2.html

3. **A Google Sheet formatted for election results**

4. **An AWS account and credentials**: Your credentials should be stored as environment variables so Serverless can deploy.

5. **Docker, for packaging python dependencies**: Download and install from https://www.docker.com/products/docker-desktop


## Project setup
1. You'll need to update your `config/client_secrets.json` with your Google account secrets that have access to your Google Sheet.
2. The Node plugin `serverless-python-requrements` is required and is defined in package.json, so install that with `npm install`
3. Make sure to update your config variables as defined in the [Configuration](#Configuration) section.
    - As part of this: **Make sure to change your service name to be specific to your project**. (Replace "palm-beach-county-scraper")

## Creating a new scraper
Run the following commands to use the Serverless CLI to create a new scraper project from this template.

```bash
$ serverless create -u https://diggit.int.tribops.com/achokey/election-results-scraper-template.git -p my_scraper
```

Create a virtual environment and install python and Node dependencies.

Included is a [scrapers](scrapers/) directory where you can house scrapers and related functions for your project if you prefer. The returned data should be in [this format](example_data.json).

Then edit the [handler.py](handler.py)'s `main` function to pass your scraped data as an argument for the `update_sheet` function.

> Make sure to save all your python requirements before deploying by running `pip freeze > requirements.txt`


## Configuration
Make sure to set preferences in the `serverless.yml` file, including:
- Lambda function preferences
    - The name of the function to be used when [running manually](#run-functions-manually).
    - The python version you want to use (Should be 3.x).
    - The cron/AWS schedule for how often to run functions.
- Environment variables
    - Abbreviation for the state to pull data for.
    - The election date
    - The preferred prefix for each object's `reference_id`.
    - News market code (`allnews`, `balnews`, `chinews`, `hartnews`, `nydn`, `orlnews`, `pilotonline`, `soflanews`).
    - The DDHQ API key (If using DDHQ API)
    - The Google Sheet spreadsheet key.


## Race name replacement feature
If your spreadsheet has data pre-populated before your results feeds are live (like a county results page that will be used on election night), race name might not match between your pre-loaded names and how they actually appear from your data sources on election night.

You can make that mapping by adding a file named `race_dictionary.csv`. This project will look for that file, find the race object in the scraped data, make the needed replacement names and then add them to the Google Sheet. The reference_ids will also be generated based on the replacement names, if any exist.



## Serverless commands

### Deployment
`serverless deploy -v`

### Run functions manually on your local machine
`serverless invoke local -f FUNCTION_NAME -l`

### Run functions manually from AWS Lambda (After deployment)
`serverless invoke -f FUNCTION_NAME -l`

### Remove the service from AWS
`serverless remove`

## Utilities

### Clear data from the sheet (Except headers and hidden rows)
`serverless invoke local -f clear_sheet`


## JSON Schema

Please follow the schemas outlined below when storing race, reporting_unit, and candidate objects in an elections spreadsheet's "data" column.

### Race object schema

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

### Reporting Unit object schema

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

### Candidate object schema

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
