FROM python:3.8

# initialize the working directory
WORKDIR /freenow

# copy the wiki api
COPY smart ./smart

COPY setup.py ./


COPY README.md ./


# run the application and build the packege

RUN python setup.py install
