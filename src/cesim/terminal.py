import os
import textwrap
import itertools
from pprint import pprint
from typing import Any, Literal
from contextlib import suppress

import pyfiglet
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rich.console import Console
from simple_term_menu import TerminalMenu

from .product import Product
from .loader import load_markets
from .market import Market, MarketHistory


CONSOLE = Console()

def intro(message:str, navigation:list[str]):
    os.system("clear")
    ascii_banner = pyfiglet.figlet_format("TelePink!")
    CONSOLE.print("[bold orchid]"+ascii_banner+"[/bold orchid]")
    print("Keep calm and scroll on", end="\n\n")
    navigation[-1] = f"[underline orchid]{navigation[-1]}[/underline orchid]"
    CONSOLE.print(" - ".join([s for s in navigation]), end="\n\n")
    print(f"{message}", end="\n\n")


def configuration(keys:list[str], values:list[Any]):
    if len(keys) > len(values): raise ValueError("More keys than values.")
    if len(keys) < len(values): raise ValueError("More values than keys.")
    
    for idx in range(len(keys)):
        CONSOLE.print(f"[bold orchid]|[/bold orchid][bold white]{keys[idx]:<20}[/bold white]{values[idx]}")
    print("")


def horizontal_list(values:list):
    string = "".join([f"{v:<3}" for v in values])
    CONSOLE.print(string)