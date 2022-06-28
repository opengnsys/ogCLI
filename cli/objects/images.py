# Copyright (C) 2020-2021 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

from urllib.parse import urlparse
from cli.utils import *

import argparse


class OgImage():

    @staticmethod
    def list_images(rest):
        r = rest.get('/images')
        print_json(r.text)

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
                            required=False,
                            choices=['unicast',
                                     'unicast-direct', 'tiptorrent'],
                            default='tiptorrent',
                            help='Transfer method. (Default: tiptorrent)')
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
        found_image = [img for img in images['images']
                       if img['id'] == parsed_args.id]
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

    @staticmethod
    def create_image(rest, args):
        parser = argparse.ArgumentParser()
        parser.add_argument('--disk',
                            nargs='?',
                            required=True,
                            help='Disk')
        parser.add_argument('--part',
                            nargs='?',
                            required=True,
                            help='Partition')
        parser.add_argument('--name',
                            nargs='?',
                            required=True,
                            help='Image name')
        parser.add_argument('--desc',
                            nargs='?',
                            required=False,
                            help='Image description (for new images)')
        parser.add_argument('--repo-id',
                            nargs='?',
                            default=1,
                            help='Images repository id')
        group = parser.add_argument_group('clients', 'Client selection args')
        group.add_argument('--client-ip',
                           action='append',
                           default=[],
                           required=True,
                           help='Specific client IP')
        parsed_args = parser.parse_args(args)

        r = rest.get('/client/info', payload={'client': parsed_args.client_ip})
        center_id = r.json()['center']

        r = rest.get('/client/setup',
                     payload={'client': parsed_args.client_ip})
        if r.status_code == 200:
            part_info = list(filter(lambda x: x['disk'] == int(parsed_args.disk) and
                             x['partition'] == int(parsed_args.part),
                             r.json()['partitions']))
            if not part_info:
                print('Partition not found.')
                return
            fs_code = list(part_info)[0]['code']

        payload = {'clients': parsed_args.client_ip, 'disk': parsed_args.disk, 'center_id': center_id,
                   'partition': parsed_args.part, 'code': str(fs_code), 'name': parsed_args.name,
                   'id': '0'}
        if parsed_args.desc:
            payload['description'] = parsed_args.desc
            payload['repository_id'] = parsed_args.repo_id

        rest.post('/image/create', payload=payload)
