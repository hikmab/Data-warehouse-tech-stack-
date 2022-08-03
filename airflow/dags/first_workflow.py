# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 01:54:51 2021

@author: viswa
"""

from airflow import DAG
from datetime import datetime,timedelta  
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.email_operator import EmailOperator


#from pre_processing import pre_process
#from pre_process import process_data

default_args = {"owner":"airflow","start_date":datetime(2022, 8, 1)}
with DAG(dag_id="workflow",default_args=default_args,schedule_interval='@daily') as dag:
   
    check_file = BashOperator(
        schedule_interval=None,
        task_id="check_file",
        bash_command="shasum ~/dags/data.csv",
        retries = 2,
        retry_delay=timedelta(seconds=15))
    
   # pre_process = PythonOperator(
    #    task_id = "pre_process",
     #   python_callable = pre_process
      #  )
    
    # agg = PythonOperator(
    #     task_id = "agg",
    #     python_callable = process_data
    #     )
    
    create_table = MySqlOperator(
        task_id = "create_table",
        mysql_conn_id = "mysql_db1",
        sql="CREATE table if NOT EXISTS trafic (track_id varchar(100) NULL,type varchar(100) NULL,traveled_d varchar(100) NULL,avg_speed varchar(100) NULL,lat varchar(100) NULL,lon varchar(100) NULL,speed varchar(100) NULL,lon_acc varchar(100) NULL,lat_acc varchar(100) NULL,time varchar(100) NULL)"
        )

    insert = MySqlOperator(
        task_id='insert_db', 
        mysql_conn_id="mysql_db1", 
        #sql="LOAD DATA LOCAL INFILE '/usr/local/airflow/dags/data.csv' INTO TABLE trafic FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' IGNORE 1 ROWS;") 
 #sql="LOAD DATA LOCAL INFILE '/usr/local/airflow/dags/data.csv' INTO TABLE trafic FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;")
        sql='load.sql')
    # email = EmailOperator(task_id='send_email',
    #     to='hikmaburhan01@gmail.com',
    #     subject='Daily report generated',
    #     html_content=""" <h1>Congratulations! Your store reports are ready.</h1> """,
    #     )
    check_file >> create_table >> insert 