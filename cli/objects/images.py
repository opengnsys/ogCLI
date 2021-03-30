#
# Copyright (C) 2021 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, version 3.
#

class OgImage():

	@staticmethod
	def list_images(rest):
		r = rest.get('/images')
		print(r.text)
