#
# Copyright (C) 2020 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, version 3.
#

import argparse

class OgClient():

	@staticmethod
	def list_clients(rest):
		r = rest.get('/clients')
		print(r.json())

	@staticmethod
	def list_client_hardware(rest, args):
		parser = argparse.ArgumentParser()
		parser.add_argument('--scope-id',
				    nargs=1,
				    required=True,
				    help='ID of the computer scope')
		parsed_args = parser.parse_args(args)

		payload = {'scope': {'id': int(parsed_args.scope_id[0]),
				     'type': 'computer'}}
		r = rest.get('/hardware', payload=payload)
		print(r.json())
