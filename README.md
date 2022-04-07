# pccs-policy-playground


## Requirements

Python: >= 3
pipenv 

## Installation

If you don't have pipenv installed, [install it first](https://pipenv.pypa.io/en/latest/install/#pragmatic-installation-of-pipenv). 
```shell
pip install --user pipenv
```
Install project dependencies. 
```shell
pipenv install
```

## Usage

### Required authentication details

The following environment variables need to be set. 

```shell
export PC_API_URL=https://api.prismacloud.io
export PC_ACCESS_KEY=<your-access-key>
export PC_SECRET_KEY=<your-secret-key>
```
Alternatively, you can pass them as a command line argument like below:

```shell
python pccs/main.py --auth "https://api.prismacloud.io::<your-access-key>::<your-secret-key>"
```

> Note: You may need to run off VPN for using these scripts.

### List custom policies

- List all custom policies (summary):
```shell
python pccs/main.py --list
```
- List all custom policies (verbose):
```shell
python pccs/main.py --list --verbose
```
- Get custom policy by ID:
```shell
python pccs/main.py --policy-id xxxxxxx 
```


