cd "${0%/*}"

flask db upgrade
gunicorn --reload runescrape_api.wsgi:app
