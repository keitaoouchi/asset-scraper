import csv
from .definition import Share, Deal, Statement


class ShareParser:
    def __init__(self, file):
        self.file = file

    def parse(self) -> [Share]:
        lines = self._parse()
        return ShareParser._convert(lines)

    def _parse(self) -> [[str]]:
        with open(self.file, encoding="SHIFT_JIS") as f:
            reader = csv.reader(f)
            # '銘柄コード', '銘柄名称', '保有株数', '売却注文中', '取得単価', '現在値', '取得金額', '評価額', '評価損益'
            lines = [line for line in reader if len(line) == 9 and line[0].isdigit()]
            return lines

    @staticmethod
    def _convert(lines) -> [Share]:
        return [Share(*l) for l in lines]


class DealParser:
    def __init__(self, file):
        self.file = file

    def parse(self) -> [Deal]:
        lines = self._parse()
        return DealParser._convert(lines)

    def _parse(self) -> [[str]]:
        with open(self.file, encoding="SHIFT_JIS") as f:
            reader = csv.reader(f)
            lines = [line for line in reader if len(line) == 14 and line[2].isdigit()]
            return lines

    @staticmethod
    def _convert(lines) -> [Deal]:
        return [Deal(*l) for l in lines]


class StatementParser:
    def __init__(self, file):
        self.file = file

    def parse(self) -> [Deal]:
        lines = self._parse()
        return StatementParser._convert(lines)

    def _parse(self) -> [[str]]:
        with open(self.file, encoding="SHIFT_JIS") as f:
            reader = csv.reader(f)
            lines = [line for line in reader if len(line) == 7 and any([l.isdigit() for l in line])]
            return lines

    @staticmethod
    def _convert(lines) -> [Statement]:
        return [Statement(*l) for l in lines]