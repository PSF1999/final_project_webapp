import pandas as pd
import numpy as np

df_matches = pd.read_csv('datasets/matches.csv')
df_players = pd.read_csv('datasets/players.csv')
def getCity():
    city = df_matches['city'].dropna().unique().tolist()
    return city
def getVenue():
    venue = df_matches['venue'].dropna().unique().tolist()
    return venue
def getTeams():
    teams = df_matches['team1'].dropna().unique().tolist()
    return teams
def getPlayers():
    players = df_players['NAME'].dropna().unique().tolist()
    return players