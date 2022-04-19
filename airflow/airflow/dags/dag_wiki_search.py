import logging
import os
import configparser
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from helper.db_management import DataManagement
from helper.sql_wiki import SqlQueries


logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("Punk Beer DAG")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))

config = configparser.ConfigParser()
config.read('dags/db.cfg')
##############################################################################
LOG.info("Initiate Dag")
#############################################################################
limit =20
defaultdb = "host={} dbname={} user={} password={} port={}".format(*config['db'].values())

newdb = "host={} dbname={} user={} password={} port={}".format(*config['freenowdb'].values())

client_db = DataManagement(defaultdb, newdb)


default_args = {
'owner'                 : 'freenow-data-platform-team',
'depend_on_past'        : False,
'email_on_failure'      : False,
'email_on_retry'        : False,
'retries'               : 2,
'retry_delay'           : timedelta(minutes=5),
'catchup'               : False
}

with DAG('dag-wiki-api',
          default_args=default_args,
          description='Consume wikipedia api and crawl around articles',
#         schedule_interval='30 12 * * 1-5',
          start_date = days_ago(1),
)  as dag:
   start_operator       = DummyOperator(task_id='Begin_execution',  dag=dag)

##############################################################################
LOG.info("Running the docker package")
##############################################################################

##############################################################################
LOG.info("Create db and table if not exists the data")
##############################################################################



create_db_table = PythonOperator(
            task_id='create_db_table',
            python_callable=client_db.main

)


run_docker_package   = DockerOperator(
                            task_id                 = 'run_docker_package',
                            image                   = 'smart-wiki:v1.0.2',
                            api_version             = 'auto',
                            auto_remove             = True,
                            command                 = f"smart wiki taxi --limit {limit}",
                            docker_url              = "tcp://docker-proxy:2375",
                            network_mode            = "bridge"
                            )

################################################################################
LOG.info("Running Data Quality")
################################################################################

#   run_quality_check   =   DataQualityOperator()

##############################################################################
LOG.info("Preparing the reports")
##############################################################################


make_report = PostgresOperator(
                    task_id='make_report',
                    postres_conn_id='postgres_default_id',
                    sql=SqlQueries.word_occurence.format("reports")
                    )



end_operator        = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> create_db_table >> run_docker_package >> make_report >> end_operator



LOG.info("Punk Beer Report Completed")
