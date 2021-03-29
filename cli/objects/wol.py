#
# Copyright (C) 2021 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, version 3.
#

from cli.utils import *

import argparse

class OgWol():

	@staticmethod
	def send_wol(rest, args):
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

		parser = argparse.ArgumentParser()
		parser.add_argument('--type',
				    nargs='?',
				    choices=['broadcast','unicast'],
				    default='broadcast',
				    help='')
		group = parser.add_argument_group('clients', 'Client selection options')
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
		parsed_args = parser.parse_args(args)

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

		payload = {'type': parsed_args.type, 'clients': list(ips)}
		r = rest.post('/wol', payload=payload)
