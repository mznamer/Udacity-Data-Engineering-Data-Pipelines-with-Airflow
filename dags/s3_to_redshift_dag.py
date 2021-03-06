from airflow import DAG
from datetime import datetime, timedelta
import os
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, 
                            LoadOperator, 
                            DataQualityOperator, 
                            CreateRedshiftTablesOperator)
from helpers import SqlInsertQueries, SqlCreateQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

s3_bucket = "s3://udacity-dend"

default_args = {
    'owner': 'mznamer-udacity',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2021, 3, 5),
    'catchup': False
}

dag = DAG(
    'udacity-airflow_project',
    default_args=default_args,
    description='DAG for Udacity Project Airflow - ETL from S3 to Redshift',
    schedule_interval='0 * * * *'
)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_redshift_tables = CreateRedshiftTablesOperator(
    task_id='Create_redshift_tables',
    dag=dag,
    redshift_conn_id="redshift_connection",
    query_list=[v.strip() for k, v in SqlCreateQueries.__dict__.items() if k[:1] != '_']
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    redshift_conn_id="redshift_connection",
    aws_credentials_id="aws_credentials",
    destination_table="staging_events",
    s3_bucket=s3_bucket,
    s3_key="log_data",
    json_path=f"{s3_bucket}/log_json_path.json"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    redshift_conn_id="redshift_connection",
    aws_credentials_id="aws_credentials",
    destination_table="staging_songs",
    s3_bucket=s3_bucket,
    s3_key="song_data",
    json_path="auto"
)

load_songplays_table = LoadOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id="redshift_connection",
    destination_table="songplays",
    sql_query=SqlInsertQueries.songplay_table_insert,
    flag_clear_table = False
)

load_song_dimension_table = LoadOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id="redshift_connection",
    destination_table="songs",
    sql_query=SqlInsertQueries.song_table_insert,
    flag_clear_table = True
)

load_artist_dimension_table = LoadOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id="redshift_connection",
    destination_table="artists",
    sql_query=SqlInsertQueries.artist_table_insert,
    flag_clear_table = True
)

load_user_dimension_table = LoadOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id="redshift_connection",
    destination_table="users",
    sql_query=SqlInsertQueries.user_table_insert,
    flag_clear_table = True
)

load_time_dimension_table = LoadOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id="redshift_connection",
    destination_table="time",
    sql_query=SqlInsertQueries.time_table_insert,
    flag_clear_table = True
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> create_redshift_tables

create_redshift_tables >> stage_events_to_redshift
create_redshift_tables >> stage_songs_to_redshift

stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table

load_songplays_table >> load_song_dimension_table
load_songplays_table >> load_artist_dimension_table
load_songplays_table >> load_user_dimension_table
load_songplays_table >> load_time_dimension_table

load_song_dimension_table >> run_quality_checks
load_artist_dimension_table >> run_quality_checks
load_user_dimension_table >> run_quality_checks
load_time_dimension_table >> run_quality_checks

run_quality_checks >> end_operator