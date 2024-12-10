import os
import shutil
import zipfile
import requests
import pandas as pd

perm_URL = 'https://download.maxmind.com/geoip/databases/GeoLite2-Country-CSV/download?suffix=zip'

## Register at the MaxMind website to get the license key for account_id and license_key

username = os.getenv('MAXMIND_USERNAME')
password = os.getenv('MAXMIND_PASSWORD')

zip_file_path = 'temp/GeoLite2-Country-CSV.zip'
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

def merge_data(ipv4_df,location_df):
    ipv4_df = ipv4_df[['network', 
                   'geoname_id',
                   'registered_country_geoname_id',
                   'is_anonymous_proxy',
                   'is_satellite_provider',
                    ]]
    location_df = location_df[[
                    'geoname_id',
                    'continent_code',
                    'continent_name',
                    'country_iso_code',
                    'country_name',
    ]]
    # Fill missing geoname_id with registered_country_geoname_id
    ipv4_df['geoname_id'] = ipv4_df['geoname_id'].fillna(ipv4_df['registered_country_geoname_id'])
    ipv4_df = ipv4_df.drop(columns=['registered_country_geoname_id'])
    # Merge ipv4 and location by geoname_id if both null then drop
    merged = pd.merge(ipv4_df, location_df, on='geoname_id', how='left')
    condition = merged['geoname_id'] == ""
    merged.loc[condition, [
        'geoname_id', 
        'continent_code', 
        'continent_name', 
        'country_iso_code', 
        'country_name']] = ""
    merged.columns = col_list
    merged = merged.drop_duplicates()
    merged.to_csv('data/geoip2-ipv4.csv', index=False)

def process_zip():
    with zipfile.ZipFile(zip_file_path, 'r') as z:
        # List all files in the ZIP archive
        file_list = z.namelist()
        
        ipv4_csv = [file for file in file_list if ipv4 in file][0]
        location_csv = [file for file in file_list if location in file][0]

        with z.open(ipv4_csv) as csv_file:
            df1 = pd.read_csv(csv_file)

        with z.open(location_csv) as csv_file:
            df2 = pd.read_csv(csv_file)

        print("DataFrame loaded successfully.")
        return df1, df2
    
def download_zip():
    response = requests.get(perm_URL, auth=(username, password))

    if response.status_code == 200:
        if 'temp' not in os.listdir():
            os.mkdir('temp')
        with open(zip_file_path, 'wb') as file:
            file.write(response.content)
        print("Zip file downloaded successfully.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}, Response: {response.text}")
        print(response.text)

def process():
    download_zip()
    ipv4_df, location_df = process_zip()
    merge_data(ipv4_df, location_df)
    shutil.rmtree('temp')

if __name__ == '__main__':
    process()