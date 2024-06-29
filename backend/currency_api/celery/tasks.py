from asgiref.sync import async_to_sync

from celery import shared_task

from backend.currency_api.service.parse_service import populate_db_from_cbr, get_data_from_cbr


@shared_task
def populate_db():
    '''
    Populate DB from CBR
    '''
    async_to_sync(populate_db_from_cbr)()


@shared_task
def parse_cbr():
    '''
    Parse CBR
    '''
    async_to_sync(get_data_from_cbr)()
