import logging
from sys import stdout

from innowise_application_task.celery import app

logger = logging.getLogger()
# enabling console output for celery workers
logger.addHandler(logging.StreamHandler(stdout))


@app.task
def test_print() -> None:
    print('а я не живая!')
    logger.info('а я живая!')
