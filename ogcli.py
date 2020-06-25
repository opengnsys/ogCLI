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

		required_cfg_params = {'api_token', 'ip', 'port'}
		difference_cfg_params = required_cfg_params - self.cfg.keys()
		if len(difference_cfg_params) > 0:
			sys.exit(f'Missing {difference_cfg_params} key in '
				 f'json config file')

		self.ogcli = OgCLI(self.cfg)

		parser = argparse.ArgumentParser(prog='ogcli')
		parser.add_argument('command', help='Subcommand to run')
		args = parser.parse_args(sys.argv[1:2])

		if not hasattr(self.ogcli, args.command):
			parser.print_help()
			sys.exit('Unknown command')

		# Call the command with the same name.
		getattr(self.ogcli, args.command)(sys.argv[2:])

if __name__ == "__main__":
	CLI()
