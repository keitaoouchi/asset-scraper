from bs4 import BeautifulSoup
from typing import Tuple
import re
import logging


class SummaryParser:
    def __init__(self, html):
        self.html = html

    def parse(self) -> Tuple[int, int, int]:
        bs = BeautifulSoup(self.html, 'html.parser')
        try:
            e = bs.find("font", text=re.compile("現金残高等")).find_parent("tr").find("font",attrs={"color": "black"})
            cash = e.string.strip().replace(",", "")
        except:
            logging.warn("現金残高等が見つかりませんでした")
            cash = 0
        try:
            e = bs.find("div", text=re.compile("株式")).find_parent("td").find_next_sibling('td').find('div')
            shares = e.string.strip().replace(",", "")
        except:
            logging.warn("株式が見つかりませんでした")
            shares = 0
        try:
            e = bs.find("div", text=re.compile("投資信託")).find_parent("td").find_next_sibling('td').find('div')
            trust = e.string.strip().replace(",", "")
        except:
            logging.warn("投資信託が見つかりませんでした")
            trust = 0
        return (cash, shares, trust)