#! /bin/bash

raspivid -n -vf -hf -t 0 -w 640 -h 480 -fps 25 -b 0 -o - | ffmpeg -i - -vcodec copy -an -f flv rtmp://localhost/live/my-stream
