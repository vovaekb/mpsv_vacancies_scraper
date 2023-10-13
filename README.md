# mpsv_vacancies_scraper

👨‍💼 Parser script for obtaining job positions published on official portal of The Ministry of Labour and Social Affairs of Czech republic ([https://www.mpsv.cz/](https://www.mpsv.cz/)).
Two clients:
- Flask REST API
- CLI script

## Flask REST API
🚀 To run Flask app
```
python api.py
```

### Test in browser
🌐 Navigate to url http://127.0.0.1:5000/ in browser.

REST API endpoints:

* /search (GET) - parsing currency rates from cbr.ru API. Accepts query parameters: city (city to search job positions), profession(speciality). Returns JSON with list of job positions.

## CLI script
🖥️ To run script
```
python cli.py --city <city> --profession <profession>
```
