#! /bin/bash

raspivid -n -vf -hf -t 0 -w 640 -h 480 -fps 25 -b 0 -o - | ffmpeg -i - -vcodec copy -an -f flv rtmp://34.197.186.122/live/my-stream
