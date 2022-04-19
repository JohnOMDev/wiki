FROM puckel/docker-airflow:1.10.9

COPY airflow/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt



# The dockerfile pull the airflow image puckel, build on it and finally use it in the docker-compose file
