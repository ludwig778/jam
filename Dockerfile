FROM python:3.7-slim-buster

RUN apt update && \
    apt install -y make && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN python3 -m pip install -r /tmp/requirements.txt

WORKDIR /home/jam
COPY . /home/jam

ENTRYPOINT ["make"]
CMD ["test"]
