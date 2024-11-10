#!/bin/bash
set -a
source $HOME/env/$HOSTNAME-pokyfriends.env;
set +a
echo "CRON START: ";
date;
echo "------------------------------------------------------------";
$HOME/projects/pokyfriends/venv/bin/python3 $HOME/projects/pokyfriends/manage.py remove-like-records
echo "CRON END: ";
date;
echo "============================================================";
