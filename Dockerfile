FROM mitmproxy/mitmproxy:latest
USER root
RUN mkdir -p /home/mitmproxy && \
    chown mitmproxy:staff /home/mitmproxy

RUN mkdir -p /home/mitmproxy/prompt && \
    chown mitmproxy:staff /home/mitmproxy/prompt

RUN mkdir -p /home/mitmproxy/completion && \
    chown mitmproxy:staff /home/mitmproxy/completion

ADD ./mitmproxy_addon.py /home/mitmproxy/mitmproxy_addon.py
RUN chmod +x /home/mitmproxy/mitmproxy_addon.py

RUN usermod -u 1000 mitmproxy
RUN usermod -G staff mitmproxy

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install Flask prospector crosshair-tool flask-sqlalchemy sqlalchemy && \
    rm -rf /var/lib/apt/lists/*
# USER mitmproxy
EXPOSE 8082

ENV FLASK_APP=/home/mitmproxy/app.py
ENV BASE_DIR=/home/mitmproxy

# Add your Flask app
ADD ./app.py /home/mitmproxy/app.py
RUN chmod +x /home/mitmproxy/app.py && \
    chown -R mitmproxy:staff /home/mitmproxy/app.py


ADD ./start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]