#!/bin/bash

mjpg_streamer -i "input_raspicam.so" -o "output_http.so -p 8099 -w /var/www/camera" & >/dev/null 2>&1
