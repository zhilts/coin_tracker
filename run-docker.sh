#!/bin/bash

# Add to crontab
# 0 0 * * * cd /usr/coin && ./run-docker.sh >> /var/log/coin.log 2>&1

docker compose run --rm bot main.py