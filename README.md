
# ogCLI

Manage your OpenGnsys environment from your command line. A CLI for the ogServer
REST API.

## Installation

This tool is expected to be executed from the OpenGnsys installation environment.

**Before running any command copy `ogcli.json` inside `/opt/opengnsys/etc/`**

## Usage

`ogcli {command} {object} [{command object options}]`

### Commands

```
usage: ogcli [-h] [{create,list,restore,send,set,setup}]

positional arguments:
  {create,list,restore,send,set,setup}
                        Subcommand to run

options:
  -h, --help            show this help message and exit
```

#### `create`

Create images.

```
usage: ogcli create [-h] {image}

positional arguments:
  {image}

options:
  -h, --help  show this help message and exit
```

#### `list`

You can list currently connected clients, disk, scope tree,
boot modes, hardware/software profiles, images, and specific client information.

```
usage: ogcli list [-h] {clients,scopes,modes,hardware,client,images,disks}

positional arguments:
  {clients,scopes,modes,hardware,client,images,disks}

options:
  -h, --help            show this help message and exit
```

#### `restore`

Restore an image partition

```
usage: ogcli restore [-h] {image}

positional arguments:
  {image}

options:
  -h, --help  show this help message and exit
```

#### `send`

Send WoL, poweroff or refresh to a given scope.

```
usage: ogcli send [-h] {wol,poweroff,refresh}

positional arguments:
  {wol,poweroff,refresh}

options:
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

#### `setup`

Setup disks of a given scope

```
usage: ogcli setup [-h] {disk}

positional arguments:
  {disk}

options:
  -h, --help  show this help message and exit
```

### Objects

They are subject to the specified command.

* `clients`: Currently connected clients to the ogServer
* `client`: Any specific client
* `disk`: Client's disks
* `images`: Partition images
* `modes`: Network boot modes
* `hardware`: Hardware profiles
* `scopes`: Scope tree of managed computers, rooms and centers.

### Examples

#### Client setup

##### DOS/MBR, first partition: 40G Linux/ext4, also add a 10G OpenGnsys cache partition. Format each partition.
```
ogcli setup disk --type dos --part 1,LINUX,EXT4,40G --part 4,CACHE,CACHE,10G --format 1,4 --client-ip 192.168.56.11
```

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
