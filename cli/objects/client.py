#
# Copyright (C) 2020 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, version 3.
#

class OgClient():

	@staticmethod
	def list_clients(rest):
		r = rest.get('/clients')
		print(r.json())
