# Copyright (C) 2020-2021 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import argparse

from cli.utils import print_json

class OgScope():

	@staticmethod
	def list_scopes(rest):
		r = rest.get('/scopes')
		print_json(r.text)
