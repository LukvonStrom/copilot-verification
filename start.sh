#!/bin/bash

mitmdump --set confdir=~/.mitmproxy -s mitmproxy_addon.py -p 8080 --set validate_inbound_headers=false --no-http2
