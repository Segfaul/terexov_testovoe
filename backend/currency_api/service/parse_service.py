import json
from typing import List
from datetime import datetime, timedelta

import aiohttp
import xmltodict

from backend.currency_api.util import get_or_create
from backend.currency_api.model import CurrencyGroup, Currency, CurrencyRate
from backend.currency_api.service.db_service import TaskAsyncSessionFactory
from backend.currency_api.config import PROXY, HEADERS


async def get_response(link: str) -> list | None:
    '''
    Function returns list object from provided link

    :param link : any http/https link
    :type link : str
    :returns : raw html object
    :rtype : html.HtmlElement | None
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=link,
            proxy=PROXY,
            headers={'user-agent': HEADERS['user_agents'][1]} if HEADERS else {}
        ) as response:
            if response.status != 200:
                return None
            content = None
            if response.content_type == 'application/xml':
                decoded_response = await response.text()
                content = json.loads(json.dumps(xmltodict.parse(decoded_response)))
            if response.content_type == 'application/json':
                content = await response.json()
            return content


async def populate_db_from_cbr():
    '''
    Function stores data from cbr into database
    '''
    with open('backend/currency_api/config/data.json', 'r', encoding='utf-8') as record_file:
        data = json.load(record_file)

    async with TaskAsyncSessionFactory() as session:
        rate_dt = datetime.strptime(data['ValCurs']['@Date'], "%d.%m.%Y").date()
        currency_group = await get_or_create(
            session, CurrencyGroup, name=data['ValCurs']['@name']
        )
        currency_rates: List[CurrencyRate] = []
        existing_currency_rates: List[CurrencyRate] = []
        for row in data['ValCurs']['Valute']:
            currency_instance = await get_or_create(
                session, Currency,
                defaults={
                    "currency_group_id": currency_group.id,
                    "name": row['Name']
                },
                num_code=int(row['NumCode']),
                char_code=row['CharCode']
            )
            related_currency_rates: List[CurrencyRate] = [
                rate async for rate in CurrencyRate.read_all(
                    session, '_modified_at', currency_id=currency_instance.id, limit=1
                )
            ]
            value = float(row['Value'].replace(',', '.'))
            vunit_rate = float(row['VunitRate'].replace(',', '.'))
            nominal = int(row['Nominal'])

            # Check if any currency_rate exist and was modified less than in 1 day
            if len(related_currency_rates) > 0 and \
                    (
                        rate_dt -
                        (related_currency_rates[0].modified_at + timedelta(hours=3)).date()
                    ).days == 0:
                current_currency_rate = related_currency_rates[0]
                if current_currency_rate.vunit_rate != vunit_rate:
                    current_currency_rate.vunit_rate = vunit_rate
                    current_currency_rate.value = value
                    current_currency_rate.nominal = nominal
                    existing_currency_rates.append(current_currency_rate.__dict__)
            else:
                currency_rates.append(
                    CurrencyRate(
                        currency_id=currency_instance.id,
                        nominal=nominal,
                        value=value,
                        vunit_rate=vunit_rate
                    ).__dict__
                )

        if currency_rates:
            await session.execute(
                CurrencyRate.__table__.insert(),
                currency_rates
            )
            await session.commit()
        if existing_currency_rates:
            for rate in existing_currency_rates:
                await session.execute(
                    CurrencyRate.__table__.update()
                    .where(CurrencyRate.id == rate['id'])
                    .values(
                        vunit_rate=rate['vunit_rate'],
                        value=rate['value'],
                        nominal=rate['nominal']
                    )
                )
                await session.commit()


async def get_data_from_cbr():
    '''
    Function collects data from cbr and save in data.json file
    '''
    rbc_link = 'https://cbr.ru/scripts/XML_daily.asp'
    val_curs = await get_response(rbc_link)

    if val_curs:
        with open('backend/currency_api/config/data.json', 'w', encoding='utf-8') as record_file:
            json.dump(val_curs, record_file, indent=4)
