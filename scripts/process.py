import os
import sys
import shutil
import zipfile
import requests
import pandas as pd

perm_URL = 'https://download.maxmind.com/geoip/databases/GeoLite2-Country-CSV/download?suffix=zip'

## Register at the MaxMind website to get the license key for account_id and license_key

username = os.getenv('MAXMIND_USERNAME')
password = os.getenv('MAXMIND_PASSWORD')

zip_file_path = 'temp/GeoLite2-Country-CSV.zip'
output_path = 'data/geoip2-ipv4.csv'
ipv4 = 'GeoLite2-Country-Blocks-IPv4.csv'
location = 'GeoLite2-Country-Locations-en.csv'

col_list = ['network',
            'geoname_id',
            'continent_code',
            'continent_name',
            'country_iso_code',
            'country_name',
            'is_anonymous_proxy',
            'is_satellite_provider']


def read_csv(file):
    # Read everything as text and keep empty cells empty. pandas would otherwise turn
    # the code NA (North America, Namibia) into a missing value.
    return pd.read_csv(file, dtype=str, keep_default_na=False)


def merge_data(ipv4_df, location_df):
    ipv4_df = ipv4_df[['network',
                       'geoname_id',
                       'registered_country_geoname_id',
                       'is_anonymous_proxy',
                       'is_satellite_provider',
                       ]].copy()
    location_df = location_df[[
        'geoname_id',
        'continent_code',
        'continent_name',
        'country_iso_code',
        'country_name',
    ]]
    # Where geoname_id is empty, use registered_country_geoname_id
    ipv4_df['geoname_id'] = ipv4_df['geoname_id'].where(
        ipv4_df['geoname_id'] != '', ipv4_df['registered_country_geoname_id'])
    ipv4_df = ipv4_df.drop(columns=['registered_country_geoname_id'])
    # A network whose geoname_id is still empty has no location: its location columns stay empty
    merged = pd.merge(ipv4_df, location_df, on='geoname_id', how='left').fillna('')
    merged = merged[col_list].drop_duplicates()
    check(merged)
    merged.to_csv(output_path, index=False)
    print(f"{len(merged)} rows written to {output_path}")


def check(merged):
    if len(merged) < 100000:
        sys.exit(f"Only {len(merged)} networks found; the MaxMind file looks wrong.")
    if merged['network'].duplicated().any():
        sys.exit("A network appears twice.")
    for col in col_list:
        if (merged[col].str.lower() == 'nan').any():
            sys.exit(f"The text 'nan' appeared in column {col}.")


def process_zip():
    with zipfile.ZipFile(zip_file_path, 'r') as z:
        # List all files in the ZIP archive
        file_list = z.namelist()

        ipv4_csv = [file for file in file_list if ipv4 in file][0]
        location_csv = [file for file in file_list if location in file][0]

        with z.open(ipv4_csv) as csv_file:
            df1 = read_csv(csv_file)

        with z.open(location_csv) as csv_file:
            df2 = read_csv(csv_file)

        print("DataFrame loaded successfully.")
        return df1, df2


def download_zip():
    response = requests.get(perm_URL, auth=(username, password), timeout=300)

    if response.status_code != 200:
        sys.exit(f"Failed to download the file. Status code: {response.status_code}")
    os.makedirs('temp', exist_ok=True)
    with open(zip_file_path, 'wb') as file:
        file.write(response.content)
    print("Zip file downloaded successfully.")


def process():
    if not username or not password:
        sys.exit("Set MAXMIND_USERNAME and MAXMIND_PASSWORD.")
    download_zip()
    ipv4_df, location_df = process_zip()
    merge_data(ipv4_df, location_df)
    shutil.rmtree('temp')


if __name__ == '__main__':
    process()
