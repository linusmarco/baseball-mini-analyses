import os
import requests
import numpy as np
import pandas as pd
import mlbgame


def games_events(games):
    all_events = []
    for game in games:
        events = mlbgame.events.game_events(game.game_id)
        
        for x in events:
            for y in events[x]:
                for i in events[x][y]:
                    all_events.append(mlbgame.events.AtBat(i))

        # for event in events:
        #     all_events.append(event)
    return all_events


def get_year(year):
    teams = mlbgame.teams()

    all_games = []

    for team in teams:
        # for month in range(1, 13):
        for month in [5]:
            try:
                # games = mlbgame.games(year, month, home=team.club_common_name)
                games = mlbgame.games(year, month, 1, home=team.club_common_name)
            except:
                games = []

            for game in games:
                all_games.append(game)

    return all_games


def main():
    
    games_2015 = mlbgame.combine_games(get_year(2015))
    print(len(games_2015))
    
    events_2015 = games_events(games_2015)
    print(len(events_2015))

    fields = [
        {
            'batter': e.batter, 
            'pitcher': e.pitcher,
            'event': e.event
        }
    for e in events_2015]

    df = pd.DataFrame(fields)

    print(df.head())
    print(df['event'].value_counts())


    


if (__name__ == "__main__"):
    main()



