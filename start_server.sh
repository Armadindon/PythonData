#!/bin/sh
gunicorn main:app -c gunicorn_conf.py
