class OgScope():

	@staticmethod
	def list_scopes(rest):
		r = rest.get('/scopes')
		print(r.json())
