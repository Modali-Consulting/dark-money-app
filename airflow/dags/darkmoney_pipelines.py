from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    "darkmoney_pipelines",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    run_resources = BashOperator(
        task_id="run_demo_resources",
        bash_command="python /opt/airflow/backend/manage.py run_pipeline --source=demo_resources",
    )

    run_finance = BashOperator(
        task_id="run_demo_finance",
        bash_command="python /opt/airflow/backend/manage.py run_pipeline --source=demo_finance",
    )

    publish_serving = BashOperator(
        task_id="publish_serving",
        bash_command="python /opt/airflow/backend/manage.py publish_serving --source=demo_resources",
    )

    run_resources >> run_finance >> publish_serving
