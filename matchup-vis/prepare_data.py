import os
import numpy as np
import pandas as pd


EVENT_DATA = "C:/Users/LMarco/Documents/02_Linus's Projects/RetroSheet/2016.CSV"


def make_dummy(df, col):
    df.loc[df[col] == 'T', col] = 1
    df.loc[df[col] == 'F', col] = 0
    assert df[col].isin([1, 0]).all()
    df[col] = pd.to_numeric(df[col])


def make_outcome_flags(df):
    df['1B'] = (df['EVENT_CD'] == 20).astype(int)
    df['2B'] = (df['EVENT_CD'] == 21).astype(int)
    df['3B'] = (df['EVENT_CD'] == 22).astype(int)
    df['HR'] = (df['EVENT_CD'] == 23).astype(int)
    df['H'] = (df['1B'] + df['2B'] + df['3B'] + df['HR']).astype(int)
    df['BB'] = (df['EVENT_CD'] == 14).astype(int)
    df['IBB'] = (df['EVENT_CD'] == 15).astype(int)
    df['HBP'] = (df['EVENT_CD'] == 16).astype(int)


def collapse_matchups(df, ids, vals):
    d = df[ids + vals]
    grouped = d.groupby(ids)
    grouped = grouped.sum().reset_index()
    return grouped


def filter_mins(df, idvar, rank):
    top = df.groupby(idvar).size().nlargest(rank).reset_index()[idvar]
    df = df[df[idvar].isin(top)]
    return df


def calc_outcomes(df):
    df['AVG'] = df['H'] / df['AB']
    df['OBP'] = (df['H'] + df['BB'] + df['IBB'] + df['HBP']) / (df['AB'] + df['BB'] + df['IBB'] + df['HBP'] + df['SF'])
    df['SLG'] = (df['1B'] + 2*df['2B'] + 3*df['3B'] + 4*df['HR']) / df['AB']
    df['OPS'] = df['OBP'] + df['SLG']


def main():
    
    # read event data
    df = pd.read_csv(EVENT_DATA)

    # clean up fields
    make_dummy(df, 'BAT_EVENT_FL')
    make_dummy(df, 'AB_FL')
    make_dummy(df, 'SH_FL')
    make_dummy(df, 'SF_FL')
    df.rename(columns={
        'RESP_BAT_ID': 'BAT_ID',
        'RESP_PIT_ID': 'PIT_ID',
        'AB_FL': 'AB',
        'SH_FL': 'SH',
        'SF_FL': 'SF'
    }, inplace=True)

    # filter to batting events (i.e no pickoffs, steals, etc.)
    df = df[df['BAT_EVENT_FL'] == 1]
    df.drop('BAT_EVENT_FL', axis=1, inplace=True)

    # var creation
    make_outcome_flags(df)

    # collapse
    ids = ['BAT_ID', 'PIT_ID']
    vals = ['AB', '1B', '2B', '3B', 'HR', 'H', 'BB', 'IBB', 'HBP', 'SF']
    df = df[df[vals].sum(axis=1) > 0]
    matchups = collapse_matchups(df, ids, vals)    

    # filter on minimums
    matchups = filter_mins(matchups, 'BAT_ID', 200)
    matchups = filter_mins(matchups, 'PIT_ID', 200)

    # calculate outcomes
    calc_outcomes(matchups)

    print(matchups.info())
    print(matchups.head())
    

if (__name__ == "__main__"):
    main()

