from datetime import timedelta
from airflow.models.baseoperator import BaseOperator

from airflow.triggers.temporal import TimeDeltaTrigger


class HelloOperator(BaseOperator):

    template_fields = ["name", "ts"]

    def __init__(self, name: str, ts: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.ts = ts

    def execute(self, context):
        message = f"Hello from {self.name}"
        print(message, self.ts)

        # Deferrable task
        self.defer(
            trigger=TimeDeltaTrigger(timedelta(seconds=3)),
            method_name="execute_complete",
            kwargs={"message": message},
        )
        return message

    def execute_complete(self, context, event=None, message=None):
        # We have no more work to do here. Mark as complete.
        print("Event Completed")
        print(message)
        return
