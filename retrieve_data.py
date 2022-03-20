import sys, requests, operator, json
import types
from functools import reduce
from pprint import pprint
from enum import Enum

API_ROOT = 'https://statsapi.web.nhl.com'
TEAMS_ROUTE = '/api/v1/teams'
FRANCHISES_ROUTE = '/api/v1/franchises'
STANDINGS_ROUTE =  '/api/v1/standings'
STATS_TYPES_ROUTE = '/api/v1/statTypes'

class StatsBy(Enum):
  SEASON = 'statsSingleSeason'
  PACE = 'onPaceRegularSeason'
  YEAR = 'yearByYear'
  HOME_AWAY = 'homeAndAway'
  WIN_LOSS = 'winLoss'
  MONTH = 'byMonth'
  DAY_OF_WEEK = 'byDayOfWeek'
  GAME = 'gameLog'
class StatsVs(Enum):
  DIVISION = 'vsDivision'
  CONFERENCE = 'vsConference'
class StatsMisc(Enum):
  GOALS_BY_SITUATION = 'goalsByGameSituation'
  SEASON_RANKINGS = 'regularSeasonStatRankings'


def main(argv):
  printlb('\n\nRetrieving data...')
  print_player_stats()

#Output
def print_team_stats():
  for team_route in get_team_routes(1):
    pprint(get_team_stats(team_route))

def print_player_stats():
  for player_route in get_player_routes(1):
    print(get_json(player_route)['people'][0]['fullName'])
    stat_params = create_stats_params(StatsBy.SEASON)
    pprint(get_player_stats(player_route, stat_params))

def print_players(num_teams = 1, num_players = None):
  count = 0
  for t, team_route in enumerate(get_team_routes(num_teams)):
    print('\n' + get_json(team_route)['teams'][0]['name'])
    for p, player_route in enumerate(get_roster_routes(team_route, num_players)):
      player_data = get_json(player_route)['people'][0]
      print(f"{player_data['fullName']:24}{player_data['primaryPosition']['type']}")
    count += p + 1
  print('\n' + str(count) + ' players')
  printlb(t + 1, 'teams')


#Stats
def get_player_stats(player_route, params) -> dict:
  return get_json(player_route + '/stats' + params)['stats'][0]['splits']

def get_team_stats(team_route):
  return get_json(team_route + '/stats')['stats']

def create_stats_params(stat_option: Enum, season: str = '20202021'):
  params = '?stats=' + stat_option.value
  if stat_option != StatsBy.YEAR:
    params += '&season=' + season
  return params


# Routes
def get_player_routes(num_teams = 1, num_players = None) -> types.GeneratorType:
  for team_route in get_team_routes(num_teams):
    yield from get_roster_routes(team_route, num_players)

def get_roster_routes(team_route, qty = None) -> types.GeneratorType:
  return get_routes(team_route + '/roster', ['roster'], ['person'], qty)
  # for player in get_json(team_route + '/roster')['roster'][:qty]:
  #   yield player['person']['link']

def get_team_routes(qty = None) -> types.GeneratorType:
  return get_routes(TEAMS_ROUTE, ['teams'], [], qty)
  # for team in get_json(TEAMS_ROUTE)['teams'][:qty]:
  #   yield team['link']


# Generics
def get_routes(base, data_keys, elem_keys = [], qty = None) -> types.GeneratorType:
  for item in get_from_dict(get_json(base), data_keys)[:qty]:
    yield get_from_dict(item, elem_keys)['link']

def get_from_dict(dict, map_list) -> dict:
  return reduce(operator.getitem, map_list, dict)

# Utils
def get_json(route: str) -> dict:
  res = requests.get(API_ROOT + route)
  return res.json()

def printlb(*args, **kwargs):
  print(*args, '\n', **kwargs)


if __name__ == '__main__':
  main(sys.argv[1:])