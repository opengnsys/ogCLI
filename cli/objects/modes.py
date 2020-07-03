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
		r = rest.get('/modes')
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

		payload = {'scope': {'id': int(parsed_args.scope_id[0]),
				     'type': parsed_args.scope_type[0]},
			   'mode': parsed_args.mode[0]}
		r = rest.post('/modes', payload=payload)
