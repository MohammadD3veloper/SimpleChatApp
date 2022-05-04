web: daphne simple_chat.asgi:application --port $PORT --bind 0.0.0.0 -v2
celeryd: celery -A simple_chat.celery worker -E -B --loglevel=INFO
tor: ./tor/bin/run_tor & gunicorn simple_chat.wsgi