import requests
from bs4 import BeautifulSoup

HEAD_HUNTER_URL = 'https://api.hh.ru/vacancies'
FLEX_JOBS_URL = 'https://www.flexjobs.com/search?search=&search={query}'
INDEED_URL = 'https://www.indeed.com/jobs?q={query}&l=&ts=1621597199451&rq=1&rsIdx=0&fromage=last&newcount=38396'
SUPER_JOB_URL = 'https://ru.jobsora.com/работа-{query}'


async def count_head_hunter(query: str) -> int:
    payload = {'text': query, 'search_field': ['description', 'name']}
    response = requests.get(HEAD_HUNTER_URL, params=payload).json()
    return int(response.get('found', -1))


async def count_flex_jobs(query: str) -> int:
    url = FLEX_JOBS_URL.format(query='+'.join(query.split()))
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    vacancies_tag = soup.find('h4', attrs={'style': 'margin:0;font-size:14px;'})

    vacancies = vacancies_tag.text
    start_index = vacancies.index('of') + 2
    end_index = vacancies.index('for') - 3
    vacancies_count = vacancies[start_index: end_index].strip()

    return vacancies_count


async def count_indeed(query: str) -> int:
    url = INDEED_URL.format(query='+'.join(query.split()))
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    vacancies_tag = soup.select('div#searchCountPages')[0]

    vacancies = vacancies_tag.text
    of_ind, jobs_ind = vacancies.index('of'), vacancies.index('jobs')
    vacancies_count = vacancies[of_ind + 2: jobs_ind].strip()
    vacancies_count = int(vacancies_count.replace(',', ''))

    return vacancies_count
