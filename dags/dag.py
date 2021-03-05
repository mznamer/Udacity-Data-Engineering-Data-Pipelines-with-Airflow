from airflow import DAG
from datetime import datetime, timedelta
import os
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadOperator, DataQualityOperator)
from helpers import SqlInsertQueries


s3_bucket = "s3://udacity-dend"

default_args = {
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime.datetime.utcnow(),
    'catchup': False
}

dag = DAG(
    'udacity-airflow_project',
    default_args=default_args,
    description='DAG for Udacity Project Airflow',
)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    redshift_conn_id="redshift_connection",
    aws_credentials_id="aws_credentials",
    destination_table="staging_events",
    s3_bucket=s3_bucket,
    s3_key="log_data/{execution_date.year}/{execution_date.month}/*.json"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    destination_table="staging_songs",
    redshift_conn_id="redshift_connection",
    aws_credentials_id="aws_credentials",
    s3_bucket=s3_bucket,
    s3_key="song_data/*/*/*.json"
)

load_songplays_table = LoadOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id="redshift_connection",
    aws_credentials_id="aws_credentials",
    destination_table="songplays",
    self.is_clear_table = False
)

load_user_dimension_table = LoadOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id="redshift_connection",
    aws_credentials_id="aws_credentials",
    destination_table="users",
    self.is_clear_table = True
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id="redshift_connection",
    aws_credentials_id="aws_credentials",
    destination_table="songs",
    self.is_clear_table = True
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id="redshift_connection",
    aws_credentials_id="aws_credentials",
    destination_table="artists",
    self.is_clear_table = True
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id="redshift_connection",
    aws_credentials_id="aws_credentials",
    destination_table="time",
    self.is_clear_table = True
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> stage_events_to_redshift
start_operator >> stage_songs_to_redshift

stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table

load_songplays_table >> load_user_dimension_table
load_songplays_table >> load_song_dimension_table
load_songplays_table >> load_artist_dimension_table
load_songplays_table >> load_time_dimension_table

load_user_dimension_table >> run_quality_checks
load_song_dimension_table >> run_quality_checks
load_artist_dimension_table >> run_quality_checks
load_time_dimension_table >> run_quality_checks

run_quality_checks >> end_operator