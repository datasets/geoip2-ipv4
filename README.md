<a className="gh-badge" href="https://datahub.io/core/geoip2-ipv4"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Database of IPv4 address networks with their respective geographical location.

## Data

Based on GeoLite2 Country Free Downloadable Databases as of Apr 21, 2015 http://dev.maxmind.com/geoip/geoip2/geolite2/

Two files were used to generate this dataset: 

```
GeoLite2-Country-Blocks-IPv4.csv  
GeoLite2-Country-Locations-en.csv  
```

with the following considerations:  

- Where geoname_id was not available, registered_country_geoname_id was used.
- Where geoname_id and registered_country_geoname_id where empty, geoname_id, continent_code, continent_name, country_iso_code and country_name are empty.

## Preparation

Process is recorded and automated in python script:

```bash
# Install the requirements
pip install -r scripts/requirements.txt

# Make sure to add your own Account_ID and License_key password as env variables
username = os.getenv('MAXMIND_USERNAME')
password = os.getenv('MAXMIND_PASSWORD')

# Run the code 
python scripts/process.py
```

## Automation
Up-to-date (auto-updates every week) geoip2-ipv4 dataset could be found on the datahub.io: https://datahub.io/core/geoip2-ipv4

## License

Datapackage: Creative Commons Zero 

Original CSV: This dataset includes GeoLite2 data created by MaxMind, available from www.maxmind.com
