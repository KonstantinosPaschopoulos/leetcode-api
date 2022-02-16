import requests
import random
from fastapi import FastAPI
from bs4 import BeautifulSoup
from starlette.responses import FileResponse

app = FastAPI()
favicon_path = 'favicon.ico'


@app.get("/")
async def root():
    problem_url = get_random_problem()

    return {
        "status": 200,
        "problem_url": problem_url,
    }


def get_random_problem():
    problems = []
    page = random.randint(1, 43)
    problem = random.randint(1, 50)

    url = f"https://leetcode.com/problemset/all/?page={page}"
    response = requests.get(url, verify=True)
    soup = BeautifulSoup(response.text, 'html.parser')

    for x in soup.findAll('div', {'class': 'odd:bg-overlay-3 dark:odd:bg-dark-overlay-1 even:bg-overlay-1 dark:even:bg-dark-overlay-3'}):
        for y in x.findAll('a', {'class': 'h-5 hover:text-primary-s dark:hover:text-dark-primary-s'}, href=True):
            problems.append(y['href'])

    return f"https://leetcode.com{problems[problem]}"


@app.get('/favicon.ico')
async def favicon():
    return FileResponse(favicon_path)
