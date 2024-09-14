FROM python:3.10-slim

WORKDIR /code

ENV HOST=0.0.0.0

# Copy Chrome files first
COPY ./google-chrome-stable_current_amd64.deb /code/google-chrome-stable_current_amd64.deb
COPY ./chrome-linux64.zip /code/chrome-linux64.zip

# Install dependencies and clean up in one layer
RUN apt-get update -qq -y && \
    apt-get install -y --no-install-recommends unzip && \
    unzip chrome-linux64.zip && \
    mv chrome-linux64 /usr/bin/ && \
    apt-get install -y --no-install-recommends ./google-chrome-stable_current_amd64.deb && \
    rm -rf chrome-linux64.zip google-chrome-stable_current_amd64.deb /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code
COPY ./app /code/app/

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
# uvicorn app.main:app --host 0.0.0.0 --port 8080