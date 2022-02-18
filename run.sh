#!/bin/bash

function run() {
  docker-compose run --rm bot $1
}
run ./duco_report.py >> ./logs.log
run ./xmr_mine_report.py >> ./logs.log
run ./xmr_nano_report.py >> ./logs.log
