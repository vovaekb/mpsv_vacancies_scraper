from flask import Flask, request, Response, render_template

from core import Core

app = Flask(__name__)


# Custom exception class
class CustomError(Exception):
    """Some internal error"""


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(CustomError)
def handle_custom_exception(error):
    print('Handle CustomError')
    print(error.args[0])
    details = error.args[0]
    resp = Response(details['message'], status=200, mimetype='text/plain')
    return resp


@app.route('/')
def index():
    return 'Hello from my API'


@app.route('/search', methods=['GET'])
def search():
    city = request.args.get('city')
    profession = request.args.get('profession')
    print(f'Search for position on {profession} in {city}')
    scraper_core = Core()
    vacancies_data, error = scraper_core.get_vacancies(city, profession)
    if not error is None:
        raise CustomError({'message': error})
    else:
        resp = Response(vacancies_data, status=200, mimetype='application/json')
        return resp


if __name__ == '__main__':
    app.run()
