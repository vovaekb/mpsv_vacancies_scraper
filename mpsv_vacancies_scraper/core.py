import json

import redis
from redis import StrictRedis

from config import redis_config
from scraper import VacanciesScraper


class Core:
    redis = StrictRedis(**redis_config)

    def get_vacancies(self, city: str, profession: str = 'developer') -> (list, str):
        print('Core::getVacancies')
        redis_key = f'mpsv_vacancies:{profession}_{city}'

        try:
            redis_data = self.redis.get(redis_key)
        except redis.exceptions.ConnectionError:
            print('Redis server is not available')
            return (None, 'Redis server is not available')

        if redis_data:
            print('Vacancies data retrieved from Redis')
            return (redis_data, None)
        else:
            # Perform html request using Scraper class
            print('Retrieve data from mpsv portal')
            scraper = VacanciesScraper(city, profession)
            vacancies_data = scraper.search()
            vacancies_data = json.dumps(vacancies_data)
            self.redis.setex(
                redis_key,
                60 * 60,
                vacancies_data
            )
            return (vacancies_data, None)
