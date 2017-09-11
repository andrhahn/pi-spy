#!/bin/bash

ps -ef | grep live_stream_start | grep -v grep | awk '{print $2}' | xargs kill
