# Copyright (C) 2020-2021 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import json

class OgScope():

	@staticmethod
	def list_scopes(rest):
		r = rest.get('/scopes')
		payload = json.loads(r.text)
		print(json.dumps(payload, sort_keys=True, indent=2))
