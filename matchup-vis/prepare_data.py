import os
import numpy as np
import pandas as pd


EVENT_DATA = "C:/Users/LMarco/Documents/02_Linus's Projects/RetroSheet/2016.CSV"


def make_dummy(df, col):
    df.loc[df[col] == 'T', col] = True
    df.loc[df[col] == 'F', col] = False
    assert df[col].isin([True, False]).all()
    df[col] = pd.to_numeric(df[col])


def make_outcome_flags(df):
    df['1B'] = df['EVENT_CD'] == 20
    df['2B'] = df['EVENT_CD'] == 21
    df['3B'] = df['EVENT_CD'] == 22
    df['HR'] = df['EVENT_CD'] == 23
    df['BB'] = df['EVENT_CD'] == 14
    df['IBB'] = df['EVENT_CD'] == 15
    df['HBP'] = df['EVENT_CD'] == 16


def collapse_matchups(df, ids, vals):
    d = df[ids + vals]
    grouped = d.groupby(ids)
    grouped = grouped.sum().reset_index()
    return grouped


def filter_mins(df, idvar, rank):
    top = df.groupby(idvar).size().nlargest(rank).reset_index()[idvar]
    df = df[df[idvar].isin(top)]
    return df


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
    df = df[df['BAT_EVENT_FL']]
    df.drop('BAT_EVENT_FL', axis=1, inplace=True)

    # var creation
    make_outcome_flags(df)

    # collapse
    ids = ['BAT_ID', 'PIT_ID']
    vals = ['AB', '1B', '2B', '3B', 'HR', 'BB', 'IBB', 'HBP', 'SF']
    df = df[df[vals].sum(axis=1) > 0]
    matchups = collapse_matchups(df, ids, vals)    

    # filter on minimums
    matchups = filter_mins(matchups, 'BAT_ID', 200)
    matchups = filter_mins(matchups, 'PIT_ID', 200)

    print(matchups.info())
    print(matchups.head())
    

if (__name__ == "__main__"):
    main()

