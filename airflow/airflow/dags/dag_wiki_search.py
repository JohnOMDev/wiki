import logging
import os
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.dates import days_ago
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.configuration import conf


logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("Punk Beer DAG")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))


##############################################################################
    LOG.info("Initiate Dag")
#############################################################################

default_args = {
'owner'                 : 'smava-data-platform-team',
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

run_docker_package   = DockerOperator(
                            task_id                 = 'run_docker_package',
                            image                   = 'smart-wiki:v1.0.0',
                            api_version             = 'auto',
                            auto_remove             = True,
                            command                 = f"smart wiki taxi --limit 10",
                            docker_url              = "tcp://docker-proxy:2375",
                            network_mode            = "bridge",
                            volumes                 = ["/data:/data"],
                            )

################################################################################
LOG.info("Running Data Quality")
################################################################################

#   run_quality_check   =   DataQualityOperator()

##############################################################################
LOG.info("Preparing the data")
##############################################################################

# make_report         = PythonOperator(
#                                task_id = "make_report",
#                                python_callable=preprocess_data
#            )



end_operator        = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> run_docker_package >> end_operator

# run_quality_check >> make_report >>


LOG.info("Punk Beer Report Completed")
