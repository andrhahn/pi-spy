#! /bin/bash

raspivid -n -vf -hf -t 0 -w 640 -h 480 -fps 25 -b 0 -o - | ffmpeg -i - -vcodec copy -an -f flv rtmp://10.200.105.198/live/my-stream

# rotate 90 degrees (for pi zero)
raspivid -n -vf -hf -rot 90 -t 0 -w 640 -h 480 -fps 25 -b 0 -o - | ffmpeg -i - -vcodec copy -an -f flv rtmp://10.200.105.198/live/my-stream
