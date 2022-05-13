from airflow.utils.state import TaskInstanceState
from lifelenz.operators.even_number_check import EvenNumberCheckOperator

from base import OperatorTestCase


class TestEvenNumberCheckOperator(OperatorTestCase):
    Operator = EvenNumberCheckOperator

    def test_even(self):
        """Tests that the EvenNumberCheckOperator returns True for 10."""
        ti = self.get_ti(my_operator_param=10)
        ti.run(ignore_ti_state=True)
        assert ti.state == TaskInstanceState.SUCCESS
        result = ti.task.execute(ti.get_template_context())
        assert result is True

    def test_odd(self):
        """Tests that the EvenNumberCheckOperator returns False for 11."""
        ti = self.get_ti(my_operator_param=11)
        result = ti.task.execute(ti.get_template_context())
        assert result is False
