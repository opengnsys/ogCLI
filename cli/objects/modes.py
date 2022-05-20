# Copyright (C) 2020-2021 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

from cli.utils import *

import argparse


class OgModes():

    @staticmethod
    def list_available_modes(rest):
        r = rest.get('/mode')
        print(r.text)

    @staticmethod
    def set_modes(rest, args):
        parser = argparse.ArgumentParser(prog='ogcli set mode')
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
        parser.add_argument('--mode',
                            nargs=1,
                            required=True,
                            help='Boot mode to be set')
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

        payload = {'clients': list(ips), 'mode': parsed_args.mode[0]}
        r = rest.post('/mode', payload=payload)
