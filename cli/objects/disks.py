#
# Copyright (C) 2021 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, version 3.
#

import argparse

class OgDisk():

	@staticmethod
	def list_disks(rest, args):
		parser = argparse.ArgumentParser()
		parser.add_argument('--client-ip',
				   nargs='?',
				   required=True,
				   help='Client IP to query')
		parsed_args = parser.parse_args(args)
		payload = {'client': [parsed_args.client_ip]}

		r = rest.get('/client/setup', payload=payload)
		print(r.text)
