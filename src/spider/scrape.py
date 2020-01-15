from sbi import csv_parser, definition, scraper
from datetime import date
from pathlib import Path
from google.cloud import storage as gcs
import os
import logging

def scrape(id: str, pw: str, bucket: str):
    logging.getLogger().setLevel(logging.INFO)
    s = scraper.Scraper(id, pw)
    #deal_range = definition.DateRange(date(2020, 1, 1), date(2020, 12, 31))
    #statements_range = definition.DateRange(date(2020, 1, 1), date(2020, 12, 31))
    csvdir = s.scrape(None, None)
    shares_csv = [csv for csv in Path(csvdir.name).glob("shares.*.csv")][0]
    #deals_csv = [csv for csv in Path(csvdir.name).glob("deals.*.csv")][0]
    #statements_csv = [csv for csv in Path(csvdir.name).glob("statements.*.csv")][0]
    b = get_client().get_bucket(bucket)
    for file in [shares_csv]:
        blob = b.blob(file.name)
        blob.upload_from_filename(file.absolute().as_posix())

def get_client():
    auth_json = os.path.join(os.path.abspath(os.path.curdir), "auth.json")
    logging.info(auth_json)
    if os.path.exists(auth_json):
        logging.info("auth.json found")
        return gcs.Client.from_service_account_json(auth_json)
    else:
        logging.info("auth.json not found")
        return gcs.Client()
    return gcs.Client

if __name__ == '__main__':
    id = os.environ["SBI_ID"]
    pw = os.environ["SBI_PW"]
    bucket = os.environ["BUCKET"]
    scrape(id, pw, bucket)