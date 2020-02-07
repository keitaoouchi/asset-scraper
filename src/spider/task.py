from sbi import scraper as sbi_scraper
from sbi import html_parser, definition
from rakuten import scraper as rakuten_scraper
from datetime import date
from pathlib import Path
from google.cloud import storage
from google.api_core.exceptions import NotFound
import os
import logging


def scrape_rakuten(id: str, pw: str, bucket: str):
    logging.getLogger().setLevel(logging.INFO)
    s = rakuten_scraper.Scraper(id, pw)
    dir = s.scrape()
    file = [csv for csv in Path(dir.name).glob("summaries.*.csv")][0]
    gcs = _gcs_client().get_bucket(bucket)
    blob = gcs.blob(file.name)
    blob.upload_from_filename(file.absolute().as_posix())
    logging.info(f"{file.name}をアップロードしました")


def scrape_sbi(id: str, pw: str, bucket: str):
    logging.getLogger().setLevel(logging.INFO)
    s = sbi_scraper.Scraper(id, pw)
    dir = s.scrape(None, None)
    shares_csv = [csv for csv in Path(dir.name).glob("shares.*.csv")][0]
    gcs = _gcs_client().get_bucket(bucket)
    for file in [shares_csv]:
        blob = gcs.blob(file.name)
        blob.upload_from_filename(file.absolute().as_posix())
        logging.info(f"{file.name}をアップロードしました")
    
    summary_html = [html for html in Path(dir.name).glob("summary.html")][0]
    with open(summary_html) as f:
        html = f.read()
        cash, shares, trust = html_parser.SummaryParser(html).parse()
        #当月用csvをgcsから取得または新規作成してcash,sharesを追記してアップロード
        today = date.today()
        file_name = f"asset_summary.{today:%Y%m%d}.csv"
        blob = gcs.blob(file_name)
        summary = definition.AssetSummary(cash, shares, trust, today)
        blob.upload_from_string(summary.make_csv_str(), content_type="text/csv")
        logging.info(f"{file_name}をアップロードしました")


def _gcs_client() -> storage.Client:
    auth_json = os.path.join(os.path.abspath(os.path.curdir), "auth.json")
    if os.path.exists(auth_json):
        logging.info("auth.json found")
        return storage.Client.from_service_account_json(auth_json)
    else:
        return storage.Client()