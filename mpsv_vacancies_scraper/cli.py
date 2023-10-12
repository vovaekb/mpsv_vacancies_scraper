import argparse
from core import Core

parser = argparse.ArgumentParser()


def main():
    parser.add_argument('--city', required=True, type=str)
    parser.add_argument('--profession', required=False, type=str)
    args = parser.parse_args()
    print(f'Search for position on {args.profession} in {args.city}')

    app = Core()
    vacancies_data, error = app.get_vacancies(args.city,
                                              args.profession)
    if not error is None:
        # raise exception with error
        print(f'Error occurred: {error}')
    else:
        print(vacancies_data)


if __name__ == '__main__':
    main()
