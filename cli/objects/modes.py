#
# Copyright (C) 2020 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, version 3.
#

import argparse

class OgModes():

	@staticmethod
	def list_available_modes(rest):
		r = rest.get('/mode')
		print(r.json())

	@staticmethod
	def set_modes(rest, args):
		parser = argparse.ArgumentParser()
		parser.add_argument('--scope-id',
				    nargs=1,
				    required=True,
				    help='ID of the scope')
		parser.add_argument('--scope-type',
				    nargs=1,
				    required=True,
				    help='Type of the scope')
		parser.add_argument('--mode',
				    nargs=1,
				    required=True,
				    help='Mode for the scope')
		parsed_args = parser.parse_args(args)

		def scope_lookup(scope_id, scope_type, d):
			if scope_id == d.get('id') and \
			   scope_type == d.get('type'):
				return d
			for scope in d['scope']:
				lookup = scope_lookup(scope_id,
						      scope_type,
						      scope)
				if lookup is not None:
					return lookup
			return None

		def ips_in_scope(scope):
			if 'ip' in scope:
				return [scope['ip']]
			ips = []
			for child in scope['scope']:
				ips += ips_in_scope(child)
			return ips

		r = rest.get('/scopes')
		scopes = r.json()
		found_scope = scope_lookup(int(parsed_args.scope_id[0]),
					   parsed_args.scope_type[0],
					   scopes)

		if found_scope is None:
			print("Scope not found")
			return None

		ips = ips_in_scope(found_scope)

		payload = {'clients': ips, 'mode': parsed_args.mode[0]}
		r = rest.post('/mode', payload=payload)
