from typing import Dict

from data import read_last_price

# Ref: https://levelup.gitconnected.com/how-to-format-integers-into-string-representations-in-python-9f6ad0f2d36f
def safe_num(num):
    if isinstance(num, str):
        num = float(num)
    return float("{:.3g}".format(abs(num)))


def format_number(num):
    num = safe_num(num)
    sign = ""

    metric = {"T": 1000000000000, "B": 1000000000, "M": 1000000, "K": 1000, "": 1}

    for index in metric:
        num_check = num / metric[index]

        if num_check >= 1:
            num = num_check
            sign = index
            break

    return f"{str(num).rstrip('0').rstrip('.')}{sign}"


def buying_calculate(cash: float, stocks: Dict[str, int]):
    result = {}
    remain = cash
    for stock, ratio in stocks.items():
        each_cash = cash * ratio / 100
        price = read_last_price(stock)
        cnt = each_cash // price
        ratio = cnt * price / cash * 100
        result[stock] = f"{int(cnt):,} ({ratio:.1f}%)"
        remain -= cnt * price
    result["Cash"] = f"${remain:.2f} ({remain / cash * 100 :.1f})%"
    return result
