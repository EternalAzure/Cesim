from typing import Literal


        # H Advertizing x Sales
        # Round 3: -0.00951x
        # Round 2: 0.00106x 
        # Round 1: -0.00038x

        # H Advertizing x Sales     Round 3 - 1014.53
        # 1000  68.89
        # 3000  49.87
        # 2000  -19.02
        # -19.02 / 2000 = -0.00951

        # 1000  14.07               Round 2 - 238.47
        # 2000  15.13
        # 1000   1.06
        # 1.06 / 1000 = 0.00106

        # 1000  6.277                Round 1 - 81.44
        # 3000  5.515
        # 2000  -0.762
        # -0.762 / 1000 = -0.000381
        # ----
        # HH Advertizing x Sales    Round 3 - 1111.87
        # 1000  51.07
        # 2000  65.87
        # 1000  14.8
        # 14.8 / 1000 = 0.0148

        # 1000  28.61               Round 2 - 575.39
        # 2000  38.02
        # 1000  9.41
        # 9.41 / 1000 = 0.00941

        # 1000  13.88               Round 1 - 247.47
        # 2000  17.03
        # 1000  3.15
        # 13.15 / 1000 = 0.00315

        # Vaikutus skaalattu markkinan mukaan   247.47      575.39      1111.87     1000
        # 0.00315 -> 0.00732 ja 0.01415         0.00315     0.00732     0.01415     
        # 0.00941 -> 0.00405 ja 0.01818         0.00405     0.00941     0.01818
        # 0.0148  -> 0.00766 ja 0.00394         0.00394     0.00766     0.01480
        # ----
        # C Advertizing x Sales
        # Round 3: 0.00044x
        # Round 2: 0.00114x 
        # Round 1: 0.00032x
        # ----
        # HC Advertizing x Sales
        # Round 3: 0.009734x
        # Round 2: 0.004976x
        # Round 1: 0.004529x



class Model:

    def __init__(self) -> None:


        self.ad_effect_h: float = 0.0       # Tilastollisesti
        self.ad_effect_hh: float = 0.01571  # 0.01571 sales per euro when market size is 1111.87k
        self.ad_effect_c: float = 0.0       # Tilastollisesti
        self.ad_effect_hc: float = 0.0077

        self.money_to_awareness_h = 0.0 # Valhe
        self.money_to_awareness_hh = 0.0 # Valhe
        self.money_to_awareness_c = 0.0 # Valhe
        self.money_to_awareness_hc = 0.0 # Valhe

        self.awareness_to_sales = 0.174 # rounds: 0.1593, 0.1742, 0.1885 (awareness x sales)
        self.awareness_to_sales_h = 0.174 # rounds: 
        self.awareness_to_sales_hh = 0.174 # rounds: 
        self.awareness_to_sales_c = 0.174 # rounds: 
        self.awareness_to_sales_hc = 0.174 # rounds: 

        self.channel_investment_effect = 0.01828 # rounds: 1.01166, 1.02456, 1.01862


    def channel_investment(self, euro:float) -> float:
        """Returns increase in sales (sales k)"""
        return euro * self.channel_investment_effect

    def advertizing(self, euro:float, group:Literal["H", "HH", "C", "HC"]) -> float:
        """Returns increase in sales (sales k)"""
        if group == "H":
            return euro * self.ad_effect_h
        if group == "HH":
            return euro * self.ad_effect_hh
        if group == "C":
            return euro * self.ad_effect_c
        if group == "HC":
            return euro * self.ad_effect_hc


