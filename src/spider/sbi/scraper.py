from datetime import date
from selenium import webdriver
from .definition import DateRange
import time
import tempfile
from pathlib import Path
import shutil
import logging
import os
from typing import Optional


class Scraper:
    def __init__(self, user_id: str, password: str):
        self.savedir = tempfile.TemporaryDirectory()
        self.tempdir = tempfile.TemporaryDirectory()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1024,768"')
        options.add_experimental_option("prefs", {"download.default_directory": self.tempdir.name})
        self.driver = webdriver.Chrome(options=options)
        self.user_id = user_id
        self.password = password

    def scrape(self, deals_range: Optional[DateRange], statements_range: Optional[DateRange]) -> tempfile.TemporaryDirectory:
        try:
            logging.info("Start scaraping")
            self._login()
            self._get_summary()
            self._get_shares()
            if deals_range:
                self._get_deals(deals_range.from_date, deals_range.to_date)
            if statements_range:
                self._get_statements(statements_range.from_date, statements_range.to_date)
            logging.info("Finished scaraping")
            return self.savedir
        except Exception as e:
            logging.error(e)
            self.savedir.cleanup()
            raise e
        finally:
            self.tempdir.cleanup()
            self.driver.close()

    def _login(self):
        logging.info("Start login")
        self.driver.get("https://www.sbisec.co.jp/ETGate/")
        self.driver.find_element_by_name("user_id").send_keys(self.user_id)
        self.driver.find_element_by_name("user_password").send_keys(self.password)
        self.driver.find_element_by_name("ACT_login").click()
        time.sleep(3)
        logging.info("Finished login")
    
    def _get_summary(self):
        logging.info("Start getting summaries")
        self.driver.find_element_by_xpath("//img[contains(@alt, '口座管理')]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//area[contains(@alt, 'サマリー')]").click()
        time.sleep(5)
        html = self.driver.page_source
        dst = os.path.join(self.savedir.name, 'summary.html')
        with open(dst, 'w') as f:
            f.write(html)
        logging.info("Finished getting summaries")

    def _get_shares(self):
        logging.info("Start getting shares")
        self.driver.find_element_by_xpath("//img[contains(@alt, '口座管理')]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//area[contains(@alt, '保有証券')]").click()
        time.sleep(5)
        self.driver.find_element_by_link_text("CSVダウンロード").click()
        time.sleep(10)
        if not self._check_csv():
            raise Exception
        self._move_csv(f"shares.{date.today():%Y%m%d}.csv")
        logging.info("Finished getting shares")

    def _get_deals(self, from_date: date, to_date: date):
        logging.info("Start getting deals")
        self.driver.find_element_by_xpath("//img[contains(@alt, '口座管理')]").click()
        time.sleep(3)
        self.driver.find_element_by_link_text("取引履歴").click()
        time.sleep(3)
        self.driver.find_element_by_name("ref_from_yyyy").send_keys(f"{from_date.year}")
        self.driver.find_element_by_name("ref_from_mm").send_keys(f"{from_date.month:02}")
        self.driver.find_element_by_name("ref_from_dd").send_keys(f"{from_date.day:02}")
        self.driver.find_element_by_name("ref_to_yyyy").send_keys(f"{to_date.year}")
        self.driver.find_element_by_name("ref_to_mm").send_keys(f"{to_date.month:02}")
        self.driver.find_element_by_name("ref_to_dd").send_keys(f"{to_date.day:02}")
        self.driver.find_element_by_name("ACT_search").click()
        time.sleep(5)
        self.driver.find_element_by_link_text("CSVダウンロード").click()
        time.sleep(10)
        if not self._check_csv():
            raise Exception
        self._move_csv(f"deals.{from_date:%Y%m%d}-{to_date:%Y%m%d}.csv")
        logging.info("Finished getting deals")

    def _get_statements(self, from_date: date, to_date: date):
        logging.info("Start getting statements")
        self.driver.find_element_by_xpath("//img[contains(@alt, '入出金・振替')]").click()
        time.sleep(3)
        self.driver.find_element_by_link_text("入出金明細").click()
        time.sleep(3)
        self.driver.find_element_by_name("in_kkn_sti_from_yyyy").send_keys(f"{from_date.year}")
        self.driver.find_element_by_name("in_kkn_sti_from_mm").send_keys(f"{from_date.month:02}")
        self.driver.find_element_by_name("in_kkn_sti_from_dd").send_keys(f"{from_date.day:02}")
        self.driver.find_element_by_name("in_kkn_sti_to_yyyy").send_keys(f"{to_date.year}")
        self.driver.find_element_by_name("in_kkn_sti_to_mm").send_keys(f"{to_date.month:02}")
        self.driver.find_element_by_name("in_kkn_sti_to_dd").send_keys(f"{to_date.day:02}")
        self.driver.find_element_by_xpath("//a/img[contains(@alt, '照会')]").click()
        time.sleep(5)
        self.driver.find_element_by_link_text("明細ダウンロード(CSV形式)").click()
        time.sleep(10)
        if not self._check_csv():
            raise Exception
        self._move_csv(f"statements.{from_date:%Y%m%d}-{to_date:%Y%m%d}.csv")
        logging.info("Finished getting deals")

    def _move_csv(self, file_name: str):
        for csv in [csv for csv in list(Path(self.tempdir.name).glob("*.csv"))]:
            src = csv.absolute().as_posix()
            dst = os.path.join(self.savedir.name, file_name)
            shutil.move(src, dst)

    def _check_csv(self) -> bool:
        return len(list(Path(self.tempdir.name).glob("*.csv"))) > 0

