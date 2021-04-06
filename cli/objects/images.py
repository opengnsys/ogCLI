#
# Copyright (C) 2021 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, version 3.
#

from urllib.parse import urlparse
from cli.utils import *

import argparse

class OgImage():

	@staticmethod
	def list_images(rest):
		r = rest.get('/images')
		print(r.text)

	@staticmethod
	def restore_image(rest, args):
		parser = argparse.ArgumentParser()
		parser.add_argument('--disk',
				    nargs='?',
				    required=True,
				    help='Disk')
		parser.add_argument('--part',
				    nargs='?',
				    required=True,
				    help='Partition')
		parser.add_argument('--id',
				    nargs='?',
				    type=int,
				    required=True,
				    help='Image id to be restored')
		parser.add_argument('--type',
				    nargs='?',
				    required=True,
				    choices=['unicast', 'unicast-direct'],
				    help='Image id to be restored')
		parser.add_argument('--repo',
				    nargs='?',
				    default=urlparse(rest.URL).netloc.split(':')[0],
				    help='Images repository ip')
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
			print('No clients specified.')
			return

		r = rest.get('/images')
		images = r.json()
		found_image = [img for img in images['images'] if img['id'] == parsed_args.id]
		if not found_image:
			print(f'Image with id {parsed_args.id} not found.')
			return
		else:
			found_image = found_image[0]

		payload = {'disk': parsed_args.disk, 'partition': parsed_args.part,
			   'id': str(parsed_args.id), 'name': found_image['name'],
			   'profile': str(found_image['software_id']),
			   'repository': parsed_args.repo,
			   'type': parsed_args.type.upper(), 'clients': list(ips)}
		r = rest.post('/image/restore', payload=payload)