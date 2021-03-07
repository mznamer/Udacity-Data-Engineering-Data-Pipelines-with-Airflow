# Project: Data Pipelines with Apache Airflow


**Apache Airflow**  is a platform to programmatically author, schedule and monitor workflows. An Airflow pipeline is just a Python script that happens to define an Airflow DAG object
#### Principles
* Dynamic: Airflow pipelines are configuration as code (Python), allowing for dynamic pipeline generation. This allows for writing code that instantiates pipelines dynamically.

* Extensible: Easily define your own operators, executors and extend the library so that it fits the level of abstraction that suits your environment.

* Elegant: Airflow pipelines are lean and explicit. Parameterizing your scripts is built into the core of Airflow using the powerful Jinja templating engine.

* Scalable: Airflow has a modular architecture and uses a message queue to orchestrate an arbitrary number of workers. Airflow is ready to scale to infinity.

[Apache Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html)



## Project Description

A music streaming company, **Sparkify** has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

Our goal is to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. Data quality plays a big part when analyses are executed on top the data warehouse, so we have to run tests against datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

### Project Datasets

* Song data: `s3://udacity-dend/song_data`
* Log data: `s3://udacity-dend/log_data`

#### 1. Song Dataset
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. 

The files are partitioned by the first three letters of each song's track ID. For example, here are file paths to two files in this dataset.

```
song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
```
###### *Example of file (TRAABJL12903CDCF1A.json):*
```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, 
"artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", 
"song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", 
"duration": 152.92036, "year": 0}
```

#### 2. Log Dataset
The second dataset is log files in JSON format generated an event simulator based on the songs in the dataset above. These simulate app activity logs from an imaginary music streaming app based on configuration settings.

The log files in the dataset are partitioned by year and month. For example, here are file paths to two files in this dataset.

```
     log_data/2018/11/2018-11-12-events.json
     log_data/2018/11/2018-11-13-events.json
```
###### *Example of file (2018-11-12-events.json):*

```
{"artist":"Slipknot", "auth":"LoggedIn", "firstName":"Aiden", "gender":"M",
"itemInSession":0,"lastName":"Ramirez", "length":192.57424,"level":"paid",
"location":"New York-Newark-Jersey City, NY-NJ-PA", "method":"PUT", 
"page":"NextSong", "registration":1540283578796.0,"sessionId":19,
"song":"Opium Of The People (Album Version)", "status":200, 
"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
"ts":1541639510796,"userId":"20"}
```

## Project requirements

#### Configuring the DAG

* The DAG does not have dependencies on past runs 
* On failure, the task are retried 3 times
* Retries happen every 5 minutes
* Catchup is turned off
* Do not email on retry

After the tasks dependencies are set, the graph view follows the flow shown in the image below:
![graph dependencies ](https://video.udacity-data.com/topher/2019/January/5c48ba31_example-dag/example-dag.png)

#### Operators
**CreateRedshiftTablesOperator** creates all tables for the project.

**StageToRedshiftOperator** loads JSON formatted files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided. The operator's parameters should specify where in S3 the file is loaded and what is the target table.

**LoadOperator**
SQL helper class runs data transformations. The operator takes as input a SQL statement, target database, and target table that will contain the results of the transformation.

**DataQualityOperator** runs checks for total records in fact and dimensional tables. If there is no records, the operator raises an exception and the task retries and fails eventually.


## Project structure

* `dags/s3_redshift_dag.py` - Directed Acyclic Graph with imports, main tasks and dependencies between tasks

* `plugins/helpers/sql_create_queries.py` - Contains SqlCreateQueries class with SQL create statements for all tables
* `plugins/helpers/sql_insert_queries.py` - Contains SqlInsertQueries class with SQL insert statements for all tables

* `plugins/operators/create_tables.py` - CreateRedshiftTablesOperator that creates Staging, Fact and Dimentional tables
* `plugins/operators/stage_redshift.py` - StageToRedshiftOperator copies data from S3 logs and songs buckets into Redshift staging tables
* `plugins/operators/load_data.py` - LoadOperator that runs loading data from Redshift staging tables into Fact table and Dimensional tables

* `plugins/operators/data_quality`.py - DataQualityOperator performs data quality check in Redshift Fact and Dimensional tables

* `README.md` - Current file, contains detailed information about the project.


## Data Schema

### Staging Tables

#### staging_songs

column name | type
------------- | -------------
num_songs | INTEGER
artist_id | VARCHAR 
artist_latitude | NUMERIC
artist_longitude | NUMERIC
artist_location | VARCHAR 
artist_name | VARCHAR 
song_id | VARCHAR 
title | VARCHAR 
duration | NUMERIC
year | INTEGER

#### staging_events

column name | type
------------- | -------------
artist | VARCHAR
auth | VARCHAR
firstName | VARCHAR
gender | CHAR(1)
itemInSession | INTEGER
lastName | VARCHAR
length | NUMERIC
level | VARCHAR
location | VARCHAR
method | VARCHAR
page | VARCHAR
registration | NUMERIC
sessionId | INTEGER
song | VARCHAR
status | INTEGER
ts | BIGINT
userAgent | VARCHAR
userId | INTEGER

### Fact Table

#### songplay - records in log data associated with song plays (records with page = "NextSong")

column name | type
------------- | -------------
playid| INTEGER
start_time | TIMESTAMP 
userid | INTEGER 
level | VARCHAR 
songid | VARCHAR 
artistid | VARCHAR 
sessionid | INTEGER 
location | VARCHAR 
user_agent | VARCHAR


### Dimension Tables

#### songs - songs in music database


column name | type
------------- | -------------
songid | VARCHAR
title | VARCHAR
artistid | VARCHAR
year | SMALLINT
duration | NUMERIC


#### artists - artists in music database

column name | type
------------- | -------------
artistid | VARCHAR
name| VARCHAR
location | VARCHAR
latitude | NUMERIC
longitude | NUMERIC

#### users - users in the app

column name | type
------------- | -------------
userid | INTEGER
first_name | VARCHAR
last_name | VARCHAR
gender | CHAR(1)
level | VARCHAR


#### time - records from songplays with specific time units

column name | type
------------- | -------------
start_time | TIMESTAMP
hour | INTEGER
day | INTEGER
week | INTEGER
month | INTEGER
year | INTEGER
weekday | INTEGER