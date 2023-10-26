from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import logging

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
    'depends_on_past': False,
}

# Instantiate a DAG
dag = DAG(
    'data_pipeline',
    default_args=default_args,
    description='A data pipeline example',
    schedule_interval=timedelta(days=1),  # Set the DAG to run daily
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=None,
    tags=['production'],
)

def extract_data_from_source():
    try:
        # Simulating data extraction
        data = "Data extracted from source"
        logging.info(data)
        return data
    except Exception as e:
        logging.error(f"Error extracting data from source: {e}")
        raise

def perform_aggregations(task_instance):
    try:
        extracted_data = task_instance.xcom_pull(task_ids='extract_data_from_source')
        # Simulating data transformation
        transformed_data = f"Transformed: {extracted_data}"
        logging.info(transformed_data)
        return transformed_data
    except Exception as e:
        logging.error(f"Error performing aggregations: {e}")
        raise

def lookup_values(task_instance):
    try:
        transformed_data = task_instance.xcom_pull(task_ids='perform_aggregations')
        # Simulating data lookup
        looked_up_data = f"Looked up: {transformed_data}"
        logging.info(looked_up_data)
        return looked_up_data
    except Exception as e:
        logging.error(f"Error looking up values: {e}")
        raise

def load_data_to_destination(task_instance):
    try:
        looked_up_data = task_instance.xcom_pull(task_ids='lookup_values')
        # Simulating data loading
        load_message = f"Loaded to destination: {looked_up_data}"
        logging.info(load_message)
    except Exception as e:
        logging.error(f"Error loading data to destination: {e}")
        raise

# Define tasks
extract_data_task = PythonOperator(
    task_id='extract_data_from_source',
    python_callable=extract_data_from_source,
    dag=dag,
)

perform_aggregations_task = PythonOperator(
    task_id='perform_aggregations',
    python_callable=perform_aggregations,
    provide_context=True,
    dag=dag,
)

lookup_values_task = PythonOperator(
    task_id='lookup_values',
    python_callable=lookup_values,
    provide_context=True,
    dag=dag,
)

load_data_to_destination_task = PythonOperator(
    task_id='load_data_to_destination',
    python_callable=load_data_to_destination,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
extract_data_task >> perform_aggregations_task >> lookup_values_task >> load_data_to_destination_task
