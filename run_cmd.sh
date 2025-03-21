#!/bin/bash

ssh localhost -p222
cd ~/easy-morning/Easy-Morning-bot
source venv/bin/activate
python3 manage.py $@
