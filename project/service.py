import requests


def get_questions_json(count: int):
    response = requests.get(f'https://jservice.io/api/random?count={count}')
    return response.json()

