#
# Copyright (C) 2020 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, version 3.
#

from cli.objects.client import OgClient
from cli.objects.scopes import OgScope
from cli.objects.modes import OgModes
from cli.objects.wol import OgWol
from cli.objects.images import OgImage
import argparse
import requests
import sys

class OgREST():
	def __init__(self, ip, port, api_token):
		self.URL = f'http://{ip}:{port}'
		self.HEADERS = {'Authorization' : api_token}

	def get(self, path, payload=None):
		try:
			r = requests.get(f'{self.URL}{path}',
					 headers=self.HEADERS,
					 json=payload)
			if r.status_code != 200:
				sys.exit(f"Cannot connect to ogServer: "
					 f"{r.status_code} HTTP status code")
		except IOError as e:
			sys.exit(f"Cannot connect to ogServer: {e}")
		return r

	def post(self, path, payload):
		try:
			r = requests.post(f'{self.URL}{path}',
					  headers=self.HEADERS,
					  json=payload)
			print(r.text)
			if r.status_code not in {200, 202}:
				sys.exit(f"Cannot connect to ogServer: "
					 f"{r.status_code} HTTP status code")
		except IOError as e:
			sys.exit(f"Cannot connect to ogServer: {e}")
		return r

class OgCLI():
	def __init__(self, cfg):
		self.rest = OgREST(cfg['ip'], cfg['port'], cfg['api_token'])

	def list(self, args):
		choices = ['clients', 'scopes', 'modes', 'hardware',
			   'client', 'images']
		parser = argparse.ArgumentParser(prog='ogcli list')
		parser.add_argument('item', choices=choices)
		parsed_args = parser.parse_args([args[0]])

		if parsed_args.item == 'clients':
			OgClient.list_clients(self.rest)
		elif parsed_args.item == 'client':
			OgClient.get_client_properties(self.rest, args[1:])
		elif parsed_args.item == 'hardware':
			OgClient.list_client_hardware(self.rest, args[1:])
		elif parsed_args.item == 'modes':
			OgModes.list_available_modes(self.rest)
		elif parsed_args.item == 'scopes':
			OgScope.list_scopes(self.rest)
		elif parsed_args.item == 'images':
			OgImage.list_images(self.rest)

	def set(self, args):
		choices = ['modes']
		parser = argparse.ArgumentParser(prog='ogcli set')
		parser.add_argument('item', choices=choices)
		parsed_args = parser.parse_args([args[0]])

		if parsed_args.item == 'modes':
			OgModes.set_modes(self.rest, args[1:])

	def send(self, args):
		choices = ['wol']
		parser = argparse.ArgumentParser(prog='ogcli send')
		parser.add_argument('send_obj', choices=choices)
		parsed_args = parser.parse_args([args[0]])

		if parsed_args.send_obj == 'wol':
			OgWol.send_wol(self.rest, args[1:])
