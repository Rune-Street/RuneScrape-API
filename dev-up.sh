cd "${0%/*}"

# flask db upgrade
gunicorn --reload --worker-class eventlet runescrape_api.wsgi:app
