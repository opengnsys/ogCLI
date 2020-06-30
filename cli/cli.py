from cli.objects.client import OgClient
from cli.objects.scopes import OgScope
from cli.objects.modes import OgModes
import argparse
import requests
import sys

class OgREST():
	def __init__(self, ip, port, api_token):
		self.URL = f'http://{ip}:{port}'
		self.HEADERS = {'Authorization' : api_token}

	def get(self, path):
		try:
			r = requests.get(f'{self.URL}{path}',
					 headers=self.HEADERS)
			if r.status_code != 200:
				sys.exit(f"Cannot connect to ogServer: "
					 f"{r.status_code} HTTP status code")
		except IOError as e:
			sys.exit(f"Cannot connect to ogServer: {e}")
		return r

class OgCLI():
	def __init__(self, cfg):
		self.rest = OgREST(cfg['ip'], cfg['port'], cfg['api_token'])

	def list(self, args):
		choices = ['clients', 'scopes', 'modes']
		parser = argparse.ArgumentParser()
		parser.add_argument('item', choices=choices)
		args = parser.parse_args(args)

		if args.item == 'clients':
			OgClient.list_clients(self.rest)
		elif args.item == 'modes':
			OgModes.list_available_modes(self.rest)
		elif args.item == 'scopes':
			OgScope.list_scopes(self.rest)
