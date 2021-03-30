#
# Copyright (C) 2020 Soleta Networks <info@soleta.eu>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, version 3.
#

def scope_lookup(scope_id, scope_type, d):
	if scope_id == d.get('id') and scope_type == d.get('type'):
		return d
	for scope in d['scope']:
		lookup = scope_lookup(scope_id, scope_type, scope)
		if lookup is not None:
			return lookup
	return None

def ips_in_scope(scope):
	if scope is None:
		return []
	if 'ip' in scope:
		return [scope['ip']]
	ips = []
	for child in scope['scope']:
		ips += ips_in_scope(child)
	return ips
