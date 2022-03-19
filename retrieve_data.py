import sys, requests, json

rootAPI: str = 'https://statsapi.web.nhl.com'
teams_endpoint: str = '/api/v1/teams'

def main(argv):
  res = requests.get(rootAPI + teams_endpoint)
  data = res.json()

if __name__ == '__main__':
  main(sys.argv[1:])