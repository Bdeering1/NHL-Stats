import sys
import requests
import operator
import types
from functools import reduce


api_root: str


def main(argv):
  print('\n\nRetrieving data...')


def get_routes(base, data_keys, elem_keys = [], qty = None) -> types.GeneratorType:
  for item in get_from_dict(get_json(base), data_keys)[:qty]:
    yield get_from_dict(item, elem_keys)['link']

def get_from_dict(dict, map_list) -> dict:
  return reduce(operator.getitem, map_list, dict)


def get_json(full_path: str) -> dict:
  res = requests.get(full_path)
  return res.json()


if __name__ == '__main__':
  main(sys.argv[1:])