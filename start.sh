#!/bin/bash

# Function to start Flask app
start_flask() {
    flask run --host=0.0.0.0 --port=8082 &
    FLASK_PID=$!
}

# Function to start mitmdump
start_mitmdump() {
    mitmdump --set confdir=/home/mitmproxy/.mitmproxy -s /home/mitmproxy/mitmproxy_addon.py -p 8080 &
    MITMDUMP_PID=$!
}

cleanup() {
    echo "Signal received, shutting down gracefully..."
    # Kill Flask and mitmdump if they are running
    [[ -n $FLASK_PID ]] && kill $FLASK_PID
    [[ -n $MITMDUMP_PID ]] && kill $MITMDUMP_PID
    # Wait for Flask and mitmdump to terminate
    wait $FLASK_PID
    wait $MITMDUMP_PID
    exit 0
}

# Trap signals
trap cleanup SIGTERM SIGINT

# Start Flask and mitmdump
start_flask
start_mitmdump

# Wait for Flask and mitmdump to finish
wait $FLASK_PID
wait $MITMDUMP_PID
