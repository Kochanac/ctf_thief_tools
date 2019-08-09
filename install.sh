#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

ln -sf $DIR/dumper.py /usr/local/sbin/dumper
ln -sf $DIR/cat_task.py /usr/local/sbin/cattask
ln -sf $DIR/ls_tasks.py /usr/local/sbin/lstasks
