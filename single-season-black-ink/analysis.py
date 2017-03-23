import numpy as np
import pandas as pd

pd.options.display.max_columns = 800

LAHMAN_HITTERS = "C:/Users/LMarco/Downloads/baseballdatabank-2017.1/core/Batting.csv"
CATEGORIES_RAW = ["HR", "RBI", "R", "H", "2B", "BB", "SB", "G", "AB", "3B"]
CATEGORIES_CALC = ["BA", "SLG"]
CATEGORIES = CATEGORIES_RAW + CATEGORIES_CALC

def main():
    h = pd.read_csv(LAHMAN_HITTERS)
    h.fillna(0)

    h = h.groupby(['playerID', 'yearID', 'lgID'])[CATEGORIES_RAW].sum().reset_index()

    h["BA"] = h["H"] / h["AB"]
    h["SLG"] = (h["H"] + h["2B"] + 2*h["3B"] + 3*h["HR"]) / h["AB"]

    h["QUALIFIED"] = h["AB"] >= 502

    for stat in CATEGORIES_RAW:
        led = h.groupby(['yearID', 'lgID'])[stat].transform(np.max) == h[stat]
        h["led_{}".format(stat)] = led.astype(int)

    q = h.loc[h["QUALIFIED"]].copy()
    # q = q
    for stat in CATEGORIES_CALC:
        led = q.groupby(['yearID', 'lgID'])[stat].transform(np.max) == q[stat]
        q["led_{}".format(stat)] = led.astype(int)

    h = pd.merge(left=h, 
                 right=q[['playerID', 'yearID', 'lgID'] + ["led_{}".format(stat) for stat in CATEGORIES_CALC]],
                 on=['playerID', 'yearID', 'lgID'])

    h["BLACK_INK"] = (4*(h["led_HR"] + h["led_RBI"] + h["led_BA"]) + 
                      3*(h["led_R"] + h["led_H"] + h["led_SLG"]) + 
                      2*(h["led_2B"] + h["led_BB"] + h["led_SB"]) + 
                      1*(h["led_G"] + h["led_AB"] + h["led_3B"]))

    h.sort_values(by="BLACK_INK", inplace=True, ascending=False)

    print(h.head())

    h.to_csv('ink.csv')


'''
Batting Statistics
Four Points for home runs, runs batted in or batting average
Three Points for runs scored, hits or slugging percentage
Two Points for doubles, walks or stolen bases
One Point for games, at bats or triples    
'''

if (__name__ == "__main__"):
    main()