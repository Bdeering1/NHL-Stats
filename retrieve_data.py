import sys, requests, operator, json
import types
from functools import reduce
from pprint import pprint

API_ROOT = 'https://statsapi.web.nhl.com'
TEAMS_ROUTE = '/api/v1/teams'
TEAM_STATS_PARAM = '?expand=team.stats'

def main(argv):
  print('\n\nRetrieving data...\n\n')
  count = 0
  for team_route in get_team_routes():
    for idx, player_route in enumerate(get_player_routes(team_route)):
      pprint(player_route)
    count += idx + 1
    # count += sum(1 for _ in get_player_routes(team_route))
  print(count, 'total values\n')


def get_player_routes(team_route, qty = -1) -> types.GeneratorType:
  return get_routes(team_route + '/roster', ['roster'], ['person'], qty)
  # for player in get_json(team_route + '/roster')['roster'][:qty]:
  #   yield player['person']['link']

def get_team_routes(qty = -1) -> types.GeneratorType:
  return get_routes(TEAMS_ROUTE, ['teams'], [], qty)
  # for team in get_json(TEAMS_ROUTE)['teams'][:qty]:
  #   yield team['link']


def get_json(route: str) -> dict:
  res = requests.get(API_ROOT + route)
  return res.json()


# Generics
def get_routes(base, data_keys, elem_keys = [], qty = -1) -> types.GeneratorType:
  for item in get_from_dict(get_json(base), data_keys)[:qty]:
    yield get_from_dict(item, elem_keys)['link']

def get_from_dict(dict, map_list) -> dict:
  return reduce(operator.getitem, map_list, dict)


if __name__ == '__main__':
  main(sys.argv[1:])