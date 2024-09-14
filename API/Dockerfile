FROM python:3.10-slim

WORKDIR /code

ENV HOST=0.0.0.0

COPY ./google-chrome-stable_current_amd64.deb /code/google-chrome-stable_current_amd64.deb
COPY ./chrome-linux64.zip /code/chrome-linux64.zip

RUN apt-get update -qq -y
RUN apt-get install -y unzip

RUN unzip chrome-linux64.zip
RUN rm chrome-linux64.zip
RUN mv chrome-linux64 /usr/bin/

RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8080

COPY ./app /code/app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
