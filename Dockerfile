FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get -y upgrade && apt-get -y install libmariadb-dev-compat

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt                                                                            

EXPOSE 5001

ENTRYPOINT  ["python3"]

CMD ["app.py"]