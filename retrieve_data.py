import sys, requests, json
from pprint import pprint

rootAPI = 'https://statsapi.web.nhl.com'
all_teams_endpoint = '/api/v1/teams'

def main(argv):
  teams_json = get_json(rootAPI + all_teams_endpoint)
  for item in teams_json['teams']:
    team_data = get_json(rootAPI + item['link'])
    pprint(team_data['teams'])

def get_json(url: str) -> dict:
  res = requests.get(url)
  return res.json()

if __name__ == '__main__':
  main(sys.argv[1:])