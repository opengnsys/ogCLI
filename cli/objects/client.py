# Copyright (C) 2020-2021 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import argparse

class OgClient():

	@staticmethod
	def list_clients(rest):
		r = rest.get('/clients')
		print(r.text)

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
		print(r.text)

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
		print(r.text)
