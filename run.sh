#!/bin/bash

. ./venv/bin/activate
./duco_report.py >> ./logs.log
./xmr_mine_report.py >> ./logs.log
./xmr_nano_report.py >> ./logs.log
deactivate