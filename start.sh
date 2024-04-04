#!/bin/bash

cd /home/mitmproxy/
ls .
mitmdump --set confdir=~/.mitmproxy -s /home/mitmproxy/mitmproxy_addon.py -p 8080 --set validate_inbound_headers=false --no-http2 


