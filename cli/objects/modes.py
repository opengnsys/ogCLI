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
		print(r.text)

	@staticmethod
	def set_modes(rest, args):
		parser = argparse.ArgumentParser()
		group = parser.add_argument_group('clients', 'Client selection args')
		group.add_argument('--center-id',
				   type=int,
				   action='append',
				   default=[],
				   required=False,
				   help='Clients from given center id')
		group.add_argument('--room-id',
				   type=int,
				   action='append',
				   default=[],
				   required=False,
				   help='Clients from given room id')
		group.add_argument('--client-ip',
				   action='append',
				   default=[],
				   required=False,
				   help='Specific client IP')
		parser.add_argument('--mode',
				    nargs=1,
				    required=True,
				    help='Boot mode to be set')
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
		ips = set()

		for center in parsed_args.center_id:
			center_scope = scope_lookup(center, 'center', scopes)
			ips.update(ips_in_scope(center_scope))
		for room in parsed_args.room_id:
			room_scope = scope_lookup(room, 'room', scopes)
			ips.update(ips_in_scope(room_scope))
		for l in parsed_args.client_ip:
			ips.add(l)

		if not ips:
			print("No clients found")
			return None

		payload = {'clients': list(ips), 'mode': parsed_args.mode[0]}
		r = rest.post('/mode', payload=payload)
