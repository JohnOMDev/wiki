# wiki
Wikipedia API can be used to access wikipedia articles based on keyword provided.

## Project Structure
│   README.md
└───smart
│   └───src
│         └───insert_query.py
│         └───wikimedia.py
│   └───app.py
│   └───config.py
│   └───db.cfg
│   └───requirements.txt
│
└───airflow
│    └───docker-compose.yml
│    └───Dockerfile
│    └───requirements.txt
│    └───env.list
│    └───airflow
│          └───Dags
│               └───db.cfg
│               └───dag_wiki_search
│               └───helper
│                     └───db_management.py
│                     └───sql_wiki.py
│          └───airflow.cfg
└───pg
│    └───docker-compose.yml
│    └─── .env
└───setup.py
│
└───Dockerfile


## Implementation
Clone the repository and follow the steps below.
### Create a virtual environment
  * python -m venv ....
  * source .../bin/activate
### Spin up Postgress DB with Docker
  * open a terminal type, `cd in to the pg directory` and type the command `docker compose up`.

### Build the wiki API docker image
  * Open another terminal and `cd in to the root directory of the project` and type the following command.
      * `docker build -t smart-wiki .`
      * `docker tag smart-wiki:latest smart-wiki:v1.0.4`.
  * You can test the wiki API application using the following commands.
      * `docker run --rm smart-wiki smart wiki taxi --limit 10 --m True`.

  * Input/Output: Once installed we should be able to run `smart --help` to get a help message with the subcommands.
  * WHERE:
      a) `smart-wiki` is the docker image.
      b) `smart` is the package.
      c) `wiki` is the module.
      d) `taxi` is the keyword (can be anything).
      e) `--limit 10` is the length of the result.
      f) `--m True` is optional and if included, it will only output the result in the terminal and not save it in db.

### Build a workflow (DAG) with Apache Airflow
  * Open another terminal and `cd in to the airflow directory` and type the following command.

      * `docker compose  up -d --build`

  * You can access your airflow through the url `http://localhost:8080/` and the worker through the url `http://localhost:5555/`.

  * Airflow use the official https://github.com/puckel/docker-airflow image as the base image
####  HAPPY CODING :)
