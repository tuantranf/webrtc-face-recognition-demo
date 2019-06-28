#!/bin/bash
# ./generate-images.sh test.mov

FPS=5
video_file=$1

docker run --rm -ti -v ${PWD}:/work ampervue/ffmpeg ffmpeg -i /work/$video_file -vf fps=$FPS /work/${video_file%.*}/${video_file%.*}-$frame%04d.jpg