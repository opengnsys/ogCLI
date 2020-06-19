class OgClient():

	@staticmethod
	def list_clients(rest):
		r = rest.get('/clients')
		print(r.json())
