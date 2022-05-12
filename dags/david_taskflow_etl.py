"""DAG using taskflow api for ETL example process."""
import json

import pendulum

from airflow.decorators import dag, task

from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from lifelenz.operators.hello_operator import HelloOperator
from lifelenz.operators.even_number_check import EvenNumberCheckOperator


@dag(
    schedule_interval="0 * * * *",
    start_date=pendulum.datetime(2022, 1, 1, tz="Australia/Adelaide"),
    catchup=False,
    tags=["example"],
)
def david_taskflow_etl():
    """# Example of a taskflow DAG."""

    @task()
    def extract():
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        order_data_dict = json.loads(data_string)
        return order_data_dict

    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        total_order_value = 0
        for value in order_data_dict.values():
            total_order_value += value
        return {"total_order_value": total_order_value}

    @task()
    def load(total_order_value: float):
        print(f"HI ITS DAVID Total order value is: {total_order_value:.2f}")

    @task()
    def select_data_from_postgres():
        postgres = PostgresHook(postgres_conn_id="airflow_sandbox_aws_postgres")
        conn = postgres.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM defaulttable;")
        print(cursor.fetchall())

    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])
    postgres_select_task = PostgresOperator(
        task_id="postgres_thingo",
        sql="SELECT * FROM defaulttable",
        postgres_conn_id="airflow_sandbox_aws_postgres",
    )
    order_data >> postgres_select_task
    select_data_from_postgres()
    HelloOperator(
        task_id="task_id_1",
        name="{{ task_instance.task_id }}",
        ts="{{ ts }}",
    )
    EvenNumberCheckOperator(
        my_operator_param=10,
        task_id="even_num_ck_tas",
    )


david_taskflow_etl = david_taskflow_etl()
