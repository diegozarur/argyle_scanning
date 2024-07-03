FROM python:3.11-slim

WORKDIR /data

COPY . /data

# update pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_ENV=${FLASK_ENV}

EXPOSE ${FLASK_PORT}

# Default command
CMD ["gunicorn", "--config", "gunicorn_config.py", "run:flask_app"]
#ENTRYPOINT ["sh", "-c", "flask run --host=0.0.0.0 --port=${FLASK_PORT}"]
#CMD flask run -h 0.0.0.0 -p ${FLASK_PORT}