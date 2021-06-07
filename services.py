import asyncio
import requests
from bs4 import BeautifulSoup
import aiohttp

HEAD_HUNTER_URL = 'https://api.hh.ru/vacancies'
FLEX_JOBS_URL = 'https://www.flexjobs.com/search?search=&search={query}'
INDEED_URL = 'https://www.indeed.com/jobs?q={query}&l=&ts=1621597199451&rq=1&rsIdx=0&fromage=last&newcount=38396'
SUPER_JOB_URL = 'https://ru.jobsora.com/работа-{query}'


async def get_soup(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
            soup = BeautifulSoup(response, 'lxml')
            return soup


class FlexJobCounter:
    SEARCH_URL_JOINER = '+'
    FLEX_JOBS_URL = 'https://www.flexjobs.com/search?search=&search={query}'
    VACANCIES_TAG_ATTRS = {'style': 'margin:0;font-size:14px;'}

    @classmethod
    def _get_search_url(cls, searched_job) -> str:
        words = searched_job.split()
        search_query = cls.SEARCH_URL_JOINER.join(words)
        return cls.FLEX_JOBS_URL.format(query=search_query)

    @classmethod
    def _extract_vacancies(cls, soup) -> str:
        vacancies_tag = soup.find('h4', attrs=cls.VACANCIES_TAG_ATTRS)
        vacancies = vacancies_tag.text
        vacancies_slice = slice(
            vacancies.index('of') + 2,
            vacancies.index('for') - 3
        )
        return vacancies[vacancies_slice].strip()

    def __init__(self, searched_job) -> None:
        self.search_url = FlexJobCounter._get_search_url(searched_job)

    async def count_vacancies(self) -> str:
        soup = await get_soup(self.search_url)
        return FlexJobCounter._extract_vacancies(soup)


class IndeedCounter:
    SEARCH_URL_JOINER = '+'
    INDEED_URL = 'https://www.indeed.com/jobs?q={query}&l=&ts=1621597199451&rq=1&rsIdx=0&fromage=last&newcount=38396'
    VACANCIES_TAG_PATH = 'div#searchCountPages'

    @classmethod
    def _get_search_url(cls, searched_job) -> str:
        words = searched_job.split()
        search_query = cls.SEARCH_URL_JOINER.join(words)
        return cls.INDEED_URL.format(query=search_query)

    @classmethod
    def _extract_vacancies(cls, soup) -> str:
        vacancies_tag = soup.select(cls.VACANCIES_TAG_PATH)[0]
        vacancies = vacancies_tag.text
        start, end = vacancies.index('of'), vacancies.index('jobs')
        return vacancies[start + 2: end].strip()

    def __init__(self, searched_job) -> None:
        self.search_url = IndeedCounter._get_search_url(searched_job)

    async def count_vacancies(self) -> str:
        soup = await get_soup(self.search_url)
        return IndeedCounter._extract_vacancies(soup)
