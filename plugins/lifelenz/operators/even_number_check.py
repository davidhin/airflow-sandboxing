from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class EvenNumberCheckOperator(BaseOperator):
    @apply_defaults
    def __init__(self, my_operator_param, *args, **kwargs):
        self.operator_param = my_operator_param
        super(EvenNumberCheckOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        if self.operator_param % 2 == 0:
            return True
        else:
            return False

