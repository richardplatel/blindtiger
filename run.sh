#!/bin/bash
cd ~pi/Development/BlindTiger
if ./wait_for_network.sh ; then
  . env/bin/activate
  rtmbot
fi

