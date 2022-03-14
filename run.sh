#!/bin/bash

function run() {
  docker-compose run --rm bot $1
}
run ./duco_report.py
run ./xmr_mine_report.py
run ./xmr_nano_report.py
