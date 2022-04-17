FROM python:3.8

# initialize the working directory
WORKDIR /freenow

# copy the wiki api
COPY wiki_api ./wiki_api

COPY setup.py ./


COPY README.md ./


# run the application and build the packege

RUN python setup.py install
