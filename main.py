from collections import namedtuple
from typing import Dict

from fastapi import FastAPI
from services import FlexJobCounter, IndeedCounter

api = FastAPI()


@api.get('/flexjobs/{query}')
async def flexjobs(query: str):
    counter = FlexJobCounter(searched_job=query)
    vacancies = await counter.count_vacancies()
    return {'job': query, 'items': vacancies, 'source': 'flexjobs'}


@api.get('/indeed/{query}')
async def indeed(query: str):
    counter = IndeedCounter(searched_job=query)
    vacancies = await counter.count_vacancies()
    return {'job': query, 'items': vacancies, 'source': 'indeed'}
