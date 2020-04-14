from bs4 import BeautifulSoup
from decimal import Decimal

def convert_to_RUR(soup, cur_from, amount):
    return (
                     float(soup.find('charcode', text=cur_from).find_parent().find('value').text.replace(',', '.')) /
                     float(soup.find('charcode', text=cur_from).find_parent().find('nominal').text.replace(',', '.'))
             ) * float(amount)

def convert_from_RUR(soup, cur_to, amount):
    proc = float(soup.find('charcode', text=cur_to).find_parent().find('nominal').text.replace(',', '.')) / \
           float(soup.find('charcode', text=cur_to).find_parent().find('value').text.replace(',', '.'))
    return proc*float(amount)

def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + date).text
    soup = BeautifulSoup(response, features="lxml")

    if cur_from == "RUR":
        result = convert_from_RUR(soup, cur_to, amount)
    elif cur_to == "RUR":
        result = convert_to_RUR(soup, cur_from, amount)
    else:
        result1 = float(soup.find('charcode', text=cur_from).find_parent().find('value').text.replace(',', '.')) / \
                  float(soup.find('charcode', text=cur_from).find_parent().find('nominal').text.replace(',', '.'))
        result1 = result1 * float(amount)

        result = convert_from_RUR(soup, cur_to, result1)

    result = Decimal(result)
    result = result.quantize(Decimal("1.0000"))
    return result

