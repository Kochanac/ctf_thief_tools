#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

ln -sf $DIR/dumper.py /usr/local/bin/dumper
ln -sf $DIR/cat_task.py /usr/local/bin/cattask
ln -sf $DIR/ls_tasks.py /usr/local/bin/lstasks
ln -sf $DIR/set_attr.py /usr/local/bin/setattr
