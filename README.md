<a className="gh-badge" href="https://datahub.io/core/geoip2-ipv4"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

# IPv4 geolocation

IPv4 networks in CIDR notation with the country and continent that MaxMind's GeoLite2 Country database assigns to each. The location is at country level only.

Column definitions and types are in `datapackage.json`.

## Data

`data/geoip2-ipv4.csv` has one row per IPv4 network:

| Column | Meaning |
|---|---|
| `network` | IPv4 network in CIDR notation, for example `1.0.0.0/24`. Each network appears once |
| `geoname_id` | [GeoNames](https://www.geonames.org/) id of the location: the country, or a continent when MaxMind gives no country. Empty when the network has no location |
| `continent_code` | `AF`, `AN`, `AS`, `EU`, `NA` (North America), `OC` or `SA`. Empty when the network has no location |
| `continent_name` | Continent name, for example `Oceania` |
| `country_iso_code` | ISO 3166-1 alpha-2 country code, for example `AU`. Empty when the location is only a continent or unknown |
| `country_name` | English country name, for example `Australia` |
| `is_anonymous_proxy` | MaxMind's flag for an anonymous proxy: `1` or `0` |
| `is_satellite_provider` | MaxMind's flag for a satellite provider that serves several countries: `1` or `0` |

### Known limitations

* The codes `NA` are real values: `continent_code` `NA` is North America and `country_iso_code` `NA` is Namibia. Many tools read the text `NA` as "missing". Read the file as text and keep empty cells empty: `pd.read_csv("data/geoip2-ipv4.csv", dtype=str, keep_default_na=False)`.
* The location is the country, not a city or a street. MaxMind says IP geolocation is inherently imprecise, and its terms forbid using GeoLite data to identify a household, an individual or a street address.
* A few networks have only a continent: their `geoname_id` is the continent's id and the two country columns are empty.
* Where MaxMind gives a network no location of its own, the country where the network is registered is used. That country can differ from the country where the addresses are used.
* A network with neither has empty location columns.
* `is_anonymous_proxy` and `is_satellite_provider` are 0 in every row of the data we checked. Do not use them to find proxies or satellite networks.
* IPv4 only. There is no IPv6.

## Data sources

* [MaxMind GeoLite2 Country](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data/), CSV format: the networks (`GeoLite2-Country-Blocks-IPv4.csv`) and the locations (`GeoLite2-Country-Locations-en.csv`). Licence: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), as stated in the [GeoLite End User License Agreement](https://www.maxmind.com/en/geolite2/eula), with attribution required (see [License](#license)).

Changes made to the source data: the script joins the two files on `geoname_id`. Where a network has no `geoname_id`, it uses `registered_country_geoname_id`. It keeps the eight columns above, drops the other columns of the MaxMind files, and removes repeated rows.

Not endorsed by, or affiliated with, MaxMind.

## Preparation

You need Python 3.12 or greater and a free MaxMind GeoLite account with a licence key. Set your account id and key as environment variables, then run the script from the repository root:

```bash
pip install -r scripts/requirements.txt
export MAXMIND_USERNAME=<your account id>
export MAXMIND_PASSWORD=<your licence key>
python scripts/process.py
```

The script stops with an error if the download fails or if the result looks wrong (fewer than 100,000 networks, a repeated network, or the text `nan` in any column).

A GitHub workflow runs the script every Sunday at 00:00 UTC, on every push to `main` and when started by hand, with the account id and licence key stored as GitHub secrets. It commits `data/` if it changed.

The data is also published on [datahub.io](https://datahub.io/core/geoip2-ipv4).

## License

The data is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). MaxMind's [GeoLite End User License Agreement](https://www.maxmind.com/en/geolite2/eula) (updated 12 February 2026) says so in section 3: "to the extent the Services contain any copyrightable elements those copyrightable elements are governed by the Creative Commons License".

What this means for you:

* **Credit MaxMind.** The agreement says "You must provide attribution of your use to MaxMind", with the example: "This product includes GeoLite Data created by MaxMind, available from https://www.maxmind.com".
* **Share alike.** If you share a changed version of the data, CC BY-SA 4.0 requires you to share it under the same licence.
* **Keep the limits that come with the data.** Section 6 allows sharing where the Creative Commons licence permits it, and says the same duties pass on to whoever receives the data. Section 4 forbids using the data for credit, insurance or employment decisions. Section 5 forbids using it to identify a household, an individual or a street address.

**Old versions.** The agreement also says (section 6, "Destructions") that you must "cease use of and destroy ... any old versions of the Services within thirty (30) days following the release of the updated GeoLite Databases". This repository replaces the data every week and keeps the older versions in its Git history. Use the current file in `data/`, not an older version from the history.

The maintainers place only their own work (the script, the column definitions and the file layout) under the [Public Domain Dedication and License (PDDL)](https://opendatacommons.org/licenses/pddl/1.0/). The CC0 text in `LICENSE` is also only the maintainers' own dedication. Neither applies to the MaxMind data. See also [ATTRIBUTION.txt](ATTRIBUTION.txt).
