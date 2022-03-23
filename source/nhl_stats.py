import sys
import types
import requests
from pprint import pprint
from enum import Enum
from get_data import printlb


API_ROOT = 'https://statsapi.web.nhl.com'
TEAMS_ROUTE = '/api/v1/teams'
FRANCHISES_ROUTE = '/api/v1/franchises'
STANDINGS_ROUTE =  '/api/v1/standings'
STATS_TYPES_ROUTE = '/api/v1/statTypes'

""" STAT TYPES
yearByYear
yearByYearRank
yearByYearPlayoffs
yearByYearPlayoffsRank
careerRegularSeason
careerPlayoffs
gameLog
playoffGameLog
vsTeam
vsTeamPlayoffs
vsDivision
vsDivisionPlayoffs
vsConference
vsConferencePlayoffs
byMonth
byMonthPlayoffs
byDayOfWeek
byDayOfWeekPlayoffs
homeAndAway
homeAndAwayPlayoffs
winLoss
winLossPlayoffs
onPaceRegularSeason
regularSeasonStatRankings
playoffStatRankings
goalsByGameSituation
goalsByGameSituationPlayoffs
statsSingleSeason
statsSingleSeasonPlayoffs
"""


def main(argv):
  print('\n\nRetrieving data...')


#Output
def print_team_stats(num_teams = 1):
  for route in get_team_routes(num_teams):
    print(get_team_name(route))
    pprint(get_team_stats(route))

def print_player_stats(num_teams = 1, num_players = None):
  for route in get_player_routes(num_teams, num_players):
    print(get_player_name(route))
    pprint(get_player_stats(route, create_stats_params('statsSingleSeason')))

def get_team_name(route):
  return get_json(route)['teams'][0]['name']

def get_player_name(route):
  return get_json(route)['people'][0]['fullName']


#Stats
def get_team_stats(team_route) -> dict:
  return get_json(team_route + '/stats')['stats']
  
def get_player_stats(player_route, params) -> dict:
  return get_json(player_route + '/stats' + params)['stats'][0]['splits']

def create_stats_params(stat_option: str, season: str = '20202021') -> str:
  params = '?stats=' + stat_option
  if 'yearByYear' not in stat_option:
    params += '&season=' + season
  return params


# Routes
def get_player_routes(num_teams = None, num_players = None) -> types.GeneratorType:
  for team in get_team_routes(num_teams):
    yield from get_roster_routes(team, num_players)

def get_team_routes(qty = None) -> types.GeneratorType:
  for team in get_json(TEAMS_ROUTE)['teams'][:qty]:
    yield team['link']

def get_roster_routes(team_route, qty = None) -> types.GeneratorType:
  for player in get_json(team_route + '/roster')['roster'][:qty]:
    yield player['person']['link']


def get_json(route: str) -> dict:
  res = requests.get(API_ROOT + route)
  return res.json()


if __name__ == '__main__':
  main(sys.argv[1:])