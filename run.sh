#!/bin/bash

if [ -z "$LISTEN_IP" ]; then
  export LISTEN_IP="0.0.0.0"
fi

if [ -z "$LISTEN_PORT" ]; then
  export LISTEN_PORT=8000
fi

gunicorn --bind $LISTEN_IP:$LISTEN_PORT pyxie:pyxie
