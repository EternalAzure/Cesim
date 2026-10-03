from typing import Literal

        # EURO TO AWARENESS BY TEAMS
        # All, Europe
        #         Blue    Green   Grey    Orange  Pink    Red
        # Round 3        -0.080   0.049   0.066   0.105   0.063
        # Round 2 1.527   0.023   0.038   0.052  -0.004  -0.021
        # Round 1 0.011   0.014   0.072   0.027           0.016

        # All, Asia
        #         Blue    Green   Grey    Orange  Pink    Red
        # Round 3         0.069   0.164   0.046           0.108
        # Round 2 2.284   0.020           0.011           0.066
        # Round 1 0.013                   0.003                

        # H, Europe
        #         Blue    Green   Grey    Orange  Pink    Red
        # Round 3         0.231   0.123   0.162   0.170   0.183
        # Round 2 0.197   0.155   0.223   0.182   0.182   0.282
        # Round 1 0.155   0.146   0.194   0.179  -0.288   0.153
        
        # AWARENESS TO SALES BY TEAMS
        # All, Europe
        #         Blue    Green   Grey    Orange  Pink    Red
        # Round 3         0.231   0.123   0.162   0.170   0.183
        # Round 2 0.197   0.155   0.223   0.182   0.182   0.282
        # Round 1 0.155   0.146   0.194   0.179  -0.288   0.153

        # All, Asia
        #         Blue    Green   Grey    Orange  Pink    Red
        # Round 3         0.162   0.197   0.135           0.219
        # Round 2 0.197   0.169           0.129           0.183
        # Round 1 0.173                   0.154                

        # EURO TO AWARENESS BY TEAMS



class Model:

    def __init__(self) -> None:

        self.money_to_awareness_h =  0.50  
        self.money_to_awareness_hh = 0.50  
        self.money_to_awareness_c =  0.50  
        self.money_to_awareness_hc = 0.50  

        self.awareness_to_intentions_h =    0.50
        self.awareness_to_intentions_hh =   0.50
        self.awareness_to_intentions_c =    0.50
        self.awareness_to_intentions_hc =   0.50

        self.intentions_to_sales_h =    0.50
        self.intentions_to_sales_hh =   0.50
        self.intentions_to_sales_c =    0.16
        self.intentions_to_sales_hc =   0.40

        self.channel_investment_effect = 0.01828 # rounds: 1.01166, 1.02456, 1.01862


    def h_price_demand_curve(self):
        average_price = 316
        x = [265]
        y = [6.85]

    def hh_price_demand_curve(self):
        average_price = 336

    def c_price_demand_curve(self):
        average_price = 338

    def hc_price_demand_curve(self):
        average_price = 360


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


    