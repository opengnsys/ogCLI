
# ogCLI

Manage your OpenGnsys environment from your command line. A CLI for the ogServer
REST API.

## Installation

This tool is expected to be executed from the OpenGnsys installation environment.

**Before running any command copy `ogcli.json` inside `/opt/opengnsys/etc/`**

## Usage

`ogcli {command} {object} [{command object options}]`

### Commands

#### `list`

You can list currently connected clients, managed scopes,
boot modes, hardware profiles and specific client information.

```
usage: ogcli list [-h] {clients,scopes,modes,hardware,client}

positional arguments:
  {clients,scopes,modes,hardware,client}

optional arguments:
  -h, --help            show this help message and exit
```

#### `set`

Set properties of the managed computers.

You can modify boot mode using `set`.

```
usage: ogcli set [-h] {modes}

positional arguments:
  {modes}

positional arguments:
  {modes}

optional arguments:
  -h, --help  show this help message and exit
```

### Objects

They are subject to the specified command.

* `clients`: Currently connected clients to the ogServer
* `client`: Any specific client
* `modes`: Network boot modes
* `hardware`: Hardware profiles
* `scopes`: Managed computers, rooms and centers.

### Examples

#### Changing the boot mode of computers in a particular classroom

##### Fetching a classroom id

```
ogcli list scopes

{'scope': [{'name': 'Unidad Organizativa (Default)', 'type': 'center', 'id': 1, 'scope': [{'name': 'Aula virtual', 'type': 'room', 'id': 1, ...
```

##### Fetching net boot modes

```
ogcli list modes

{'modes': ['11', 'pxe', '00unknown', '19pxeADMIN', '13', '10', '12']}
```

##### Changing boot mode of the classroom

```
ogcli set modes --room-id 1 --mode pxe
```

## License

ogCLI is released under the GNU Affero Public License v3

## Authors

[Soleta Networks](https://opengnsys.soleta.eu)
