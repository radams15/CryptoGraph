#!/bin/bash

podman run -v $PWD:/graph:z -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/dri:/dev/dri -e DISPLAY=$DISPLAY -it --rm graph bash -c "cd /graph ; python3 main.py"
