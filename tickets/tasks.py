import datetime
import logging
from sys import stdout

from innowise_application_task.celery import app

logger = logging.getLogger()
# enabling console output for celery workers
logger.addHandler(logging.StreamHandler(stdout))


@app.task
def test_print() -> None:
    """Test task for checking whether celery actually works."""
    print('а я не живая!')
    logger.info('а я живая!')


@app.task
def close_old_tickets() -> None:
    """Task that sets status of all tickets older than (for example) 90 days as 'Closed'."""
    from tickets.models import Ticket

    # calculating datetime that's 90 days ago away from the moment of executing this task
    DEFAULT_CLOSURE_DAY_AMOUNT = 90
    start_time = datetime.datetime.now() - datetime.timedelta(DEFAULT_CLOSURE_DAY_AMOUNT)
    old_tickets = Ticket.objects.filter(creation_time__lt=start_time, force_closed=False)

    for ticket in old_tickets:
        ticket.status = 'Closed'
        ticket.force_closed = True
    logging.info(f'{len(old_tickets)} tickets edited!')

    Ticket.objects.bulk_update(objs=old_tickets, fields=('status', 'force_closed',))
    logging.info(f'{len(old_tickets)} tickets updated!')
