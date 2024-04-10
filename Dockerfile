FROM python:3.11.7 AS app

WORKDIR /usr/src/app
EXPOSE 8000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
ENV FLASK_DEBUG=false
ENV PYTHONUNBUFFERED="true"

COPY .prospector.yaml .prospector.yaml

CMD ["gunicorn", "-c", "python:config.gunicorn", "src.entrypoint-flask:app"]
