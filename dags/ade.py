
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.mysql_to_s3 import MySQLToS3Operator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.providers.amazon.aws.operators.s3_delete_objects import S3DeleteObjectsOperator
from airflow.models import Variable

from datetime import datetime
from datetime import timedelta

import requests
import logging
import psycopg2
import json


dag = DAG(
    dag_id = 'MySQL_to_Redshift_clean',
    start_date = datetime(2021,11,27), # 날짜가 미래인 경우 실행이 안됨
    schedule_interval = '0 9 * * *',  # 적당히 조절
    max_active_runs = 1,
    catchup = False,
    default_args = {
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
    }
)

schema = "beam8686"
table = "nps"
s3_bucket = "grepp-data-engineering"
s3_key = schema + "-" + table

# s3_key가 존재하지 않으면 에러를 냄!
s3_folder_cleanup = S3DeleteObjectsOperator(
    task_id = 's3_folder_cleanup',
    bucket = s3_bucket,
    keys = s3_key,
    aws_conn_id = "aws_conn_id",
    dag = dag
)

s3_folder_cleanup
