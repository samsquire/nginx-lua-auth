#!/usr/bin/env bash
source venv/bin/activate
export SERVER_ARGS="--nothing nothing";
sudo -E $(which gunicorn) -w 1 -k gevent server:app --bind 127.0.0.1:5000 &

wait

