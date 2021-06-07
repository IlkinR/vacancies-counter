from fastapi import FastAPI
from services import count_flex_jobs, count_indeed

api = FastAPI()


@api.get('/flexjobs/{query}')
async def flexjobs(query: str):
    vacancies = await count_flex_jobs(query)
    return {'job': query, 'items': vacancies, 'source': 'flexjobs'}


@api.get('/indeed/{query}')
async def indeed(query: str):
    vacancies = await count_indeed(query)
    return {'job': query, 'items': vacancies, 'source': 'indeed'}
