# Copyright (C) 2020-2021 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import argparse
import re

from cli.utils import print_json

class OgDisk():

	@staticmethod
	def list_disks(rest, args):
		parser = argparse.ArgumentParser()
		parser.add_argument('--client-ip',
				   nargs='?',
				   required=True,
				   help='Client IP to query')
		parsed_args = parser.parse_args(args)
		payload = {'client': [parsed_args.client_ip]}

		r = rest.get('/client/setup', payload=payload)
		print_json(r.text)

	@staticmethod
	def setup_disk(rest, args):
		def parse_size(size):
			size = size.upper()
			units = {"M": 10**3, "G": 10**6, "T": 10**9} # Mapped to K
			# size = re.sub(r'(\d+)([MGT])', r'\1 \2', size)
			match = re.match(r'(\d+)([MGT])', size)
			if match:
				if len(match.groups()) == 2:
					number, unit = match.groups()
					return str(int(float(number)*units[unit]))
			print(f'Error parsing size {size}. Aborting.')
			return None

		disk_type_map = {'dos': 'MSDOS', 'gpt': 'GPT'}
		part_types = ['LINUX', 'EFI', 'WINDOWS', 'CACHE']
		fs_types = ['EXT4', 'FAT32', 'NTFS', 'CACHE']

		parser = argparse.ArgumentParser()
		parser.add_argument('--type',
				    nargs='?',
				    required=True,
				    choices=['dos','gpt'],
				    help='Disk partition scheme')
		parser.add_argument('--num',
				    nargs='?',
				    default=1,
				    help='Disk number (defaults to 1)')
		parser.add_argument('--format',
				    nargs='?',
				    const=True,
				    type=lambda x: x.split(','),
				    help='Indicates which partitions to reformat if they are already present. '\
					 'Use --part alone to mean all partitions.')
		parser.add_argument('--part',
				    nargs='+',
				    action='append',
				    type=lambda x: x.split(','),
				    required=True,
				    help='Partition definition (syntax: "num,part_scheme,fs,size")')
		group = parser.add_argument_group('clients', 'Client selection args')
		group.add_argument('--center-id',
				   type=int,
				   action='append',
				   default=[],
				   required=False,
				   help='Clients from given center id')
		group.add_argument('--room-id',
				   type=int,
				   action='append',
				   default=[],
				   required=False,
				   help='Clients from given room id')
		group.add_argument('--client-ip',
				   action='append',
				   default=[],
				   required=False,
				   help='Specific client IP')

		parsed_args = parser.parse_args(args)
		r = rest.get('/scopes')
		scopes = r.json()
		ips = set()

		for center in parsed_args.center_id:
			center_scope = scope_lookup(center, 'center', scopes)
			ips.update(ips_in_scope(center_scope))
		for room in parsed_args.room_id:
			room_scope = scope_lookup(room, 'room', scopes)
			ips.update(ips_in_scope(room_scope))
		for l in parsed_args.client_ip:
			ips.add(l)
		if not ips:
			print("No clients found")
			return None

		payload = {'clients': parsed_args.client_ip, 'type': disk_type_map[parsed_args.type], 'disk': str(parsed_args.num),
			   'cache': '0', 'cache_size': '0', 'partition_setup': []}
		for i, p in enumerate(parsed_args.part, start=1):
			p = p[0]
			part_num, code, fs, size = p[0], p[1].upper(), p[2].upper(), p[3]

			if code not in part_types:
			    print(f'Specified partition type {code} is not supported. Aborting...')
			    return
			if fs not in fs_types:
			    print(f'Specified filesystem {code} is not supported. Aborting...')
			    return
			size = parse_size(size)

			for j in range(i, int(part_num)):
				part = {'partition': str(j), 'code':'EMPTY',
					'filesystem': 'EMPTY', 'size': '0',
					'format': '0'}
				payload['partition_setup'].append(part)

			if parsed_args.format is True or (type(parsed_args.format) == list and part_num in parsed_args.format):
			    do_format = '1'
			else:
			    do_format = '0'

			if fs == 'CACHE':
				payload['cache'] = '1'	# Assuming flag specifying if there's cache in the setup
				payload['cache_size'] = size
			part = {'partition': str(p[0]), 'code':code.upper(),
				'filesystem': fs.upper(), 'size': size,
				'format': do_format}
			payload['partition_setup'].append(part)

		last_partnum = int(parsed_args.part[-1][0][0])
		# Pad with empty partitions if no 4th part was defined
		for i in range(last_partnum + 1, 5):
			part = {'partition': str(i), 'code':'EMPTY',
				'filesystem': 'EMPTY', 'size': '0',
				'format': '0'}
			payload['partition_setup'].append(part)

		rest.post('/setup', payload=payload)
