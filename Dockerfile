FROM python:3.8

# initialize the working directory
WORKDIR /wiki_api

#install dependency
# COPY requirements.txt
# RUN pip install -r requirements.txt

#copy the punk api
COPY /wiki_api .

#run the application
RUN python setup.py install

# CMD["python", "main.py"]

RUN python setup.py install
