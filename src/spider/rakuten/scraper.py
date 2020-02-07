from datetime import date
from selenium import webdriver
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

    def scrape(self,) -> tempfile.TemporaryDirectory:
        try:
            logging.info("Start scaraping")
            self._login()
            self._get_summary()
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
        self.driver.get("https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html")
        self.driver.find_element_by_id("form-login-id").send_keys(self.user_id)
        self.driver.find_element_by_id("form-login-pass").send_keys(self.password)
        self.driver.find_element_by_id("login-btn").click()
        time.sleep(3)
        logging.info("Finished login")
    
    def _get_summary(self):
        logging.info("Start getting summaries")
        self.driver.find_element_by_id("gmenu_acc_reg_change").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//span[contains(text(), '資産残高・保有商品')]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//input[contains(@alt, 'CSVで保存')]").click()
        time.sleep(5)
        logging.info("Finished getting summaries")
        if not self._check_csv():
            raise Exception
        self._move_csv(f"summaries.{date.today():%Y%m%d}.csv")

    def _move_csv(self, file_name: str):
        for csv in [csv for csv in list(Path(self.tempdir.name).glob("*.csv"))]:
            src = csv.absolute().as_posix()
            dst = os.path.join(self.savedir.name, file_name)
            shutil.move(src, dst)

    def _check_csv(self) -> bool:
        return len(list(Path(self.tempdir.name).glob("*.csv"))) > 0