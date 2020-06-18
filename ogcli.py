#!/usr/bin/python

from ogcli.ogcli import OgCLI
import argparse
import json
import sys

OG_CLI_CFG_PATH="/opt/opengnsys/etc/ogcli.json"

class CLI():
	def __init__(self):
		try:
			with open(OG_CLI_CFG_PATH, 'r') as json_file:
				self.cfg = json.load(json_file)
		except json.JSONDecodeError:
			sys.exit(f'ERROR: Failed parse malformed JSON file '
				f'{OG_CLI_CFG_PATH}')
		except:
			sys.exit(f'ERROR: cannot open {OG_CLI_CFG_PATH}')

		self.ogcli = OgCLI(self.cfg)

		parser = argparse.ArgumentParser(prog='ogcli')
		parser.add_argument('command', help='Subcommand to run')
		args = parser.parse_args(sys.argv[1:2])

		if not hasattr(self, args.command):
			parser.print_help()
			sys.exit('Unknown command')

		# Call the command with the same name.
		getattr(self, args.command)(sys.argv[2:])

	def list(self, args):
		parser = argparse.ArgumentParser()
		parser.add_argument('item', choices=['clients'])
		parser.parse_args(args)

		if parser.item == 'clients':
			self.ogcli.client_list()

if __name__ == "__main__":
	CLI()
