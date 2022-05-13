import datetime
import unittest

import pendulum
from airflow import DAG
from airflow.models import DagRun
from airflow.models import TaskInstance as TI
from airflow.models import XCom
from airflow.models.baseoperator import BaseOperator
from airflow.models.taskinstance import TaskInstance
from airflow.utils.session import create_session
from airflow.utils.state import DagRunState
from airflow.utils.types import DagRunType

DATA_INTERVAL_START = pendulum.datetime(2022, 1, 1)
DATA_INTERVAL_END = DATA_INTERVAL_START + datetime.timedelta(days=1)
DAG_ID = "test_dag"
TASK_ID = "test_task"


class OperatorTestCase(unittest.TestCase):
    """Base class for testing operators that require context."""

    # Operator to be tested is specified in the Operator class variable
    # NOTE: While convenient, could this be confusing?
    Operator = BaseOperator

    def setUp(self):
        """Initilize DAG to add operators to."""
        super().setUp()
        self.dag = DAG(
            DAG_ID,
            default_args={"owner": "airflow", "start_date": DATA_INTERVAL_START},
        )

    def tearDown(self):
        """Prevent UNIQUE constraint errors between tests."""
        super().tearDown()
        with create_session() as session:
            session.query(DagRun).delete()
            session.query(TI).delete()
            session.query(XCom).delete()

    def get_ti(self, **kwargs) -> TaskInstance:
        """Get task instance for operator using operator's arguments."""
        self.Operator(dag=self.dag, task_id=TASK_ID, **kwargs)
        dagrun = self.dag.create_dagrun(
            state=DagRunState.RUNNING,
            execution_date=DATA_INTERVAL_START,
            data_interval=(DATA_INTERVAL_START, DATA_INTERVAL_END),
            start_date=DATA_INTERVAL_END,
            run_type=DagRunType.MANUAL,
        )
        ti = dagrun.get_task_instance(task_id=TASK_ID)
        ti.task = self.dag.get_task(task_id=TASK_ID)
        return ti
