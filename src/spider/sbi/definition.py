from datetime import date
from typing import Optional
from datetime import date

class AssetSummary:
    def __init__(self, cash: int, shares: int, trust: int, created_at: date):
        self.cash = cash
        self.shares = shares
        self.trust = trust
        self.created_at = created_at
    
    def make_csv_str(self) -> str:
        header = "cash,shares,trust,created_at"
        body = f"{self.cash},{self.shares},{self.trust},{self.created_at:%Y%m%d}"
        return "\n".join([header, body]) + "\n"


class DateRange:
    def __init__(self, from_date: date, to_date: date):
        self.from_date = from_date
        self.to_date = to_date


class Share:
    def __init__(self,
                 code: int,
                 name: str,
                 number_of_share: int,
                 number_of_selling: int,
                 average_price: int,
                 last_price: int,
                 aquisition_cost: int,
                 last_evaluation: int,
                 profit: int):
        """
        保有銘柄の各行を表す

        Attributes
        ----------
        code: int
            銘柄コード
        name: str
            銘柄名称
        number_of_share: int
            保有株数
        number_of_selling: int
            売却注文中
        average_price: int
            取得単価
        last_price: int
            現在値
        aquisition_cost: int
            取得金額
        last_evaluation: int
            評価額
        profit: int
            評価損益
        """
        self.code = code
        self.name = name
        self.number_of_share = number_of_share
        self.number_of_selling = number_of_selling
        self.average_price = average_price
        self.last_price = last_price
        self.aquisition_cost = aquisition_cost
        self.last_evaluation = last_evaluation
        self.profit = profit


class Deal:
    def __init__(self,
                 deal_at: date,
                 name: str,
                 code: int,
                 market: str,
                 deal_type: str,
                 due_type: Optional[str],
                 azukari: int,
                 kazei_type: Optional[int],
                 deal_amount: int,
                 price: int,
                 cost: int,
                 tax: int,
                 delivery_at: date,
                 kessai_amount: Optional[int]):
        """
        保有銘柄の各行を表す

        Attributes
        ----------
        deal_at: date
            約定日
        name: str
            銘柄
        code: int
            銘柄コード
        market: string
            市場
        deal_type: str
            取引
        due_type: Optional[str]
            期限
        azukari: str
            預り
        kazei_type: Optional[str]
            課税
        deal_amount: int
            約定数量
        price: int
            約定単価
        cost: int
            手数料/諸経費等
        tax: int
            税額
        delivery_at: date
            受渡日
        kessai_amount: Optional[int]
            受渡金額/決済損益
        """
        self.deal_at = deal_at
        self.name = name
        self.code = code
        self.market = market
        self.deal_type = deal_type
        self.due_type = due_type if due_type is not "--" else None
        self.azukari = azukari
        self.kazei_type = kazei_type if kazei_type is not "--" else None
        self.deal_amount = deal_amount
        self.price = price
        self.cost = cost
        self.tax = tax
        self.delivery_at = delivery_at
        self.kessai_amount = kessai_amount if kessai_amount is not "--" else None


class Statement:
    def __init__(self,
                 statement_at: date,
                 statement_type: str,
                 detail: int,
                 out_amount: int,
                 in_amount: int,
                 transfer_out_amount: int,
                 transfer_in_amount: int):
        """
        保有銘柄の各行を表す

        Attributes
        ----------
        statement_at: date
            入出金日
        statement_type: str
            区分
        detail: str
            摘要
        out_amount: int
            出金額
        in_amount: int
            入金額
        transfer_out_amount: int
            振替出金額
        transfer_in_amount: int
            振替入金額
        """
        self.statement_at = statement_at
        self.statement_type = statement_type
        self.detail = detail
        self.out_amount = out_amount if out_amount is not "-" else 0
        self.in_amount = in_amount if in_amount is not "-" else 0
        self.transfer_out_amount = transfer_out_amount if transfer_out_amount is not "-" else 0
        self.transfer_in_amount = transfer_in_amount if transfer_in_amount is not "-" else 0
