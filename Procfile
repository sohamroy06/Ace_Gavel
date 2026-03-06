web: python initialize.py && gunicorn -b 0.0.0.0:$PORT -w 4 gavel:app
worker: celery -A gavel:celery worker --loglevel=info
