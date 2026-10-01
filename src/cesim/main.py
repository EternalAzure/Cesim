from pprint import pprint
from typing import Any

import xlrd
import pandas as pd

from .product import Product
from .market import Market
from .analyse import Analyse



def read_row_str(sheet, rown:int, start_coln=1):
    cell_values:list[str] = []

    for column in range(start_coln, sheet.ncols -1):
        cell_value = sheet.cell(rown, column).value
        if isinstance(cell_value, str):
            cell_values.append(cell_value)

    return cell_values

def read_row_float(sheet, rown:int, start_coln=1):
    cell_values:list[float] = []

    for column in range(start_coln, sheet.ncols -1):
        cell_value = sheet.cell(rown, column).value
        if isinstance(cell_value, float):
            cell_values.append(cell_value)

    return cell_values

def read_product_europe(sheet, coln:int) -> Product:

    company = str(sheet.cell(1, coln).value)
    temp_col = coln
    while len(company) <= 0:
        temp_col -= 1
        company = str(sheet.cell(1, temp_col).value)

    name = str(sheet.cell(2, coln).value)
    price = round(float(sheet.cell(3, coln).value), 2)

    # Sales
    households_sales = round(float(sheet.cell(6, coln).value), 3)
    high_end_households_sales = round(float(sheet.cell(7, coln).value), 3)
    companies_sales = round(float(sheet.cell(8, coln).value), 3)
    high_end_companies_sales = round(float(sheet.cell(9, coln).value), 3)
    total_sales = round(float(sheet.cell(11, coln).value), 3)

    # Sales by distribution channel
    specialist = round(float(sheet.cell(14, coln).value), 4)
    generalist = round(float(sheet.cell(15, coln).value), 4)
    online = round(float(sheet.cell(16, coln).value), 4)
    
    # Market share %
    households_market_share = round(float(sheet.cell(19, coln).value), 4)
    high_end_households_market_share = round(float(sheet.cell(20, coln).value), 4)
    companies_market_share = round(float(sheet.cell(21, coln).value), 4)
    high_end_companies_market_share = round(float(sheet.cell(22, coln).value), 4)
    
    # Marketing
    advertizing = round(float(sheet.cell(25, coln).value), 4)
    channel_investments = round(float(sheet.cell(26, coln).value), 2)

    # Product characteristics
    performance = int(sheet.cell(29, coln).value)
    battery = int(sheet.cell(30, coln).value)
    camera = True if sheet.cell(32, coln).value == "x" else False
    memory = True if sheet.cell(33, coln).value == "x" else False
    display = True if sheet.cell(34, coln).value == "x" else False
    resistance = True if sheet.cell(35, coln).value == "x" else False
    security = True if sheet.cell(36, coln).value == "x" else False
    design = str(sheet.cell(37, coln).value)
    
    variable_unit_cost = round(float(sheet.cell(39, coln).value), 2)

    # Awareness & Intentions
    households_awareness = round(float(sheet.cell(85, coln).value), 2)
    high_end_households_awareness = round(float(sheet.cell(86, coln).value), 2)
    companies_awareness = round(float(sheet.cell(87, coln).value), 4)
    high_end_companies_awareness = round(float(sheet.cell(88, coln).value), 2)
    
    households_intention = round(float(sheet.cell(97, coln).value), 2)
    high_end_households_intention = round(float(sheet.cell(98, coln).value), 2)
    companies_intention = round(float(sheet.cell(99, coln).value), 4)
    high_end_companies_intention = round(float(sheet.cell(100, coln).value), 2)
    

    product = Product(
        name,
        company,
        price,
        variable_unit_cost,
        households_sales,
        high_end_households_sales,
        companies_sales,
        high_end_companies_sales,
        total_sales,
        specialist,
        generalist,
        online,
        households_market_share,
        high_end_households_market_share,
        companies_market_share,
        high_end_companies_market_share,
        advertizing,
        channel_investments,
        performance,
        battery,
        camera,
        memory,
        display,
        resistance,
        security,
        design,
        households_awareness,
        high_end_households_awareness,
        companies_awareness,
        high_end_companies_awareness,
        households_intention,
        high_end_households_intention,
        companies_intention,
        high_end_companies_intention
    )


    return product

def read_product_asia(sheet, coln:int) -> Product:

    company = str(sheet.cell(1, coln).value)
    temp_col = coln
    while len(company) <= 0:
        temp_col -= 1
        company = str(sheet.cell(1, temp_col).value)

    name = str(sheet.cell(41, coln).value)
    price = round(float(sheet.cell(42, coln).value), 2)

    # Sales
    households_sales = round(float(sheet.cell(45, coln).value), 3)
    high_end_households_sales = round(float(sheet.cell(46, coln).value), 3)
    companies_sales = round(float(sheet.cell(47, coln).value), 3)
    high_end_companies_sales = round(float(sheet.cell(48, coln).value), 3)
    total_sales = round(float(sheet.cell(50, coln).value), 3)

    # Sales by distribution channel
    specialist = round(float(sheet.cell(53, coln).value), 4)
    generalist = round(float(sheet.cell(54, coln).value), 4)
    online = round(float(sheet.cell(55, coln).value), 4)
    
    # Market share %
    households_market_share = round(float(sheet.cell(58, coln).value), 4)
    high_end_households_market_share = round(float(sheet.cell(59, coln).value), 4)
    companies_market_share = round(float(sheet.cell(60, coln).value), 4)
    high_end_companies_market_share = round(float(sheet.cell(61, coln).value), 4)
    
    # Marketing
    advertizing = round(float(sheet.cell(64, coln).value), 4)
    channel_investments = round(float(sheet.cell(65, coln).value), 2)

    # Product characteristics
    performance = int(sheet.cell(68, coln).value)
    battery = int(sheet.cell(69, coln).value)
    camera = True if sheet.cell(71, coln).value == "x" else False
    memory = True if sheet.cell(72, coln).value == "x" else False
    display = True if sheet.cell(73, coln).value == "x" else False
    resistance = True if sheet.cell(74, coln).value == "x" else False
    security = True if sheet.cell(75, coln).value == "x" else False
    design = str(sheet.cell(76, coln).value)
    
    variable_unit_cost = round(float(sheet.cell(78, coln).value), 2)

    # Awareness & Intentions
    households_awareness = round(float(sheet.cell(104, coln).value), 2)
    high_end_households_awareness = round(float(sheet.cell(105, coln).value), 2)
    companies_awareness = round(float(sheet.cell(106, coln).value), 4)
    high_end_companies_awareness = round(float(sheet.cell(107, coln).value), 2)
    
    households_intention = round(float(sheet.cell(110, coln).value), 2)
    high_end_households_intention = round(float(sheet.cell(111, coln).value), 2)
    companies_intention = round(float(sheet.cell(112, coln).value), 4)
    high_end_companies_intention = round(float(sheet.cell(113, coln).value), 2)

    product = Product(
        name,
        company,
        price,
        variable_unit_cost,
        households_sales,
        high_end_households_sales,
        companies_sales,
        high_end_companies_sales,
        total_sales,
        specialist,
        generalist,
        online,
        households_market_share,
        high_end_households_market_share,
        companies_market_share,
        high_end_companies_market_share,
        advertizing,
        channel_investments,
        performance,
        battery,
        camera,
        memory,
        display,
        resistance,
        security,
        design,
        households_awareness,
        high_end_households_awareness,
        companies_awareness,
        high_end_companies_awareness,
        households_intention,
        high_end_households_intention,
        companies_intention,
        high_end_companies_intention
    )


    return product


def main() -> None:
    round = int(input("Round: "))
    if round == 1:
        book = xlrd.open_workbook("/home/miisu/Desktop/repos/cesim/src/cesim/results-r01.xls")
    elif round == 2:
        book = xlrd.open_workbook("/home/miisu/Desktop/repos/cesim/src/cesim/results-r02.xls")
    elif round == 3:
        book = xlrd.open_workbook("/home/miisu/Desktop/repos/cesim/src/cesim/results-r03.xls")
    elif round == 4:
        book = xlrd.open_workbook("/home/miisu/Desktop/repos/cesim/src/cesim/results-r04.xls")
    else: raise ValueError("Round must me a positive integer")
    sheet = book.sheet_by_index(0)

    product_column_indexes_europe:list[int] = []
    for i, name in enumerate(read_row_str(sheet, 2), 1):
        if len(name) > 0:
            product_column_indexes_europe.append(i)

    product_column_indexes_asia:list[int] = []
    for i, name in enumerate(read_row_str(sheet, 41), 1):
        if len(name) > 0:
            product_column_indexes_asia.append(i)

    products_europe:list[Product] = []
    for index in product_column_indexes_europe:
        products_europe.append(read_product_europe(sheet, index))

    products_asia:list[Product] = []
    for index in product_column_indexes_asia:
        products_asia.append(read_product_asia(sheet, index))

    market_europe = Market(products_europe)
    market_asia = Market(products_asia)
    analyse_europe = Analyse(market_europe, round)
    analyse_asia = Analyse(market_asia, round)


    # -- ALOITA TÄSTÄ -- #
    # Löydä suosituimmat tyylit
    #analyse_europe.design()

    # Löydä suosituimmat ominaisuudet
    #analyse_europe.feature()
    #analyse_europe.design_feature()
    
    # Löydä tehon ja akun suhde kysyntään
    #analyse_europe.performance()
    #analyse_europe.battery()
    #analyse_europe.performance_per_euro()
    #analyse_europe.battery_per_euro()

    # Löydä hinnan suhde kysyntään
    #analyse_europe.price()

    # Löydä suhteellisen hinnan suhde kysyntään
    #analyse_europe.cumulative()

    # Löydä markkinoinnin vaikutus
    #analyse_europe.advertizing()

    # Löydä suosituimmat puhelimet ryhmittäin
    

    # Mallinnan kysyntä


    
    return

    return

    df = pd.DataFrame(
        {
            "Name": [
                "Braund, Mr. Owen Harris",
                "Allen, Mr. William Henry",
                "Bonnell, Miss Elizabeth",
            ],
            "Age": [22, 35, 58],
            "Sex": ["male", "male", "female"],
        }
    )

    sales_households = read_row_float(6)
    sales_high_end_households = read_row_float(7)
    sales_companies = read_row_float(8)
    sales_high_end_companies = read_row_float(9)
    sales_total = read_row_float(11)



if __name__ == "__main__":
    main()