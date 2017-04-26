import os
import sys
import numpy as np
import pandas as pd


EVENT_DATA = "C:/Users/LMarco/Documents/02_Linus's Projects/RetroSheet/2016.CSV"
ROSTERS = "C:/Users/LMarco/Documents/02_Linus's Projects/RetroSheet"


def get_rosters(folder):
    files = os.listdir(folder)
    rosters = [r for r in files if r.upper().endswith(".ROS")]
    players = pd.DataFrame()
    for r in rosters:
        tm = pd.read_csv(os.path.join(folder, r), header=None)
        players = players.append(tm)
    
    players.rename(columns={
        0: 'ID',
        1: 'LAST',
        2: 'FIRST'
    }, inplace=True)
    players = players.drop_duplicates(subset='ID')[['ID', 'FIRST', 'LAST']]

    return players


def merge_names(matchups, players):
    for p in ['BAT', 'PIT']:
        matchups = matchups.merge(players,  
                                  left_on='{}_ID'.format(p), 
                                  right_on='ID', 
                                  how='left')
        matchups.drop('ID', axis=1, inplace=True)
        matchups.rename(columns={
            'LAST': '{}_LAST'.format(p),
            'FIRST': '{}_FIRST'.format(p)
        }, inplace=True)

    return matchups


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
    matchups = filter_mins(matchups, 'BAT_ID', 100)
    matchups = filter_mins(matchups, 'PIT_ID', 100)

    # calculate outcomes
    calc_outcomes(matchups)

    # add names from rosters
    players = get_rosters(ROSTERS)
    matchups = merge_names(matchups, players)

    print(matchups.info())
    print(matchups.head())
    

if (__name__ == "__main__"):
    main()

