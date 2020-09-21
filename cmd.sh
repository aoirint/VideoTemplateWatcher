#!/bin/sh

docker run --rm -it \
  -e DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v "${PWD}/work_sample:/work" \
  aoirint/video-template-watcher "$@"
