import os
from typing import Any
from pprint import pprint

import pyfiglet
import numpy as np
import pandas as pd
from rich.console import Console
from simple_term_menu import TerminalMenu

from .terminal import intro
from .analysis import Analysis
from .simulation import Simulation


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
    analyse = Analysis()
    simulate = Simulation()

    options = ["Quit", "Analyse", "Simulate"]
    terminal_menu = TerminalMenu(options)
    console = Console()

    while True:
        # -- INTRO -- #
        intro("Select task.", ["Home"])

        # -- MAIN LOOP -- #
        entry_index = terminal_menu.show()
        if entry_index == 0:
            exit(0)
        elif entry_index == 1:
            analyse.main()
        elif entry_index == 2:
            simulate.main()


    # TUOTEVERTAILU
    #analyse_asia.compare.winners_across_segments()
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




if __name__ == "__main__":
    main()

