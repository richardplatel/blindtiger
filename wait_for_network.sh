#!/bin/bash

for run in {1..30};
do
  iad=$(ifconfig wlan0 | fgrep 'inet addr')
  if [ "xx${iad}" != "xx" ] ; then
    exit 0
  fi
  sleep 1
done

exit 4
