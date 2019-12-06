# ctf_thief_tools

## Usage:

copy request to one of tasks json (RMB -> "copy request headers" in firefox) and save it to /tmp/request

`install.sh` will link scripts to /usr/local/sbin

`dumper ctfd 1-100` in empty directory will dump tasks

`cattask ./task1`

`lstasks`

`setattr Solved True task1` - mark task1 as solved

## supported boards:
* ctfd

* ctforces (ctforces.com)