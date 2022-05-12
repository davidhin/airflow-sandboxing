import datetime
import unittest

import pendulum
from airflow import DAG
from airflow.utils.state import DagRunState, TaskInstanceState
from airflow.utils.types import DagRunType

from lifelenz.operators.even_number_check import EvenNumberCheckOperator

DATA_INTERVAL_START = pendulum.now()
DATA_INTERVAL_END = DATA_INTERVAL_START + datetime.timedelta(days=1)
TEST_DAG_ID = "my_custom_operator"
TEST_TASK_ID = "my_custom_task"


class TestEvenNumberCheckOperator(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.dag = DAG(
            TEST_DAG_ID,
            default_args={"owner": "airflow", "start_date": DATA_INTERVAL_START},
        )
        self.even = 10
        self.odd = 11
        EvenNumberCheckOperator(
            task_id=TEST_TASK_ID, my_operator_param=self.even, dag=self.dag
        )

    def test_even(self):
        """Tests that the EvenNumberCheckOperator returns True for 10."""
        dagrun = self.dag.create_dagrun(
            state=DagRunState.RUNNING,
            execution_date=DATA_INTERVAL_START,
            data_interval=(DATA_INTERVAL_START, DATA_INTERVAL_END),
            start_date=DATA_INTERVAL_END,
            run_type=DagRunType.MANUAL,
        )
        print(dagrun)

        ti = dagrun.get_task_instance(task_id=TEST_TASK_ID)
        ti.task = self.dag.get_task(task_id=TEST_TASK_ID)
        ti.run(ignore_ti_state=True)
        assert ti.state == TaskInstanceState.SUCCESS
        result = ti.task.execute(ti.get_template_context())
        assert result is True
