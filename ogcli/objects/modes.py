class OgModes():

	@staticmethod
	def list_available_modes(rest):
		r = rest.get('/modes')
		print(r.json())
