import sys
import types
import requests
import csv
from pprint import pprint


API_ROOT = 'https://statsapi.web.nhl.com'
TEAMS_ROUTE = '/api/v1/teams'
STATS_TYPES_ROUTE = '/api/v1/statTypes'
CONFIGURATIONS_ROUTE = '/api/v1/configurations'


def main(argv):
  print('\n\nRetrieving data...')
  with open ('player_stats.csv',  'w') as f:
    writer = csv.writer(f)
    writer.writerows(output_player_stats())
  
  with open ('goalie_stats.csv',  'w') as f:
    writer = csv.writer(f)
    writer.writerows(output_goalie_stats())


#Output
def output_goalie_stats(stat_type = 'statsSingleSeason'):
  all_stats = []
  header_row = ['Name', 'Position', 'Team']
  for stat_item in (item for item in get_player_stats('/api/v1/people/8476903', create_stats_params(stat_type))[0]['stat'].keys()):
    header_row.append(stat_item)
  all_stats.append(header_row)

  for route, name, pos, team in get_player_info():
    stat_list_obj = get_player_stats(route, create_stats_params(stat_type))
    if len(stat_list_obj) ==  0 or pos != 'Goalie':
      continue
    row = [name, pos, team]
    for stat_item in (item for item in stat_list_obj[0]['stat'].values()):
      row.append(stat_item)
    all_stats.append(row)

  return all_stats

def output_player_stats(stat_type = 'statsSingleSeason'):
  all_stats = []
  header_row = ['Name', 'Position', 'Team']
  for stat_item in (item for item in get_player_stats('/api/v1/people/8474056', create_stats_params(stat_type))[0]['stat'].keys()):
    header_row.append(stat_item)
  all_stats.append(header_row)

  for route, name, pos, team in get_player_info():
    stat_list_obj = get_player_stats(route, create_stats_params(stat_type))
    if len(stat_list_obj) ==  0 or pos == 'Goalie':
      continue
    row = [name, pos, team]
    for stat_item in (item for item in stat_list_obj[0]['stat'].values()):
      row.append(stat_item)
    all_stats.append(row)

  return all_stats

def print_player_stats(num_teams = 1, num_players = None):
  for route, name, pos, team in get_player_info(num_teams, num_players):
    print(name)
    print(pos)
    print(team)
    pprint(get_player_stats(route, create_stats_params('statsSingleSeason')))

def print_team_stats(num_teams = 1):
  for route in get_team_routes(num_teams):
    print(get_team_name(route))
    pprint(get_team_stats(route))

def print_stat_types():
  pprint(get_json(STATS_TYPES_ROUTE))

#Stats
def get_player_stats(player_route, params) -> dict:
  return get_json(player_route + '/stats' + params)['stats'][0]['splits']

def get_team_stats(team_route) -> dict:
  return get_json(team_route + '/stats')['stats']

def create_stats_params(stat_option: str, season: str = '20212022') -> str:
  params = '?stats=' + stat_option
  if 'yearByYear' not in stat_option:
    params += '&season=' + season
  return params

# Routes
def get_player_info(num_teams = None, num_players = None) -> types.GeneratorType:
  for t_route, t_name in ((t['link'], t['name']) for t in get_json(TEAMS_ROUTE)['teams'][:num_teams]):
    for p_route, p_name, p_pos in ((p['person']['link'], p['person']['fullName'], p['position']['name']) \
                                    for p in get_json(t_route + '/roster')['roster'][:num_players]):
      yield p_route, p_name, p_pos, t_name


def get_roster_routes(team_route, qty = None) -> types.GeneratorType:
  for player in get_json(team_route + '/roster')['roster'][:qty]:
    yield player['person']['link']

def get_team_routes(qty = None) -> types.GeneratorType:
  for team in get_json(TEAMS_ROUTE)['teams'][:qty]:
    yield team['link']


# Utility
def get_player_name(route):
  return get_json(route)['people'][0]['fullName']

def get_team_name(route):
  return get_json(route)['teams'][0]['name']

def get_json(route: str) -> dict:
  res = requests.get(API_ROOT + route)
  return res.json()


if __name__ == '__main__':
  main(sys.argv[1:])