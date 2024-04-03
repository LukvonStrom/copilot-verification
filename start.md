docker run --rm -d \
-v ~/.mitmproxy:/home/mitmproxy/.mitmproxy \
-v $(pwd)/completion:/home/mitmproxy/completion \
-v $(pwd)/prompt:/home/mitmproxy/prompt \
-p 8080:8080 mitmproxy/mitmproxy


## LOL

docker build -t copilotproxy . && docker run --rm -v ~/.mitmproxy:/home/mitmproxy/.mitmproxy -v $(pwd)/completion:/home/mitmproxy/completion -v $(pwd)/prompt:/home/mitmproxy/prompt -p 8080:8080 copilotproxy:latest mitmdump --set confdir=/home/mitmproxy/.mitmproxy -s /home/mitmproxy/mitmproxy_addon.py -p 8080 & flask run --host=0.0.0.0 --port=8082



docker build -t copilotproxy . && docker run --rm -v ~/.mitmproxy:/home/mitmproxy/.mitmproxy -p 8080:8080 -p 8082:8082 copilotproxy:latest cd /home/mitmproxy && flask run --host=0.0.0.0 --port=8082 & mitmdump --set confdir=/home/mitmproxy/.mitmproxy -s /home/mitmproxy/mitmproxy_addon.py -p 8080

