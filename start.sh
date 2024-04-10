#!/bin/bash

cd /home/mitmproxy/
ls .
mitmdump --set confdir=~/.mitmproxy -s /home/mitmproxy/src/entrypoint-mitmproxy.py -p 8080 --set validate_inbound_headers=false --no-http2 