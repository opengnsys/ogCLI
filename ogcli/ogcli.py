import requests

class OgCLI():
	def __init__(self, cfg):
		self.api_token = cfg['api_token']

	def client_list(self):
		headers = {'Authorization' : self.api_token}
		try:
			r = requests.get('http://127.0.0.1:8888/clients',
                                         headers=headers)
			if r.status_code != 200:
				sys.exit(f"Cannot connect to ogServer: "
                                         f"{r.status_code} HTTP status code")
		except IOError as e:
			sys.exit(f"Cannot connect to ogServer: {e}")

		print(r.json())
