#!/usr/bin/env bash
pip install --upgrade pip
pip uninstall -y python-telegram-bot
pip install python-telegram-bot==20.7
pip install -r requirements.txt
