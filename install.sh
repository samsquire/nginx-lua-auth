#!/usr/bin/env bash

ln -s $(pwd)/nginx.conf /etc/nginx/nginx.conf
ln -s $(pwd)/nginx.service /etc/systemd/system/nginx.service
ln -s $(pwd)/session_validator.lua /etc/nginx/session_validator.lua
sudo mkdir /etc/nginx/sessions

virtualenv venv


