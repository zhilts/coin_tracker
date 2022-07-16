#!/usr/bin/env bash

HOST=coin.sz.aws
APP_PATH=/usr/coin/

ssh $HOST "cd ${APP_PATH} && docker-compose down && rm -rf ./*"
scp ./* $HOST:${APP_PATH}
ssh $HOST "cd ${APP_PATH} && docker-compose build && docker-compose up -d"
