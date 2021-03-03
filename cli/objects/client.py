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
		parser.add_argument('--client-ip',
				    nargs=1,
				    type=str,
				    required=True,
				    help='client IP')
		parsed_args = parser.parse_args(args)

		payload = {'client': parsed_args.client_ip}
		r = rest.get('/hardware', payload=payload)
		print(r.json())

	@staticmethod
	def get_client_properties(rest, args):
		parser = argparse.ArgumentParser()
		parser.add_argument('--client-ip',
				    nargs=1,
				    required=True,
				    help='client IP')
		parsed_args = parser.parse_args(args)

		payload = {'client': parsed_args.client_ip}
		r = rest.get('/client/info', payload=payload)
		print(r.json())
