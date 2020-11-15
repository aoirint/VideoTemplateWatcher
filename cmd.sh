#!/bin/sh

docker run --rm -it \
  -u "$(id -u):$(id -g)" \
  -e DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v "${PWD}/work_sample:/work" \
  aoirint/video-template-watcher "$@"
