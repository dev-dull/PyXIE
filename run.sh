#!/bin/bash

if [ -z "$LISTEN_IP" ]; then
  export LISTEN_IP="0.0.0.0"
fi

if [ -z "$LISTEN_PORT" ]; then
  export LISTEN_PORT=5000  # Set to 5000 to match Flask's default and avoid confusion in the docs
fi

gunicorn --bind $LISTEN_IP:$LISTEN_PORT pyxie:pyxie
