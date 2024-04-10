FROM python:3.12.2-slim-bookworm AS app

WORKDIR /usr/src/app
EXPOSE 8080

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
ENV FLASK_DEBUG=false
ENV PYTHONUNBUFFERED="true"
CMD ["gunicorn", "-c", "python:config.gunicorn", "src.entrypoint-flask:app"]
