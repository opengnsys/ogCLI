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
		parser.add_argument('--scope-name',
				    nargs=1,
				    required=True,
				    help='Name of the scope (room or computer)')
		parser.add_argument('--mode',
				    nargs=1,
				    required=True,
				    help='Mode for the scope')
		parsed_args = parser.parse_args(args)

		payload = {'scope_name': parsed_args.scope_name[0],
			   'mode': parsed_args.mode[0]}
		r = rest.post('/modes', payload=payload)
