from pprint import pprint
from typing import Any

import xlrd
import pandas as pd
import numpy as np

from .product import Product, Phone
from .market import Market, MarketHistory
from .analyse import Analyse, DisplayPhone
from .simulation import Simulation
from .demand_model import DemandModel
from .loader import load_markets




def calculate_line(x1:int, x2):
    """Used once"""
    #print(f"{x1=} {x2=}")
    y1 = float(input("y1: "))
    y2 = float(input("y2: "))

    x = [x1, x2] #NOTE change this
    y = [y1, y2]
    slope, intercept = np.polyfit(x, y, 1)
    slope = float(round(slope, 4))
    intercept = float(round(intercept, 4))

    print(f"{slope=} {intercept=}")


def main() -> None:
    rnd = int(input("Round: "))

    data = load_markets()
    analyse_asia = Analyse(data, rnd, "asia")
    analyse_europe = Analyse(data, rnd, "europe")


    # -- ALOITA TÄSTÄ -- #
    # SUOSITUIMMAT TYYLIT
    #analyse_asia.design()

    # SUOSITUIMMAT OMINAISUUDET
    #analyse_europe.feature()
    #analyse_europe.design_feature()
    
    # TEHON JA AKUN SUHDE KYSYNTÄÄN
    #analyse_asia.performance()
    #analyse_asia.battery()
    #analyse_europe.performance_per_euro()
    #analyse_europe.battery_per_euro()

    # HINNAN SUHDE KYSYNTÄÄN
    #analyse_europe.price()
    #analyse_europe.margin_x_sales()

    # Löydä suhteellisen hinnan suhde kysyntään
    #analyse_europe.cumulative()

    # MARKKINOINNIN VAIKUTUS
    #analyse_europe.all_awareness()
    #analyse_europe.all_advertizing_x_sales_by_battery()
    #analyse_europe.all_advertizing_x_sales_by_performance()

    #analyse_europe.advertizing()
    #analyse_europe.all_advertizing_x_sales_by_price()
    #analyse_europe.advertizing_relook()
    #analyse_europe.channel_investments()

    # VOITOT
    #analyse_europe.profit()
    #analyse_europe.profit_x_specs()

    # TUOTEVERTAILU
    #analyse_europe.compare.winners_across_segments()
    #analyse_europe.compare.high_price_segment()
    #analyse_europe.compare.mid_price_segment()
    #analyse_europe.compare.low_price_segment()

    # KILPAILU
    new_products = [(225, 200), (385, 290), (350, 270), (320, 260), (270, 250), (250, 240)]     # Asia
    new_products = [(250, 200), (370, 290), (335, 270), (320, 260), (300, 250), (275, 240)]     # EU
    #analyse_europe.competion_stack_by_team()
    #print(analyse_europe.market.stats.average_battery())
    #print(analyse_europe.market.stats.average_performance())
    #analyse_europe.price_demand()
    #analyse_europe.price_deviance_demand()


    # SIMULOI
    sim = Simulation()
    sim.test_model_europe(rnd)



    #model.test(markets1)   # ValueError: shapes (1,18) and (17,) not aligned: 18 (dim 1) != 17 (dim 0)


   





if __name__ == "__main__":
    main()